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

from spaceone.api.identity.plugin import external_auth_pb2, external_auth_pb2_grpc
from spaceone.core.pygrpc import BaseAPI
from spaceone.core.pygrpc.message_type import *


class ExternalAuth(BaseAPI, external_auth_pb2_grpc.ExternalAuthServicer):
    pb2 = external_auth_pb2
    pb2_grpc = external_auth_pb2_grpc

    def init(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service(
            "ExternalAuthService", metadata
        ) as external_auth_svc:
            data = external_auth_svc.init(params)
            return self.locator.get_info("PluginInfo", data)

    def authorize(self, request, context):
        params, metadata = self.parse_request(request, context)

        with self.locator.get_service(
            "ExternalAuthService", metadata
        ) as external_auth_svc:
            data = external_auth_svc.authorize(params)
            return self.locator.get_info("UserInfo", data)
