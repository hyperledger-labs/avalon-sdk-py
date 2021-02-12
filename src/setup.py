#!/usr/bin/env python

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

import os
import sys
import subprocess
import re

from setuptools import setup, find_packages

setup(name='avalon_sdk_direct',
      version='0.0.4',
      description='Avalon SDK ',
      author='Hyperledger Avalon ',
      author_email="karthika.murthy@intel.com",                                               
      url='https://github.com/hyperledger/avalon_sdk_py',    
      package_dir = {'enums' : 'common/enums',
                     'handler' : 'internal/handler/direct',
                     'interfaces' : 'common/interfaces',
                     'exceptions' : 'internal/exceptions',
                     'validation' : 'internal/validation',
                     'avalon_sdk_direct' : 'avalon_sdk_direct'},      
      packages=['enums',
                'handler', 
                'interfaces',
                'exceptions',
                'validation',
                'avalon_sdk_direct'
               ],

      package_data={'validation': ['data/*.json']},
      include_package_data=True,
      install_requires=['jsonschema'],
      entry_points={})
