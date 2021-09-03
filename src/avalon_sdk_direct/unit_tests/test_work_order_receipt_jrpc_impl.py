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
        self.__work_order_id = "1bf7b8ee900cdae9d866d388d277bb3a570e465875af383bd3063ecf1998d971" 
        self.__worker_service_id = secrets.token_hex(32)
        self.__worker_id = "0b03616a46ea9cf574f3f8eedc93a62c691a60dbd3783427c0243bacfe5bba94"
        self.__requester_id = secrets.token_hex(32)
        self.__receipt_create_status = 0
        self.__work_order_request_hash = base64.b64encode(str.encode(
                "SampleHash", "utf-8")).decode("utf-8")
        self.__requester_generated_nonce = secrets.token_hex(32)
        self.__requester_signature = base64.b64encode(str.encode(
                "SampleRequesterSignature", "utf-8")).decode("utf-8")
        self.__signature_rules = ""
        self.__receipt_verification_key = "AES-GCM-256"
        self.__receipt_status = None
        self.__updater_id = secrets.token_hex(32)
        self.__update_index = 0


    def test_work_order_receipt_retrieve(self):
        req_id = 31
        res = {}
        logging.info(
            "Calling work_order_receipt_retrieve with \n workOrderId " ,
            self.__work_order_id)
        res = self.__work_order_receipt_wrapper.work_order_receipt_retrieve(
                self.__work_order_id, req_id)
        logging.info("Result: %s\n", res)

        self.__worker_service_id = res['result']['workerServiceId']
        self.__worker_id = res['result']['workerId']
        self.__requester_id = res['result']['requesterId'] 
        self.__receipt_create_status =  res['result']['receiptCreateStatus']
        self.__work_order_request_hash = res['result']['workOrderRequestHash']

    def test_work_order_receipt_create(self):
        req_id = 32
        
        logging.info(
            "Calling work_order_receipt_create with \n work_order_id " +
            "%s\nworker_service_id %s\nworker_id %s\nrequester_id %s\nreceipt_create_status" +
            "%s\nwork_order_request_hash %s\nrequester_generated_nonce %s\n requester_signature" +
            "%s\nsignature_rules %s\nreceipt_verification_key %s\n",
            self.__work_order_id, self.__worker_service_id, self.__worker_id, self.__requester_id,
            self.__receipt_create_status, self.__work_order_request_hash, self.__requester_generated_nonce,
            self.__requester_signature, self.__requester_signature, self.__receipt_verification_key)

        res = self.__work_order_receipt_wrapper.work_order_receipt_create(
               self.__work_order_id, self.__worker_service_id, self.__worker_id, self.__requester_id,
               self.__receipt_create_status, self.__work_order_request_hash, self.__requester_generated_nonce,
                self.__requester_signature, self.__signature_rules, self.__receipt_verification_key, req_id)                
        logging.info("Result: %s\n", res)

    def test_work_order_receipt_update_retrieve(self):
        req_id = 33
        res = {}
        logging.info(
            "Calling work_order_receipt_update_retrieve with workOrderId %s\n" +
            ' updater_id %s\n update_index %s\n ',
            self.__work_order_id , self.__updater_id, self.__update_index)
        res = self.__work_order_receipt_wrapper.work_order_receipt_update_retrieve(
                self.__work_order_id, self.__updater_id, self.__update_index, req_id)
        logging.info("Result: %s\n", res)

        self.__update_type = res['result']['updateType']
        self.__update_data = res['result']['updateData']
        self.__update_signature = res['result']['updateSignature']

    def test_work_order_receipt_update(self):
        req_id = 34
        
        logging.info(
            "Calling work_order_receipt_update with \n work_order_id " +
            "%s\nupdater_id %s\nupdate_type %s\nupdate_data %s\nrupdate_signature" +
            "%s\nsignature_rules %s\n")

        res = self.__work_order_receipt_wrapper.work_order_receipt_update(
               self.__work_order_id, self.__updater_id, self.__update_type, self.__update_data,
               self.__update_signature, self.__signature_rules, req_id)                
        logging.info("Result: %s\n", res)
    
    def test_work_order_receipt_lookup(self):
        req_id = 35
        res = {}
        logging.info(
            "Calling work_order_receipt_lookup with \n worker_service_id " ,
            self.__worker_service_id)
        res = self.__work_order_receipt_wrapper.work_order_receipt_lookup(
                self.__worker_service_id, req_id)
        logging.info("Result: %s\n", res)

        #self.__worker_id = res['result']['ids'][0]
        self.__lookup_tag = res['result']['lookupTag']

    
    def test_work_order_receipt_lookup_next(self):
        req_id = 36
        logging.info(
            'Calling work_order_receipt_lookup_next with\n last_lookup_tag %d\n' +
            ' worker_service_id %s\n worker_id %s\n requester_id %s\n receipt_status %s\n',
            self.__lookup_tag, self.__worker_service_id, self.__worker_id,
            self.__requester_id, self.__receipt_status)
        res = self.__work_order_receipt_wrapper.work_order_receipt_lookup_next(
            self.__lookup_tag, self.__worker_service_id, self.__worker_id,
            self.__requester_id, self.__receipt_status, req_id)
        logging.info('Result: %s\n', res)

    
def main():
    logging.info("Running test cases...\n")
    config ={
              "json_rpc_uri" : "http://localhost:1947",
    }
    test = TestJRPCWorkOrderReceiptImpl(config)
    logging.info("********************************************************************************")
    test.test_work_order_receipt_retrieve()
    logging.info("********************************************************************************")
    test.test_work_order_receipt_create()
    logging.info("********************************************************************************")
    test.test_work_order_receipt_update()
    logging.info("********************************************************************************")
    test.test_work_order_receipt_update_retrieve()
    logging.info("********************************************************************************")
    test.test_work_order_receipt_lookup()
    logging.info("********************************************************************************")
    test.test.work_order_receipt_lookup_next()
    


if __name__ == "__main__":
    main()