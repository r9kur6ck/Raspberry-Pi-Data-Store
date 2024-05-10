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
arg_parser.add_argument('--url', help='path', required=True)
arg_parser.add_argument('--method', help='method', required=True)
arg_parser.add_argument('--act_pre', help='call pre action', action='store_true')
arg_parser.add_argument('--act_post', help='call post action', action='store_true')
arg_parser.add_argument('--func_id', help='function id', required=True)
args = arg_parser.parse_args()
print(args)

id = args.id
name = args.name
url = args.url
method = args.method
act_pre = args.act_pre
act_post = args.act_post
func_id = args.func_id

s = db.DB()
r = db.DsEvent(id=id, name=name, url=url, method=method, act_pre=act_pre, act_post=act_post, func_id=func_id)
print(r)
s.insert(r)
print(s)

s.db_disconnect()
