#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json

from fastapi import APIRouter, File
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Union, List, Optional

from LIB import db
from LIB import storage

DEBUG = False # True

router = APIRouter(
    prefix="/file",
    tags=["file"],
)

# MinIOへのアクセス情報取得
s = db.DB()
st_rec = s.select(db.DsStorage, "MinIO")
if DEBUG : print("st_rec=",st_rec)
if st_rec != None:
    url = "http://" + st_rec.address + ":" + str(st_rec.port)
    access_key_id = st_rec.access_key_id
    secret_access_key = st_rec.secret_access_key
else:
    url = "http://localhost:9000"
    access_key_id = "admin"
    secret_access_key = "admin001"

if DEBUG:
    print("url = ", url)
    print("access_key_id = ", access_key_id)
    print("secret_access_key = ", secret_access_key)

st = storage.Storage(url, access_key_id, secret_access_key)

"""
Storage
"""
@router.get("/{channel_id}")
async def list_file(channel_id: str):
    print("read_file", channel_id)
    """
    データを検索
    """
    res = st.list_file(channel_id)
    
    return {"Status": "OK", "OBJECTS":res}

@router.get("/{channel_id}/{filename}")
async def get_file(channel_id: str, filename: str, need_token: bool = False, account: str = None):
    print("get_file", channel_id, filename, need_token, account)
    """
    データを検索
    """
    d = st.get_file(channel_id, filename)

    res = Response(content=d, status_code=200)
    
    return res

@router.post("/{channel_id}/{filename}")
async def put_file(channel_id: str, filename: str, file: bytes = File(...)):
    print("put_file", channel_id, filename)

    res = st.put_file(channel_id, filename, file)

    return {"Status": "OK", "RESULT": res}


@router.delete("/{channel_id}/{filename}")
async def delete_file(channel_id: str, filename: str):
    print("delete_file", channel_id, filename)

    res = st.delete_file(channel_id, filename)
    
    return {"Status": "OK", "RESULT": res}



