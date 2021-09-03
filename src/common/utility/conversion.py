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

"""
Required type conversions
""" 

def convert_byte32_arr_to_hex_arr(byte32_arr):
    """
    This function takes in an array of byte32 strings and
    returns an array of hex strings.

    Parameters:
    byte32_arr Strings to convert from a byte32 array to a hex array
    """
    hex_ids = []
    for byte32_str in byte32_arr:
        hex_ids = hex_ids + [byte32_str.hex()]
    return hex_ids
