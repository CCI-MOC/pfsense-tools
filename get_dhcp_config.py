"""
This script reads the dhcp config from the firewall and prints to
stdout what looks like a dnsmasq config file
"""

import argparse
import requests

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--firewall-ip",
        help="Firewall ip",
        required=True,
    )
    parser.add_argument(
        "--token",
        help="Firewall Token",
        required=True,
    )
    parser.add_argument(
        "--parent-interface",
        help="Interface where the config is read from. Can be found from the url",
        required=True,
    )
    args = parser.parse_args()

    url = f"https://{args.firewall_ip}/api/v2/services/dhcp_server?id={args.parent_interface}"
    headers = {
        "accept": "application/json",
        "x-api-key": args.token
    }
    response = requests.get(url, headers=headers, verify=False)

    data = response.json()
    entries = data['data']['staticmap']

    for entry in entries:
        ip = entry['ipaddr']
        hostname = entry['hostname']
        mac = entry['mac']
        print(f"doesnt-matter,{mac},{ip},{hostname},12h")
