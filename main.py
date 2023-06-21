#!python

# Generates a list of devices showing every component with a serial number

from vmanage_api import VmanageRestApi
from getpass import getpass
from time import sleep
import csv

vmanage_ip = input('Input vManage address in the format {name or ip}:{port}  : ')
vmanage_user = input('Input vManage user name: ')
vmanage_password = getpass('Input vManage password: ')

vmanage = VmanageRestApi(vmanage_ip, vmanage_user, vmanage_password)
if vmanage.token:
    print('vManage Login Success\n\n')

devices = vmanage.get_request('/device')

final_list = []
all_headers = ['system-ip']

for device in devices['data']:
    if (device['device-type'] == 'vedge') and (device['reachability'] == 'reachable'):
        try:
            hardware = vmanage.get_request(f'/device/hardware/inventory?deviceId={device["system-ip"]}')
            sleep(0.2)
            sn_list = {'system-ip': device['system-ip']}
            for item in list(hardware['data']):
                if 'serial-number' in item.keys():
                    sn_list[item['hw-description']] = item['serial-number']
                    if item['hw-description'] not in all_headers:
                        all_headers.append(item['hw-description'])
            final_list.append(sn_list)
            print(sn_list)
        except Exception as e:
            print(f'{e}\n{device}')

vmanage.logout()

with open('output.csv', 'w') as file:
    csv_output = csv.DictWriter(file, all_headers)
    csv_output.writeheader()
    csv_output.writerows(final_list)
