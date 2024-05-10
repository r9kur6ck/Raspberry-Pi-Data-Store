#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime
import argparse

import db


# オプション解析
arg_parser = argparse.ArgumentParser(description='register Function')
arg_parser.add_argument('--id', help='ID', required=True)
arg_parser.add_argument('--name', help='name', required=True)
arg_parser.add_argument('--address', help='contract address', required=True)
arg_parser.add_argument('--abi', help='contract ABI', required=True)
args = arg_parser.parse_args()
print(args)

id = args.id
name = args.name
addr = args.address
abi = args.abi

s = db.DB()
r = db.DsFunction(id=id, name=name, address=addr, abi=abi)
print(r)
s.insert(r)
print(s)

s.db_disconnect()
