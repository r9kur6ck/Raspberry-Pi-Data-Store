#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union, List, Optional

from LIB import db
from LIB import ethereum

DEBUG = False # True

router = APIRouter(
    prefix="/bchain_data",
    tags=["bchain_data"],
)

# Ethereumへのアクセス情報取得
s = db.DB()
eth_rec = s.select(db.DsEthereum, "Ethereum")
if DEBUG : print("eth_rec=",eth_rec)
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



if DEBUG:
    print("url = ", url)
    print("account = ", account)
    print("password = ", password)
    print("private_key = ", private_key)

eth = ethereum.Ethereum(url, account, password, private_key)

# コントラクト設定
func_rec = s.select(db.DsFunction, "MyDataStore")
if DEBUG : print("func_rec = ", func_rec)
if func_rec:
    eth.set_contract(func_rec.address, func_rec.abi)

"""
Ethereum
"""

class DList(BaseModel):
    timestamp: Optional[str]
    source: str
    data: List[dict]

@router.get("/")
async def get_data(channel_id: str, measurement: str, start: int = 0, stop: int = 100):
    print("get_data", channel_id, measurement, start, stop)
    """
    データを取得する
    """
    res = eth.get_data(channel_id, measurement, start, stop, None)
    if DEBUG : print(res)

    return {"Status": "OK", "data":res}

@router.get("/length")
async def get_data_number(channel_id: str, measurement: str):
    print("get_data_number", channel_id, measurement)
    """
    データ数を取得する
    """
    res = eth.get_data_number(channel_id, measurement)
    if DEBUG : print(res)

    return {"Status": "OK", "Result":res}


@router.post("/{channel_id}/{measurement}")
async def put_data(channel_id: str, measurement: str, data : DList):
    print("put_data:", channel_id, measurement, data)
    """
    データを登録する
    """
    eth.put_data(channel_id, measurement, data.json())
    return {"Status": "OK"}


