#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime

from LIB import db
from LIB import influxdb
from LIB import storage

DEBUG = False # True

## 作成
def create_channel(id, name, owner):
    print("create_channel:" + name)

    s = db.DB()

    # チャネル存在確認
    c = s.select(db.DsChannel, id)
    print(c)
    if c != None:
        print("Channel " + id + " is exists.")
        return None
    
    # チャネル登録
    c = db.DsChannel(id=id, name=name, owner=owner)
    s.insert(c)
    print(s)
    
    # InfluxDBにBucketを作成する
    idb_rec = s.select(db.DsInfluxDB, "InfluxDB")
    print("idb_rec=",idb_rec)
    if idb_rec != None:
        url = "http://" + idb_rec.address + ":" + str(idb_rec.port)
        print("url = " + url)
        idb = influxdb.InfluxDB(url, idb_rec.organization, idb_rec.token)
        print(idb)
        idb.create_bucket(id)
        
    # Storage(MinIO)にBucketを作成する
    st_rec = s.select(db.DsStorage, "MinIO")
    print("st_rec=",st_rec)
    if st_rec != None:
        url = "http://" + st_rec.address + ":" + str(st_rec.port)
        print("url = " + url)
        st = storage.Storage(url, st_rec.access_key_id, st_rec.secret_access_key)
        print(st)
        st.create_bucket(id)

    return c


## 削除
def delete_channel(id):
    print("delete_channel:" + id)
    s = db.DB()
    c = s.select(db.DsChannel, id)
    print(c)
    if c == None:
        print("Channel " + id + " is NOT exists.")
        return None
    s.delete(c)

    # InfluxDBのBucketを削除する
    idb_rec = s.select(db.DsInfluxDB, "InfluxDB")
    print("idb_rec=",idb_rec)
    if idb_rec != None:
        url = "http://" + idb_rec.address + ":" + str(idb_rec.port)
        print("url = " + url)
        idb = influxdb.InfluxDB(url, idb_rec.organization, idb_rec.token)
        idb.delete_bucket(id)

    # Storage(MinIO)のBucketを削除する
    st_rec = s.select(db.DsStorage, "MinIO")
    print("st_rec=",st_rec)
    if st_rec != None:
        url = "http://" + st_rec.address + ":" + str(st_rec.port)
        print("url = " + url)
        st = storage.Storage(url, st_rec.access_key_id, st_rec.secret_access_key)
        print(st)
        st.delete_bucket(id)
    
    
## 一覧
def list_channel():
    print("list_channel")
    s = db.DB()
    channel = s.list(db.DsChannel)
    for c in channel:
        print(c.name,c.id)

    return channel
    

## 情報取得
def get_channel(id):
    print("get_channel")
    s = db.DB()
    c = s.select(db.DsChannel, id)
    print(c)
    return c


""" 
create_channel("TTT", "TT name2", "tsuyo2")
create_channel("TTT2", "TT name3", "tsuyo3")

get_channel("TTT22")

channel = list_channel()
for c in channel:
    print("L", c.id,c.name,c.owner)

change_channel_name("TTT", "UPDATED NAE")
channel = list_channel()
for c in channel:
    print("L2", c.id,c.name,c.owner)
delete_channel("TTT")
channel = list_channel()
for c in channel:
    print("L3", c.id,c.name,c.owner)

delete_channel("TTT2")
"""
