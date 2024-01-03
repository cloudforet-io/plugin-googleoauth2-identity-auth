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

__all__ = ["GoogleConnector"]

import json
import requests
import logging

from spaceone.core.error import *
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger(__name__)


class GoogleConnector(BaseConnector):
    auth_type = "GOOGLE_OAUTH2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_server = "https://www.googleapis.com"
        self.token_url = "%s/oauth2/v2/tokeninfo" % self.auth_server
        self.user_url = "%s/oauth2/v3/userinfo" % self.auth_server

    def init(self, options):
        # This is connection check for Google Authorization Server
        # URL: https://www.googleapis.com/oauth2/v4/token
        # After connection without param.
        # It should return 404
        response = requests.get(self.auth_server)
        if response.status_code == 404:
            return "ACTIVE"
        else:
            raise ERROR_NOT_FOUND(key="auth_server", value=self.auth_server)

    def authorize(self, options, secret_data, credentials):
        """
        options
        credentials:
          - access_token
        """
        # Authorization Grant
        headers = {"Content-Type": "application/json"}
        data = {
            "access_token": credentials["access_token"],
        }
        _LOGGER.debug(f"[authorize] data: {data}")
        # Check tokeninfo
        response = requests.post(self.token_url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            _LOGGER.debug(
                f"GoogleConnector return code {response.status_code} : {response.json()}"
            )
            raise ERROR_NOT_FOUND(key="user", value="<from access_token>")

        # status_code == 200
        response_info = response.json()
        _LOGGER.debug(f"response: {response_info}")

        user_info = {}
        if email := response_info.get("email"):
            user_info["email"] = email
            user_info["user_id"] = email
            user_info["state"] = "ENABLED"
            return user_info
        raise ERROR_NOT_FOUND(key="user", value="<from access_token>")

    def get_endpoint(self, options):
        result = {
            "authorization_endpoint": self.auth_server,
            "token_endpoint": self.token_url,
            "userinfo_endpoint": self.user_url,
        }
        return result
