#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2019) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from tempfile import NamedTemporaryFile
import shutil
import csv

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: update_csv
short_description: update specified column in CSV file.
description:
    - Provides an interface to update CSV file
requirements:
    - "python >= 3.6"
author: "GSE"
'''

EXAMPLES = '''
- name: update CSV with data
  update_csv:
    csvfile_path: "/path/to/csvfile"
    col_name: "<col>"
    ilo_ip: "x.x.x.x"
    data: "Data to be written"
'''

def update_csvfile(csvfile_path,ilo_ip, col_name, data):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    fields = ['iLO_IP', 'username', 'password', 'DNS_Servers','New_DNS_servers','Remarks']

    with open(csvfile_path, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['iLO_IP'] == str(ilo_ip):
                if col_name == "DNS_Servers":
                    row[col_name] = ';'.join(data)
                if col_name == "Remarks":
                    if data == False:
                        row[col_name] = "Success"
                    if data == True:
                        row[col_name] = "Failed"
            writer.writerow(row)
    
    shutil.move(tempfile.name, csvfile_path)

if __name__ == "__main__":

    module = AnsibleModule(
    argument_spec=dict(
            csvfile_path=dict(required=True, type='path'),
            ilo_ip=dict(required=True, type='str'),
            col_name=dict(required=True, type='str'),
            data=dict(required=True, type='raw')
                      )
            )
    
    csvfile_path = module.params['csvfile_path']
    col_name = module.params['col_name']
    ilo_ip = module.params['ilo_ip']
    data = module.params['data']
    
    update_csvfile(csvfile_path, ilo_ip, col_name, data)

    module.exit_json(changed=True, result='Updated CSV file.')

