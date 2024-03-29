# Copyright 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json
import time
from enums.error_code import WorkOrderStatus
from handler.http_jrpc_client import HttpJrpcClient
from interfaces.work_order import WorkOrder
from exceptions.invalid_parameter import InvalidParamException
from validation.argument_validator import ArgumentValidator
from validation.json_validator import JsonValidator
from handler.error_handler import error_handler

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


class JRPCWorkOrderImpl(WorkOrder):
    """
    This class is to manage to the work orders from client side.
    """

    def __init__(self, config):
        self.__uri_client = HttpJrpcClient(config.get("json_rpc_uri"))
        self.validation = ArgumentValidator()


    @error_handler
    def work_order_submit(self, work_order_request, id=None):
        """
        Submit a work order request to an Avalon listener.

        Parameters:
        work_order_id     Work order ID
        worker_id         Worker ID value derived from the worker's DID
        requester_id      Requester ID
        work_order_request Work order request in JSON RPC string format
        id                Optional JSON RPC request ID
        """
        
        # JSON Validation
        JsonValidator.json_validation(id, "WorkOrderSubmit", json.loads(work_order_request))

        work_order_req_json = json.loads(work_order_request)
        # Argument validation
        self.validation.not_null(id, work_order_req_json)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderSubmit",
            "id": id
        }
        json_rpc_request["params"] = work_order_req_json

        logging.info("Work order request %s", json_rpc_request)
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_get_result_nonblocking(self, work_order_id, id=None):
        """
        Get the work order result in non-blocking way.

        Parameters:
        work_order_id     Work order ID
        id                Optional JSON RPC request ID

        Returns:
        JSON RPC response of dictionary type
        """
        # Argument validation
        self.validation.not_null(id, work_order_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderGetResult",
            "id": id,
            "params": {
                "workOrderId": work_order_id
            }
        }
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_get_result(self, work_order_id, id=None):
        """
        Get the work order result in a blocking way until it gets a
        result or error.

        Parameters:
        work_order_id     Work order ID
        id                Optional JSON RPC request ID

        Returns:
        JSON RPC response of dictionary type
        """
        self.validation.not_null(id, work_order_id)

        response = self.work_order_get_result_nonblocking(work_order_id, id)
        if "error" in response:
            if response["error"]["code"] != WorkOrderStatus.PENDING:
                return response
            else:
                while "error" in response and \
                        response["error"]["code"] == WorkOrderStatus.PENDING:
                    response = self.work_order_get_result_nonblocking(
                        work_order_id, id)
                    # TODO: currently pooling after every 2 sec interval
                    # forever.
                    # We should implement feature to timeout after
                    # responseTimeoutMsecs in the request.
                    time.sleep(2)
                return response
        else:
            return response

    @error_handler
    def encryption_key_get(self, worker_id, requester_id,
                           last_used_key_nonce=None, tag=None,
                           signature_nonce=None, signature=None, id=None):
        """
        API to receive a worker's key.

        Parameters:
        worker_id           Worker ID of the worker whose encryption key
                            is requested
        last_used_key_nonce Optional nonce associated with the last retrieved
                            key. If it is provided, the key retrieved should
                            be newer than this one.
                            Otherwise any key can be retrieved
        tag                 Tag that should be associated with the returned
                            key, e.g. the requester ID. This is an optional
                            parameter. If it is not provided, requester_id is
                            used as a key
        requester_id        ID of the requester that plans to use
                            the returned key to submit one or more work orders
                            using this key
        signature_nonce     Optional nonce associated with the signature and
                            is used only if signature below is also provided
        signature           Optional signature of worker_id,
                            last_used_key_nonce, tag, and signature_nonce.
        id                  Optional JSON RPC request ID
        """
        self.validation.not_null(id, worker_id, requester_id)
        
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "EncryptionKeyGet",
            "id": id,
            "params": {
                "workerId": worker_id,
                "lastUsedKeyNonce": last_used_key_nonce,
                "tag": tag,
                "requesterId": requester_id,
                "signatureNonce": signature_nonce,
                "signature": signature
            }
        }
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def encryption_key_set(self, worker_id, encryption_key, encryption_nonce,
                           tag, signature_nonce, signature, id=None):
        """
        API called by a Worker or Worker Service to receive a Worker's key.

        Parameters:
        worker_id        ID of the worker to set an encryption key
        encryption_key   Encryption key to set
        encryption_nonce Nonce associated with the key
        tag              Tag that should be associated with the returned key,
                         e.g. requester ID.
        signature_nonce  Nonce associated with the signature
        signature        Signature generated by the worker on the worker_id,
                         tag and encryption_nonce
        id               Optional JSON RPC request ID

        Returns:
        JRPC response with the result of the operation.
        """
        # Not supported for direct model.
        message = "Operation is not supported"
        raise InvalidParamException(message, id)
