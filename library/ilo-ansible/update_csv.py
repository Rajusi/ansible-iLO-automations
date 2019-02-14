from tempfile import NamedTemporaryFile
import shutil
import csv

from ansible.module_utils.basic import *

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

