#!/usr/bin/env python

'''
Dynamic inventory script for db-host-prep
'''

import os
import sys
import argparse
import json
import boto3
import socket
import dns.resolver
import dns.reversename

class dynamicInventory(object):

    def __init__(self):
        self.inventory = {}
        self.labId = os.environ['LAB_ID']

        self.parse_args()

        if self.args.list:
            self.inventory = self.lab_inventory()
        elif self.args.host:
            self.inventory = self.empty_hostvars()
        else:
            self.inventory = self.empty_hostvars()

        print(json.dumps(self.inventory))

    def lab_inventory(self):
        inventoryJson = {}
        inventoryJson['lab'] = {"hosts": [], "vars": {}}
        inventoryJson['_meta'] = {"hostvars": {}}
        hostname = socket.gethostname()

        filters = [
            {
                'Name': 'tag:LabName',
                'Values': [self.labId]
            }
        ]

        ip_result = dns.resolver.query(hostname, 'A')
        arpa_result = dns.reversename.from_address(ip_result[0].to_text())
        fqdn_result = dns.resolver.query(arpa_result, 'PTR')
        host_fqdn = fqdn_result[0].to_text()
        domain_name = host_fqdn.split('.',1)[1].rstrip('.')

        inventoryJson['lab']['vars']['domain'] = domain_name

        ec2 = boto3.resource('ec2')
        instances = ec2.instances.filter(Filters=filters)

        for instance in instances:
            for tags in instance.tags:
                if tags["Key"] == 'Name':
                    inventoryJson['lab']['hosts'].append(tags["Value"])

        return inventoryJson

    def empty_hostvars(self):
        return {'_meta': {'hostvars': {}}}

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

def main():
    if "LAB_ID" in os.environ:
        dynamicInventory()
    else:
        print("Please set LAB_ID environment variable before running this script.")
        sys.exit(1)

if __name__ == '__main__':

    try:
        main()
    except SystemExit as e:
        if e.code == 0:
            os._exit(0)
        else:
            os._exit(e.code)