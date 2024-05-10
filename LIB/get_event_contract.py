#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime

from LIB import db
from LIB import ethereum

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
    
eth = ethereum.Ethereum(url, account, password, private_key)

# コントラクト設定
event_id = "AUDIT"
func_id = "MyAuditEvent"
func_rec = s.select(db.DsFunction, func_id)
eth.set_event_contract(func_id, func_rec.address, func_rec.abi)

params = {"name":event_id}
res = eth.get_event_contract(func_id, params)
print(res)
