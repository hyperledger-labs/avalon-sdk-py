# Copyright 2019 Intel Corporation
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
from encodings.hex_codec import hex_encode
import unittest
from os import path, environ
import errno
import secrets
import time
import base64
import json

from avalon_sdk_direct.jrpc_work_order_receipt import JRPCWorkOrderReceiptImpl

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

class TestJRPCWorkOrderReceiptImpl(unittest.TestCase):
    def __init__(self, config):
        super(TestJRPCWorkOrderReceiptImpl, self).__init__()
        self.__config = config

        self.__work_order_receipt_wrapper = JRPCWorkOrderReceiptImpl(self.__config)
        self.__work_order_id = secrets.token_hex(32) 
        self.__worker_service_id = "50"
        self.__worker_id = secrets.token_hex(32)
        self.__requester_id = "0"
        self.__receipt_create_status = 0
        self.__work_order_request_hash = "whash"
        self.__requester_generated_nonce = "0"
        self.__requester_signature = "r_sig"
        self.__signature_rules = "SHA-256/RSA-OAEP-4096"
        self.__receipt_verification_key = "AES-GCM-256"
       
#           "verifyingKey": "-----BEGIN PUBLIC KEY-----\n" +
#           "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEW" +
#           "PblapM4eJI3vg8I8DhoKAeceop2VnqK\n" +
#           "40Yqs6WhLpxYvbYGrDsrIwNTZHrxNSHaX59APUpWamulen25G3LFCw==\n" +
#           "-----END PUBLIC KEY-----\n"
        
    def test_work_order_receipt_create(self):
        req_id = 21
        
        logging.info(
            "Calling work_order_receipt_create with \n work_order_id " +
            "%s\nworker_service_id %s\nworker_id %s\nrequester_id %s\nreceipt_create_status" +
            "%s\nwork_order_request_hash %s\nrequester_generated_nonce %s\n requester_signature" +
            "%s\nsignature_rules %s\nreceipt_verification_key %s\n")

        res = self.__work_order_receipt_wrapper.work_order_receipt_create(
               self.__work_order_id, self.__worker_service_id, self.__worker_id, self.__requester_id,
               self.__receipt_create_status, self.__work_order_request_hash, self.__requester_generated_nonce,
                self.__requester_signature, self.__signature_rules, self.__receipt_verification_key, req_id)                
        logging.info("Result: %s\n", res)

    def test_work_order_receipt_lookup(self):
        req_id = 25
        res = {}
        logging.info(
            "Calling work_order_receipt_lookup with \n worker_service_id " +
            "%s\nworker_id %s\nrequester_id %s\nreceipt_status %s\n",
            self.__worker_service_id, self.__worker_id, self.__requester_id, self.__receipt_status)
        res = self.__work_order_receipt_wrapper.work_order_receipt_lookup(
                self.__worker_id, req_id)
        logging.info("Result: %s\n", res)

    def test_work_order_receipt_retrieve(self):
        req_id = 22
        res = {}
        logging.info(
            "Calling work_order_receipt_retrieve with workOrderId %s\n",
            self.__work_order_id)
        res = self.__work_order_receipt_wrapper.work_order_receipt_retrieve(
                self.__work_order_id, req_id)
        logging.info("Result: %s\n", res)


def main():
    logging.info("Running test cases...\n")
    config ={
              "json_rpc_uri" : "http://localhost:1947",
    }
    test = TestJRPCWorkOrderReceiptImpl(config)
    logging.info("********************************************************************************")
    test.test_work_order_receipt_lookup()
    logging.info("********************************************************************************")
    test.test_work_order_receipt_create()
    logging.info("********************************************************************************")
    test.test_work_order_receipt_retrieve()


if __name__ == "__main__":
    main()