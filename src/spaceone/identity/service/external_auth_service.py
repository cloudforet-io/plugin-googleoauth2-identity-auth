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

import logging

from spaceone.core.error import *
from spaceone.core.service import *

from spaceone.identity.error import *
from spaceone.identity.manager.external_auth_manager import ExternalAuthManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class ExternalAuthService(BaseService):
    resource = "ExternalAuth"

    def __init__(self, metadata):
        super().__init__(metadata)
        self.external_auth_manager: ExternalAuthManager = self.locator.get_manager(
            "ExternalAuthManager"
        )

    @transaction()
    @check_required(["options", "domain_id"])
    def init(self, params):
        """verify options
        Args:
            params
              - options
              - domain_id

        Returns:
            - metadata
        Raises:
            ERROR_NOT_FOUND:
        """
        options = params["options"]
        self.external_auth_manager.init(options)

        metadata = self.external_auth_manager.get_endpoint(options)
        metadata.update(options)
        metadata.update({"identity_provider": "google"})
        metadata.update({"protocol": "oauth2"})

        return {"metadata": metadata}

    @transaction()
    @check_required(["options", "secret_data", "credentials", "domain_id"])
    def authorize(self, params: dict):
        """verify options
        Args:
            params
              - 'options' : 'dict'
              - 'secret_data': may be empty dictionary
              - 'credentials': 'dict'                         #required
              - 'domain_id': 'str'                            #required
              - 'metadata': 'dict'

        Returns:

        Raises:
            ERROR_NOT_FOUND:
        """

        options = params["options"]
        secret_data = params["secret_data"]
        credentials = params["credentials"]
        domain_id = params["domain_id"]
        metadata = params.get("metadata", {})

        return self.external_auth_manager.authorize(
            options, secret_data, credentials, domain_id, metadata
        )
