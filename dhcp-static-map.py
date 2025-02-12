"""
This script reads a dnsmasq style conf file and then creates static dhcp map
in pfsense firewall
"""

import requests
import os

firewall_ip = "https://10.208.0.1"
endpoint = "/api/v2/services/dhcp_server/static_mapping"
url = firewall_ip + endpoint
token = os.getenv("FIREWALL_API_TOKEN")
assert token, "please set FIREWALL_API_TOKEN"
headers = {
    "accept": "application/json",
    "x-api-key": token
}

# parent id can be found from the URL or by filtering the plural endpoint by name
parent_interface = "specify"

# open a dnsmasq dhcp config file where each line looks like
# dhcp-host=eth4,74:86:7A:F0:75:54,10.2.4.16,OCT4-16,12h
# just delete all the other configuration first!
with open("vlan911.conf", "r") as file:
    lines = [line.rstrip() for line in file]

configs = []
for line in lines:
    parameters = line.split(",")
    macaddr = parameters[1]
    ipaddr = parameters[2]
    hostname = parameters[3]
    configs.append({
        "parent_id": parent_interface,
        "mac": macaddr,
        "ipaddr": ipaddr,
        "hostname": hostname,
        "descr": hostname,
        "defaultleasetime": 43200, # 12 hours
    })

for config in configs:
    print(config['ipaddr'])
    response = requests.post(url, data=config, headers=headers, verify=False)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
        import ipdb; ipdb.set_trace()
