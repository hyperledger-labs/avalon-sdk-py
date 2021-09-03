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


import base64
import unittest
from os import path, environ
import errno
import toml
import secrets
import logging
from avalon_sdk_direct.jrpc_worker_registry import JRPCWorkerRegistryImpl


from avalon_sdk_direct.jrpc_work_order import JRPCWorkOrderImpl

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


class TestWorkOrderEncryptionKeyJRPCImpl(unittest.TestCase):
    def __init__(self, config):
        super(TestWorkOrderEncryptionKeyJRPCImpl, self).__init__()
        self.__config = config
        self.__wo_enc_updater = JRPCWorkOrderImpl(self.__config)
        

    def test_encryption_key_get(self):
        req_id = 31
        logging.info("testinh encryption key get")
        self.__workerId = secrets.token_hex(32)
        self.__last_used_key_nonce = secrets.token_hex(32)
        self.__tag = secrets.token_hex(32)
        self.__requester_id = secrets.token_hex(32)
        self.__signature_nonce = secrets.token_hex(32)
        self.__signature = secrets.token_hex(32)

        logging.info(
            "Calling encryption_key_get with workerId %s\n" +
            " lastUsedKeyNonce %s\n tag %s\n requesterId %s\n" +
            " signatureNonce %s\n, signature %s\n",
            self.__workerId, self.__last_used_key_nonce, self.__tag,
            self.__requester_id, self.__signature_nonce, self.__signature)
        res = self.__wo_enc_updater.encryption_key_get(
            self.__workerId,
            self.__last_used_key_nonce,
            self.__tag, self.__requester_id,
            self.__signature_nonce,
            self.__signature,
            req_id)
        logging.info("Result: %s\n", res)

    def test_encryption_key_set(self):
        req_id = 32
        workerId = "0x1234"
        logging.info(
            "Calling encryption_key_set with workerId %s\n" +
            " encryptionKey %s\n encryptionKeyNonce %s\n tag %s\n" +
            " signatureNonce %s\n signature %s\n",
            self.__workerId, self.__last_used_key_nonce, self.__tag,
            self.__requester_id, self.__signature_nonce, self.__signature)

        res = self.__wo_enc_updater.encryption_key_set(
            self.__workerId,
            self.__last_used_key_nonce,
            self.__tag, self.__requester_id,
            self.__signature_nonce,
            self.__signature,
            req_id)
        logging.info("Result: %s\n", res)
        self.assertEqual(
            res['id'], req_id, "encryption_key_set Response id doesn't match")


def main():
    logging.info("Running test cases...\n")
    tcf_home = environ.get("TCF_HOME", "../../")
    config = {
              "json_rpc_uri" : "http://localhost:1947",
    }
    # jrpc_worker = JRPCWorkerRegistryImpl(config)
    # req_id = 16
    # worker_ids = jrpc_worker.worker_lookup(
    #         worker_type=1, id=req_id)
    # logging.info(worker_ids)
    test = TestWorkOrderEncryptionKeyJRPCImpl(config)
    
    test.test_encryption_key_get()
    test.test_encryption_key_set()


if __name__ == "__main__":
    main()
