"""
This script reads a dnsmasq style conf file and then creates static dhcp map
in pfsense firewall
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
        help="Parent interface where the config is applied. Can be found from the url",
        required=True,
    )
    parser.add_argument(
        "--config-file",
        help="csv file of the format nothin,mac,ipaddr,hostname",
        required=True,
    )
    args = parser.parse_args()

    url = f"https://{args.firewall_ip}/api/v2/services/dhcp_server/static_mapping"
    headers = {
        "accept": "application/json",
        "x-api-key": args.token
    }
    # open a dnsmasq dhcp config file where each line looks like
    # dhcp-host=eth4,74:86:7A:F0:75:54,10.2.4.16,OCT4-16,12h
    with open(args.config_file, "r") as file:
        lines = [line.rstrip() for line in file]

    configs = []
    for line in lines:
        parameters = line.split(",")
        macaddr = parameters[1]
        ipaddr = parameters[2]
        hostname = parameters[3]
        configs.append({
            "parent_id": args.parent_interface,
            "mac": macaddr,
            "ipaddr": ipaddr,
            "hostname": hostname,
            "descr": hostname,
        })

    for config in configs:
        print(config['ipaddr'])
        response = requests.post(url, data=config, headers=headers, verify=False)
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
