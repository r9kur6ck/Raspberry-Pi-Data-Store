#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime
import argparse

from LIB import db
from LIB import ethereum


arg_parser = argparse.ArgumentParser(description='register Ethereum')
arg_parser.add_argument('--channel', help='Channel ID', required=True)
arg_parser.add_argument('--measurement', help='measuement', required=True)
args = arg_parser.parse_args()
print(args)

channel_id = args.channel
measurement = args.measurement


# Ethereumへのアクセス情報取得
s = db.DB()
eth_rec = s.select(db.DsEthereum, "Ethereum")
print("eth_rec=",eth_rec)
if eth_rec != None:
    url = "http://" + eth_rec.address + ":" + str(eth_rec.port)
    account = eth_rec.account
    password = eth_rec.password
    private_key = eth_rec.private_key
else:
    url = "http://192.168.3.3:8545"
    account = "0x70f9e0445a572d62eabf6d6669f69283558d7e2f"
    password = "dataprovider"
    private_key = "c2f7b10487844a8d0f708a2397a63e0aa2b2695351775fe5548557bc71280e28"



print("url = ", url)
print("account = ", account)
print("password = ", password)
print("private_key = ", private_key)

    
eth = ethereum.Ethereum(url, account, password, private_key)

# コントラクト設定
func_rec = s.select(db.DsFunction, "MyDataStore")
eth.set_contract(func_rec.address, func_rec.abi)

res = eth.get_data_number(channel_id, measurement)
print(res)

res = eth.get_data(channel_id, measurement, 0, 100, None)
print(res)
