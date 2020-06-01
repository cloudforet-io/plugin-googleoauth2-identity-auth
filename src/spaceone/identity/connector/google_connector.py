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
    def __init__(self, transaction, config):
        super().__init__(transaction, config)
        self.auth_server = 'https://www.googleapis.com'
        self.token_url = '%s/oauth2/v2/tokeninfo' % self.auth_server
        self.user_url = '%s/oauth2/v3/userinfo' % self.auth_server

    def verify(self, options):
        # This is connection check for Google Authorization Server
        # URL: https://www.googleapis.com/oauth2/v4/token
        # After connection without param.
        # It should return 404
        r = requests.get(self.auth_server)
        if r.status_code == 404:
            return "ACTIVE"
        else:
            raise ERROR_NOT_FOUND(key='auth_server', value=self.auth_server)

    def login(self, options, credentials, user_credentials):
        """
        options
        credentials:
          - access_token
        """
        # Authorization Grant
        headers={'Content-Type':'application/json'}
        data = {
            'access_token': user_credentials['access_token'],
        }
        _LOGGER.debug("data:%s" % data)
        # Check tokeninfo
        r = requests.post(self.token_url, headers=headers, data=json.dumps(data))
        if r.status_code != 200:
            _LOGGER.debug("GoogleConnector return code:%s" % r.json())
            raise ERROR_NOT_FOUND(key='user', value='<from access_token>')
        # status_code == 200
        r2 = r.json()
        _LOGGER.debug(f'response: {r2}')
        result = {}
        if 'email' in r2:
            result['email'] = r2['email']
            result['user_id'] = r2['email']
            result['state'] = 'ENABLED'
            return result
        raise ERROR_NOT_FOUND(key='user', value='<from access_token>')


    def find(self, options, params):
        # TODO: NOT SUPPORT
        raise ERROR_NOT_FOUND(key='find', value='does not support')
