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

import json
import logging

from handler.http_jrpc_client import HttpJrpcClient
from interfaces.work_order_receipt import WorkOrderReceipt
from exceptions.invalid_parameter import InvalidParamException
from validation.argument_validator import ArgumentValidator
from validation.json_validator import JsonValidator
from handler.error_handler import error_handler

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


class JRPCWorkOrderReceiptImpl(WorkOrderReceipt):
    """
    This class is an implementation of WorkOrderReceiptInterface
    to manage work order receipts from the client side.
    """
    def __init__(self, config):
        self.__uri_client = HttpJrpcClient(config.get("json_rpc_uri"))
        self.validation = ArgumentValidator()

    @error_handler
    def work_order_receipt_create(
            self, work_order_id,
            worker_service_id,
            worker_id,
            requester_id,
            receipt_create_status,
            work_order_request_hash,
            requester_nonce,
            requester_signature,
            signature_rules,
            receipt_verification_key,
            id=None):
        """
        Create a Work Order Receipt JSON RPC request and submit to an
        Avalon listener.

        Parameters:
        work_order_id            Work order ID
        worker_service_id        Worker service ID
        worker_id                Worker ID value derived from the worker's DID
        requester_id             Requester ID
        receipt_create_status    Receipt creation status
        work_order_request_hash  Work order request hash value
        requester_nonce          Requester generated nonce
        requester_signature      Signature generated by the requester
        signature_rules          Defines hashing and signing algorithms;
                                 separated by forward slash '/'
        receipt_verification_key Receipt verification key
        id                       Optional JSON RPC request ID
        """

        self.validation.not_null(id, worker_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderReceiptCreate",
            "id": id,
            "params": {
                "workOrderId": work_order_id,
                "workerServiceId": worker_service_id,
                "workerId": worker_id,
                "requesterId": requester_id,
                "receiptCreateStatus": receipt_create_status,
                "workOrderRequestHash": work_order_request_hash,
                "requesterGeneratedNonce": requester_nonce,
                "requesterSignature": requester_signature,
                "signatureRules": signature_rules,
                "receiptVerificationKey": receipt_verification_key
            }
        }

        JsonValidator.json_validation(id,"WorkOrderReceiptCreate", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_receipt_update(
            self, work_order_id,
            updater_id,
            update_type,
            update_data,
            update_signature,
            signature_rules, id=None):
        """
        Update a Work Order Receipt JSON RPC request and submit an
        Avalon listener.

        Parameters:
        work_order_id    Work Order ID
        updater_id       Updater ID
        update_type      Updater type
        update_data      Receipt update data
        update_signature Signature of the update
        signature_rules  Defines hashing and signing algorithms;
                         separated by forward slash '/'
        id               Optional JSON RPC request ID
        """

        self.validation.not_null(id, work_order_id)
           
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderReceiptUpdate",
            "id": id,
            "params": {
                "workOrderId": work_order_id,
                "updaterId": updater_id,
                "updateType": update_type,
                "updateData": update_data,
                "updateSignature": update_signature,
                "signatureRules": signature_rules
            }
        }
        
        JsonValidator.json_validation(id,"WorkOrderReceiptUpdate", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_receipt_retrieve(self, work_order_id, id=None):
        """
        Retrieve a work order receipt JSON RPC request and submit to an
        Avalon listener.

        Parameters:
        work_order_id Work order ID
        id            Optional Optional JSON RPC request ID
        """

        self.validation.not_null(id, work_order_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderReceiptRetrieve",
            "id": id,
            "params": {
                "workOrderId": work_order_id
            }
        }
        JsonValidator.json_validation(id,"WorkOrderReceiptRetrieve", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_receipt_update_retrieve(
            self, work_order_id,
            updater_id,
            update_index, id=None):
        """
        Retrieve a work order receipt update JSON RPC request and submit to an
        Avalon listener.

        Parameters:
        work_order_id Work order ID
        id            Optional Optional JSON RPC request ID
        """

        self.validation.not_null(id, work_order_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderReceiptUpdateRetrieve",
            "id": id,
            "params": {
                "workOrderId": work_order_id,
                "updaterId": updater_id,
                "updateIndex": update_index
            }
        }
        JsonValidator.json_validation(id,"WorkOrderReceiptUpdateRetrieve", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_receipt_lookup(
            self, worker_service_id=None,
            worker_id=None, requester_id=None, receipt_status=None, id=None):
        """
        Work Order Receipt Lookup
        All fields are optional and, if present, condition should match for
        all fields. If none are passed it should return all
        work order receipts.

        Parameters:
        worker_service_id        Optional worker service ID to lookup
        worker_id                Optional worker ID value derived from
                                 the worker's DID
        requester_id             Optional requester ID to lookup
        receipt_status           Optional receipt status
        id                       Optional JSON RPC request ID
        """

        self.validation.not_null(id, worker_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderReceiptLookUp",
            "id": id,
            "params": {
            }
        }

        if worker_service_id is not None:
            json_rpc_request["params"]["workerServiceId"] = worker_service_id

        if worker_id is not None:
            json_rpc_request["params"]["workerId"] = worker_id

        if requester_id is not None:
            json_rpc_request["params"]["requesterId"] = requester_id

        if receipt_status is not None:
            json_rpc_request["params"]["requestCreateStatus"] = receipt_status
        
        JsonValidator.json_validation(id,"WorkOrderReceiptLookUp", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def work_order_receipt_lookup_next(
            self, last_lookup_tag,
            worker_service_id=None, worker_id=None, requester_id=None,
            receipt_status=None, id=None):
        """
        Work Order Receipt Lookup Next.
        Call to retrieve subsequent results after calling
        work_order_receipt_lookup or

        Parameters:
        last_lookup_tag          Last lookup tag returned by
                                 work_order_receipt_lookup
        worker_service_id        Optional worker service ID to lookup
        worker_id                Optional worker ID value derived from
                                 the worker's DID
        requester_id             Optional requester ID to lookup
        receipt_status           Optional receipt status
        id                       Optional JSON RPC request ID
        """

        self.validation.not_null(id, worker_id)
        
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkOrderReceiptLookUpNext",
            "id": id,
            "params": {
                "lastLookUpTag": last_lookup_tag
            }
        }

        if worker_service_id is not None:
            json_rpc_request["params"]["workerServiceId"] = worker_service_id

        if worker_id is not None:
            json_rpc_request["params"]["workerId"] = worker_id

        if requester_id is not None:
            json_rpc_request["params"]["requesterId"] = requester_id

        if receipt_status is not None:
            json_rpc_request["params"]["requestCreateStatus"] = receipt_status

        JsonValidator.json_validation(id,"WorkOrderReceiptLookUpNext", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response
