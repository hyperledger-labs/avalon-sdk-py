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
from enums.worker import WorkerType
from validation.argument_validator import ArgumentValidator
from validation.json_validator import JsonValidator
from interfaces.worker_registry \
     import WorkerRegistry
from handler.http_jrpc_client import HttpJrpcClient
from handler.error_handler import error_handler


class JRPCWorkerRegistryImpl(WorkerRegistry):
    """
    This class is to read the worker registry to get the more details
    of worker.
    """

    def __init__(self, config):
        self.__uri_client = HttpJrpcClient(config.get("json_rpc_uri"))
        self.validation = ArgumentValidator()

    @error_handler
    def worker_retrieve(self, worker_id, id=None):
        """
        Retrieve the worker identified by worker ID.

        Parameters:
        worker_id Worker ID value derived from the worker's DID
        id        Optional Optional JSON RPC request ID

        Returns:
        JRPC response containing:
        organization ID, application ID, worker status,
        and worker details.
        """

        self.validation.not_null(id, worker_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkerRetrieve",
            "id": id,
            "params": {
                "workerId": worker_id
            }
        }
        
        JsonValidator.json_validation(id,"WorkerRetrieve", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def worker_lookup(self, worker_type=None, organization_id=None,
                      application_type_id=None, id=None):
        """
        Worker lookup based on worker type, organization ID,
        and application ID.
        All fields are optional and, if present, condition should match for
        all fields. If none are passed it should return all workers.

        Parameters:
        worker_type         Optional characteristic of Workers for which you
                            may wish to search. Currently defined types are:
                            * "TEE-SGX": an Intel SGX Trusted Execution
                              Environment
                            * "MPC": Multi-Party Compute
                            * "ZK": Zero-Knowledge
        organization_id     Optional parameter representing the
                            organization that hosts the Worker,
                            e.g. a bank in the consortium or
                            anonymous entity
        application_type_id Optional application type that has to be supported
                            by the worker
        id                  Optional Optional JSON RPC request ID


        Returns:
        JRPC response containing number of workers,
        lookup tag, and list of worker IDs.
        """
        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkerLookUp",
            "id": id,
            "params": {
            }
        }

        e_value = self.validation.enum_value(id, "WorkerType", worker_type)
        json_rpc_request["params"]["workerType"] = e_value

        if organization_id is not None:
            json_rpc_request["params"]["organizationId"] = organization_id

        if application_type_id is not None:
            json_rpc_request["params"]["applicationTypeId"] = \
                application_type_id

        JsonValidator.json_validation(id,"WorkerLookUp", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def worker_lookup_next(self, lookup_tag, worker_type=None,
                           organization_id=None, application_type_id=None,
                           id=None):
        """
        Retrieve subsequent Worker lookup results based on worker type,
        organization ID, and application ID.
        Similar to workerLookUp with additional parameter lookup_tag.

        Parameters:
        lookup_tag          Used to lookup subsequent results after calling
                            worker_lookup
        worker_type         Optional characteristic of Workers for which you
                            may wish to search. Currently defined types are:
                            * "TEE-SGX": an Intel SGX Trusted Execution
                              Environment
                            * "MPC": Multi-Party Compute
                            * "ZK": Zero-Knowledge
        organization_id     Optional parameter representing the
                            organization that hosts the Worker,
                            e.g. a bank in the consortium or
                            anonymous entity
        application_type_id Optional application type that has to be supported
                            by the worker
        id                  Optional Optional JSON RPC request ID

        Returns:
        JRPC response containing number of workers,
        lookup tag, and list of worker IDs.
        """

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkerLookUpNext",
            "id": id,
            "params": {
                "lookUpTag": lookup_tag
            }
        }

        e_value = self.validation.enum_value(id, "WorkerType",worker_type)
        json_rpc_request["params"]["workerType"] = e_value

        if organization_id is not None:
            json_rpc_request["params"]["organizationId"] = organization_id

        if application_type_id is not None:
            json_rpc_request["params"]["applicationTypeId"] = \
                application_type_id

        JsonValidator.json_validation(id,"WorkerLookUpNext", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def worker_register(self, worker_id, worker_type, org_id,
                        application_type_ids, details, id=None):
        """
        Adds worker details to registry

        Parameters:
        worker_id            Worker ID value derived from the worker's DID
        worker_type          Type of Worker. Currently defined types are:
                             * "TEE-SGX": an Intel SGX Trusted Execution
                               Environment
                             * "MPC": Multi-Party Compute
                             * "ZK": Zero-Knowledge
        org_id               Organization that hosts the Worker,
                             e.g. a bank in the consortium or
                             anonymous entity
        application_type_ids Application types supported by the worker
        id                   Optional JSON RPC request ID

        Returns:
        JRPC response with worker registry status.
        """
        
        self.validation.not_null(id, worker_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkerRegister",
            "id": id,
            "params": {
                "workerId": worker_id,
                "organizationId": org_id,
                "applicationTypeId": application_type_ids,
                "details": details
            }
        }

        e_value = self.validation.enum_value(id, "WorkerType",worker_type)
        json_rpc_request["params"]["workerType"] = e_value
        JsonValidator.json_validation(id,"WorkerRegister", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def worker_update(self, worker_id, details, id=None):
        """
        Update worker with new information.

        Parameters:
        worker_id Worker ID value derived from the worker's DID
        details   Detailed information about the worker in
                  JSON RPC format as defined in
        id        Optional JSON RPC request ID

        Returns:
        JRPC response with update status.
        """

        self.validation.not_null(id, worker_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkerUpdate",
            "id": id,
            "params": {
                "workerId": worker_id,
                "details": details
            }
        }

        JsonValidator.json_validation(id,"WorkerUpdate", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response

    @error_handler
    def worker_set_status(self, worker_id, status, id=None):
        """
        Set the worker status to active, offline,
        decommissioned, or compromised state.

        Parameters:
        worker_id  Worker ID value derived from the worker's DID
        status     Worker status value to set
        id         Optional JSON RPC request ID

        Returns:
        JRPC response with status.
        """

        self.validation.not_null(id, worker_id)

        json_rpc_request = {
            "jsonrpc": "2.0",
            "method": "WorkerSetStatus",
            "id": id,
            "params": {
                "workerId": worker_id,
                "status": status.value
            }
        }

        JsonValidator.json_validation(id,"WorkerSetStatus", json_rpc_request["params"])
        response = self.__uri_client._postmsg(json.dumps(json_rpc_request))
        return response
