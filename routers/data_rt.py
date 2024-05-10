#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union, List, Optional

from LIB import db
from LIB import influxdb

DEBUG = False # True

router = APIRouter(
    prefix="/data",
    tags=["data"],
)

# InfluxDBへのアクセス情報取得
s = db.DB()
idb_rec = s.select(db.DsInfluxDB, "InfluxDB")
if DEBUG : print("idb_rec=",idb_rec)
if idb_rec != None:
    url = "http://" + idb_rec.address + ":" + str(idb_rec.port)
    organization = idb_rec.organization
    token = idb_rec.token
else:
    url = "http://localhost:8086"
    organization = "MyDataServer"
    token = ""

if DEBUG:
    print("url = ", url)
    print("organization = ", organization)
    print("token = ", token)
    
idb = influxdb.InfluxDB(url, organization, token)


"""
InfluxDB
"""
class DList(BaseModel):
    timestamp: Optional[str]
    source: str
    data: List[dict]

@router.get("/")
async def get_data(channel_id: str, measurement: Union[str, None] = None, start: Union[str, None] = None, stop: Union[str, None] = None):
    print("get_data", channel_id, measurement, start, stop)
    """
    データを取得する
    """
    res = idb.get_data(channel_id, measurement, start, stop, None)
    if DEBUG : print(res)

    return {"Status": "OK", "data":res}



@router.post("/{channel_id}/{measurement}")
async def put_data(channel_id: str, measurement: str, data : DList):
    print("put_data:", channel_id, measurement, data)
    """
    データを登録する
    """
    idb.put_data(channel_id, measurement, data.json())
    return {"Status": "OK"}


