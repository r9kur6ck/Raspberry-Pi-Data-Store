#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime
import argparse

import db


# オプション解析
arg_parser = argparse.ArgumentParser(description='register Ethereum')
arg_parser.add_argument('--id', help='ID', required=True)
arg_parser.add_argument('--name', help='name', required=True)
arg_parser.add_argument('--address', help='server address(hostname or IP address)', default="127.0.0.1")
arg_parser.add_argument('--port', help='port nuber', type=int, default=8545)
arg_parser.add_argument('--account', help='account address', required=True)
arg_parser.add_argument('--password', help='account password', required=True)
arg_parser.add_argument('--privatekey', help='account private key', required=True)
args = arg_parser.parse_args()
print(args)

id = args.id
name = args.name
address = args.address
port = args.port
acc = args.account
pw = args.password
pk = args.privatekey

s = db.DB()
r = db.DsEthereum(id=id, name=name, address=address, port=port, account=acc, password=pw,private_key=pk)
print(r)
s.insert(r)
print(s)

s.db_disconnect()
