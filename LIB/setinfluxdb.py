#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime
import argparse

import db


# オプション解析
arg_parser = argparse.ArgumentParser(description='register InfluxDB')
arg_parser.add_argument('--id', help='ID', required=True)
arg_parser.add_argument('--name', help='name', required=True)
arg_parser.add_argument('--address', help='server address(hostname or IP address)', default="127.0.0.1")
arg_parser.add_argument('--port', help='port nuber', type=int, default=8086)
arg_parser.add_argument('--token', help='API token', required=True)
arg_parser.add_argument('--organization', help='orgnanization', default="MyDataServer")
args = arg_parser.parse_args()
print(args)

id = args.id
name = args.name
address = args.address
port = args.port
token = args.token
org  = args.organization


s = db.DB()
r = db.DsInfluxDB(id=id, name=name, address=address, port=port, token=token, organization=org)
print(r)
s.insert(r)
print(s)

s.db_disconnect()
