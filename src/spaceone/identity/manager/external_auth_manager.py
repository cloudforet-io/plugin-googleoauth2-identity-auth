# -*- coding: utf-8 -*-
#
#   Copyright 2020 The SpaceONE Authors.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

__all__ = ["ExternalAuthManager"]

import logging

from spaceone.core import config
from spaceone.core.error import *
from spaceone.core.manager import BaseManager

from spaceone.identity.connector.google_connector import GoogleConnector
from spaceone.identity.error.custom import *

_LOGGER = logging.getLogger(__name__)


class ExternalAuthManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.google_connector: GoogleConnector = self.locator.get_connector(
            "GoogleConnector"
        )

    def init(self, options: dict):
        """Check Google OAuth connection

        Args:
            options:
              - client_id
        """
        google_connector: GoogleConnector = self.locator.get_connector(
            "GoogleConnector"
        )
        response = google_connector.init(options)
        # ACTIVE/UNKNOWN
        return response

    def authorize(
        self,
        options: dict,
        secret_data: dict,
        credentials: dict,
        domain_id: str,
        schema_id: str = None,
    ):
        """Get access_token from credentials
        Args:
            'options' : 'dict',         # required
            'secret_data' : 'dict',     # required
            'credentials' : 'dict'      # required
            'domain_id' : 'str'         # required
            'schema_id' : 'str'
        Returns:
            'user_info' : 'dict'
        """

        user_info = self.google_connector.authorize(options, secret_data, credentials)
        # check user_info, if needed
        if validator := options.get("validator"):
            user_id = user_info["user_id"]
            self._verify_user_id(validator, user_id)
        return user_info

    def get_endpoint(self, options):
        """
        Discover endpoints
        """

        endpoints = self.google_connector.get_endpoint(options)
        return endpoints

    @staticmethod
    def _verify_user_id(validator: str, user_id: str):
        """
        Args:
            validator: domain name (ex. gmail.com or mz.co.kr)
            user_id: user_id (ex. choonho.son or choonho.son@gmail.com)

        Returns:
            user_id: full user_id (ex. choonho.son@gmail.com)
        Errors:
            ERROR_NOT_FOUND_USER_ID: if there is no matching
        """
        if user_id.endswith(f"@{validator}"):
            return user_id
        raise ERROR_NOT_FOUND_USER_ID(user_id=user_id)
