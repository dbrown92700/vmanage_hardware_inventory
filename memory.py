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
all_headers = [
    'vdevice-name',
    'model',
    'disk_size',
    'disk_avail',
    'disk_used',
    'mem_total',
    'mem_free',
    'mem_used'
]

for device in devices['data']:
    if (device['device-type'] == 'vedge') and (device['reachability'] == 'reachable'):
        try:
            hardware = vmanage.get_request(f'/device/system/status?deviceId={device["system-ip"]}')['data'][0]
            # print(hardware)
            sleep(0.2)
            inv_list = {}
            for item in list(all_headers):
                inv_list[item] = hardware[item]
                if 'disk' in item:
                    inv_list[item] = inv_list[item].replace('M', '000000')
            final_list.append(inv_list)
            print(inv_list)
        except Exception as e:
            continue
            print(f'{e}\n{device}')

vmanage.logout()

with open('memory.csv', 'w') as file:
    csv_output = csv.DictWriter(file, all_headers)
    csv_output.writeheader()
    csv_output.writerows(final_list)



"""
      "mem_used": "3229060",
      "procs": "505",
      "disk_avail": "11164M",
      "disk_mount": "/bootflash",
      "board_type": "Vedge-ISR",
      "vdevice-name": "100.64.255.1",
      "total_cpu_count": "8",
      "mem_cached": "2985744",
      "timezone": "UTC +0000",
      "reboot_type": "Initiated by other",
      "disk_fs": "/dev/bootflash1",
      "fp_cpu_count": "4",
      "chassis-serial-number": "FLM2240W0JU",
      "min1_avg": "1.99",
      "state_description": "All daemons up",
      "personality": "vEdge",
      "disk_used": "1539M",
      "disk_use": "12",
      "model": "vedge-ISR-4331",
      "disk_status": "enabled",
      "state": "green",
      "config_date/date-time-string": "Mon Jun 17 19:42:56 UTC 2024",
      "linux_cpu_count": "4",
      "reboot_reason": "Enabling controller-mode",
      "cpu_user": "13.05",
      "testbed_mode": "0",
      "min15_avg": "2.00",
      "disk_size": "13377M",
      "cpu_idle": "78.40",
      "mem_buffers": "721376",
      "model_sku": "None",
      "cpu_system": "8.53",
      "version": "17.12.03.0.3740",
      "min5_avg": "1.99",
      "tcpd_cpu_count": "0",
      "vdevice-host-name": "Branch-MEX-1",
      "mem_total": "16370844",
      "uptime": "10 days 00 hrs 52 min 06 sec",
      "vdevice-dataKey": "100.64.255.1",
      "mem_free": "13141784",
      "bootloader_version": "Not applicable",
      "device_role": "cEdge-SDWAN",
      "fips_mode": "disabled",
      "build_number": "Not applicable",
      "lastupdated": 1718652320505,
      "loghost_status": "disabled",
      "uptime-date": 1717785180000
"""