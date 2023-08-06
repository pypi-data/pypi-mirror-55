import datetime
import jwt
import requests
import logging
import socket
import os

from collections.abc import Iterable
from http.cookiejar import CookiePolicy
from wrapt import ObjectProxy
from deprecated import deprecated
from http import HTTPStatus
from urllib.parse import urljoin, urlparse, parse_qs, ParseResult
from collections import defaultdict

from pypermedia import HypermediaClient
from requests_toolbelt.adapters import host_header_ssl

from dli import __version__
from dli.siren import siren_to_entity
from dli.client.components.auto_reg_metadata import AutoRegMetadata
from dli.client.components.datafile import Datafile
from dli.client.components.dataset import Dataset, Dictionary
from dli.client.components.me import Me
from dli.client.components.package import Package
from dli.client.components.search import Search
from dli.client.components.accounts import Accounts
from dli.client.exceptions import (
    DatalakeException, InsufficientPrivilegesException,
    InvalidPayloadException, UnAuthorisedAccessException,
    CatalogueEntityNotFoundException, AuthenticationFailure
)

from dli.siren import PatchedSirenBuilder

logger = logging.getLogger(__name__)


class _Environment:

    _catalogue_accounts_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 'accounts.datalake.ihsmarkit.com',
        'catalogue-uat.datalake.ihsmarkit.com': 'accounts-uat.datalake.ihsmarkit.com',
        'catalogue-uat2.datalake.ihsmarkit.com': 'accounts-uat2.datalake.ihsmarkit.com',
        'catalogue-dev.udpmarkit.net': 'accounts-dev.udpmarkit.net',
        'catalogue-qa.udpmarkit.net': 'accounts-qa.udpmarkit.net',
        'catalogue-qa2.udpmarkit.net': 'accounts-qa2.udpmarkit.net',
    }

    def __init__(self, api_root):
        """
        Class to manage the different endpoints

        :param str root_url: The root url of the catalogue
        """
        catalogue_parse_result = urlparse(api_root)

        self.catalogue = ParseResult(
            catalogue_parse_result.scheme, catalogue_parse_result.netloc,
            '', '', '', ''
        ).geturl()

        accounts_host = self._catalogue_accounts_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.accounts = ParseResult(
            catalogue_parse_result.scheme, accounts_host, '', '', '', ''
        ).geturl()


class DliClient(Accounts, AutoRegMetadata,
                Datafile, Dataset, Dictionary,
                Me, Package, Search):
    """
    Definition of a client. This client mixes in utility functions for
    manipulating packages, datasets and datafiles.
    """
    _environment_class = _Environment

    def __init__(self, api_key, api_root, host=None):
        self._environment = self._environment_class(api_root)
        self.api_key = api_key
        self.host = host
        self._session = self._new_session()

    def _new_session(self):
        return Session(
            self.api_key,
            self._environment,
            self.host,
        )

    @property
    def session(self):
        # if the session expired, then reauth
        # and create a new context
        if self._session.has_expired:
            self._session = self._new_session()
        return self._session

    @property
    def ctx(self):
        """ Alias to self.session for backward compatibility.
        """
        return self.session


class Response(ObjectProxy):

    def __init__(self, wrapped, builder, *args, **kwargs):
        super(Response, self).__init__(wrapped, *args, **kwargs)
        self.builder = builder

    @property
    def is_siren(self):
        return self.request.headers.get(
            'Content-Type', ''
        ).startswith('application/vnd.siren+json')

    def to_siren(self):
        # Pypermedias terminology, not mine
        python_object = self.builder._construct_entity(
            self.json()
        ).as_python_object()

        # Keep the response availible
        python_object._raw_response = self

        return python_object

    def to_many_siren(self, relation):
        return [
            siren_to_entity(c) for c in
            self.to_siren().get_entities(rel=relation)
        ]


class BlockAll(CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


class DLIAdapter(host_header_ssl.HostHeaderSSLAdapter):

    def __init__(self, session, *args, **kwargs):
        self.session = session
        super().__init__(*args, **kwargs)

    def add_headers(self, request, **kwargs):
        request.headers["X-Data-Lake-SDK-Version"] = str(__version__)
        # if a host has been provided, then we need to set it on the header
        if self.session.host:
            request.headers['Host'] = self.session.host


class DLIBearerAuthAdapter(DLIAdapter):
    def add_headers(self, request, **kwargs):
        super().add_headers(request, **kwargs)
        if self.session.auth_key and 'Authorization' not in request.headers:
            request.headers['Authorization'] = f'Bearer {self.session.auth_key}'


class DLISirenAdapter(DLIAdapter):
    def add_headers(self, request, **kwargs):
        super().add_headers(request, **kwargs)
        request.headers['Content-Type'] = "application/vnd.siren+json"


class DLICookieAuthAdapter(DLIAdapter):
    def add_headers(self, request, **kwargs):
        super().add_headers(request, **kwargs)
        # Accounts V1 authentication is broken, in that it only accepts
        # a cookie rather than an API key.
        request.headers['Cookie'] = f'oidc_id_token={self.session.auth_key}'


class DLIAccountsV1Adapter(DLISirenAdapter, DLICookieAuthAdapter):
    def add_headers(self, request, **kwargs):
        super().add_headers(request, **kwargs)


class DLIInterfaceV1Adapter(DLISirenAdapter, DLIBearerAuthAdapter):
    def add_headers(self, request, **kwargs):
        super().add_headers(request, **kwargs)


class Session(requests.Session):

    def __init__(self, api_key, environment, host, auth_key=None):
        super().__init__()
        self.api_key = api_key
        self._environment = environment
        self.host = host
        self.siren_builder = PatchedSirenBuilder()
        self.auth_key = auth_key or self._get_auth_key()
        self.token_expires_on = self.get_expiration_date(self.auth_key)

        self.mount(
            urljoin(self._environment.catalogue, '__api/'),
            DLIInterfaceV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.catalogue, '__api_v2/'),
            DLIBearerAuthAdapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, '__api/'),
            DLIAccountsV1Adapter(self)
        )

        self.mount(
            urljoin(self._environment.accounts, '__api_v2/'),
            DLIBearerAuthAdapter(self)
        )



        # Don't allow cookies to be set.
        # The new API will reject requests with both a cookie
        # and a auth header (as there's no predictiable crediential to choose).
        #
        # However the old API, once authenticate using a Bearer token will
        # as a side effect of a request return a oidc_id_token which matches
        # the auth header. This is ignored.
        self.cookies.set_policy(BlockAll())

    def request(self, method, url, *args, **kwargs):
        if not urlparse(url).netloc:
            url = urljoin(self._environment.catalogue, url)


        kwargs.pop('hooks', None)
        hooks = {'response': self._response_hook}

        try:
            return super().request(method, url, hooks=hooks, *args, **kwargs)
        except socket.error as e:
            raise ValueError('Unable to make request. Your sample_data '
                             'file may be too large. Please keep '
                             'uploads under 10 megabytes.') from e

    @staticmethod
    def get_expiration_date(token):
        # use a default_timeout if the token can't be decoded
        # until the proper endpoint is added on the catalog
        default_timeout = (
            datetime.datetime.utcnow() +
            datetime.timedelta(minutes=55)
        )

        try:
            # get the expiration from the jwt auth token
            decoded_token = jwt.decode(token, verify=False)
            if 'exp' not in decoded_token:
                return default_timeout

            return datetime.datetime.fromtimestamp(
                decoded_token['exp']
            )

        except Exception:
            return default_timeout

    @property
    def has_expired(self):
        # by default we don't want to fail if we could not decode the token
        # so if the ``token_expiry`` is undefined we assume the session
        # is valid
        if not self.token_expires_on:
            return False
        return datetime.datetime.utcnow() > self.token_expires_on

    def _response_hook(self, response, *args, **kwargs):
        # Appologies for the ugly code. The startswith siren check
        # is to make this onlly relevant to the old API.
        response = Response(response, self.siren_builder)

        if not response.ok:
            exceptions = defaultdict(
                lambda: DatalakeException,
                {HTTPStatus.BAD_REQUEST: InvalidPayloadException,
                 HTTPStatus.UNPROCESSABLE_ENTITY: InvalidPayloadException,
                 HTTPStatus.UNAUTHORIZED: UnAuthorisedAccessException,
                 HTTPStatus.FORBIDDEN: InsufficientPrivilegesException,
                 HTTPStatus.NOT_FOUND: CatalogueEntityNotFoundException}
            )

            try:
                message = response.json()
            except ValueError:
                message = response.text

            raise exceptions[response.status_code](
                message=message,
                params=parse_qs(urlparse(response.request.url).query),
                response=response,
            )

        return response

    def _get_auth_key(self):
        start_session_url = '/__api/start-session'

        try:
            response = self.post(
                '/__api/start-session', headers={
                    'Authorization': 'Bearer {}'.format(self.api_key)
                }
            )
        except DatalakeException as e:
            raise AuthenticationFailure(
                message='Could not authenticate API key'
            ) from e

        return response.text
