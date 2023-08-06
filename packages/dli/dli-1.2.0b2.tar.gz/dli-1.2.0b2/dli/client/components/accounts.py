
import logging

from dli.client.components import SirenComponent
from dli.client.components.urls import accounts_urls
from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.models import AccountModel
from urllib.parse import urljoin


class Accounts(SirenComponent):

    def get_account_by_name(self, account_name):
        """
        Retreives account details given an account name. This may raise a 401
        error if you are not an admin on accounts. This usually means your
        API key must be a datalake-ops or datalake-mgmt key (depending on
        the enviroment).

        :param str account_name: The name of the account. For example found
                                 on package tech data ops.

        :returns: account object
        """
        response = self.session.get(
            urljoin(
                self._environment.accounts,
                '/__api_v2/groups'
            ),
            params={
                'filter[0][value]': account_name,
                'filter[0][operator]': 'eq',
                'filter[0][field]': 'name'
            }
        ).json()

        if not response['data']:
            raise CatalogueEntityNotFoundException(
                message=f'Account with name {account_name} not found'
            )

        data = response['data'][0]

        return AccountModel._from_v2_response(data)
