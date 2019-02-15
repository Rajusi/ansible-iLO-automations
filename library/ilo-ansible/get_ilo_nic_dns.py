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

import sys
import logging
import json
import time
import redfish.ris.tpdefs
from redfish import AuthMethod, redfish_client
from ansible.module_utils._redfishobject import RedfishObject
from redfish.rest.v1 import ServerDownOrUnreachableError

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: get_ilo_nic_dns
short_description: Get iLO DNS Servers
description:
    - Provides an interface to Get iLO DNS Servers
requirements:
    - "python >= 3.6"
author: "GSE"
'''

EXAMPLES = '''
- name: get iLO DNS Servers
  get_ilo_nic_dns:
    ilo_ip: "x.x.x.x"
    ilo_use: "username"
    ilo_pass: "password"
'''

def get_ilo_nic_dns(redfishobj, get_active):
    instances = redfishobj.search_for_type("Manager.")

    for instance in instances:
        tmp = redfishobj.redfish_get(instance["@odata.id"])  

        response = redfishobj.redfish_get(tmp.dict["EthernetInterfaces"]\
                                                                ["@odata.id"])

        for entry in response.dict["Members"]:
            nic = redfishobj.redfish_get(entry["@odata.id"])

            if get_active and nic.dict["Status"]["State"] == "Enabled":
                if redfishobj.typepath.defs.isgen9:
                    oemhpdict = nic.dict["Oem"]["Hp"]
                else:
                    oemhpdict = nic.dict["Oem"]["Hpe"]
                return oemhpdict["IPv4"]["DNSServers"]



if __name__ == "__main__":

    module = AnsibleModule(
    argument_spec=dict(
            ilo_ip=dict(required=True, type='str'),
            ilo_pass=dict(required=True, type='str'),
            ilo_user=dict(required=True, type='str')
                      )
            )


    iLO_https_url = "https://" + module.params['ilo_ip']
    iLO_account = module.params['ilo_user']
    iLO_password = module.params['ilo_pass']

    try:
        REDFISH_OBJ = RedfishObject(iLO_https_url, iLO_account, iLO_password)
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or doesn't support " \
                                                                "RedFish.\n")
        sys.exit()
    except Exception as excp:
        raise excp

    response = get_ilo_nic_dns(REDFISH_OBJ, True)
    REDFISH_OBJ.redfish_client.logout()

    if not response:
        module.fail_json(msg="Could not rertive DNSservers!")
    else:
        module.exit_json(changed=True, DNSServers=response)
  
