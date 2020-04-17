#!/usr/bin/env python3

import subprocess
import optparse
import re

# take two argument, the interface that you want to change
# and the new mac address that you want to give
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface to change its mac address')
    parser.add_option('-m', '--mac', dest='new_mac', help='new mac address')
    return parser.parse_args()

# changing mac address
def change_mac(interface, new_mac):
    print('[+] Changing mac address for ' + interface + ' to ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

# function name is clear :p
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface]).decode('utf-8')
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w:', ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[+] Could not read MAC address.')


options = get_arguments()
# print(options[0].interface)

current_mac = get_current_mac(options[0].interface)
print('current MAC = ' + str(current_mac))

change_mac(options[0].interface, options[0].new_mac)

current_mac = get_current_mac(options[0].interface)
if current_mac == options[0].new_mac:
    print('[+] MAC address was successfully changed to ' + current_mac)
else:
    print('[+] MAC address did not get changed')
