#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import json
import datetime
import argparse

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

DEBUG = False # True

# 設定ファイルを読み込む
config_path = os.getenv('MYDATASERVER_LIB_CONFIG_PATH')
if config_path == None:
    config_path = '.'
fp = open(config_path + '/config.json')
config = json.load(fp)
fp.close()
if DEBUG : print(config)

db_user = config['metadb']['USER']
db_pass = config['metadb']['PASS']
db_name = config['metadb']['DB']
db_host = config['metadb']['HOST']
db_port = config['metadb']['PORT']

# MySQLに接続
from sqlalchemy.engine.url import URL
db_url = URL.create(
    drivername="mysql",
    username=db_user,
    password=db_pass,
    host=db_host,
    port=db_port,
    database=db_name,
    query = {"charset": 'utf8'},
)

engine = create_engine(db_url)


# データモデル
Base = declarative_base()
Base.metadata.bind = engine

## channel
class DsChannel(Base):
    __tablename__ = "ds_channel"
    __table_args__ = {"autoload":True}

if DEBUG : print(DsChannel.__dict__)

## InfluxDB
class DsInfluxDB(Base):
    __tablename__ = "ds_influxdb"
    __table_args__ = {"autoload":True}

if DEBUG : print(DsInfluxDB.__dict__)


## Storage
class DsStorage(Base):
    __tablename__ = "ds_storage"
    __table_args__ = {"autoload":True}

if DEBUG : print(DsStorage.__dict__)

## Ethereum
class DsEthereum(Base):
    __tablename__ = "ds_ethereum"
    __table_args__ = {"autoload":True}

if DEBUG : print(DsEthereum.__dict__)


## function
class DsFunction(Base):
    __tablename__ = "ds_function"
    __table_args__ = {"autoload":True}

if DEBUG : print(DsFunction.__dict__)

## event
class DsEvent(Base):
    __tablename__ = "ds_event"
    __table_args__ = {"autoload":True}

if DEBUG : print(DsEvent.__dict__)


class DB:
    def __init__(self):
        print("Constructor of DB")
        # DB接続
        from sqlalchemy.orm import sessionmaker
        SessionClass = sessionmaker(engine)  
        self.session = SessionClass()

    def __del__(self):
        print("Destructor of DB")
        self.db_disconnect()

    # DB切断
    def db_disconnect(self):
        print("db_disconnect")
        self.session.close()

    # 全レコード取得
    def list(self, tbl):
        print("list", tbl)
        r = self.session.query(tbl).all()
        if DEBUG : print(r)
        return r

    # レコード追加
    def insert(self, rec):
        print("insert", rec)
        try:
            self.session.add(rec)
            self.session.commit()
        except Exception as e:
            print(e)
        finally:
            pass
    
    # レコード取得
    def select(self, tbl, id):
        print("select")
        r  = self.session.query(tbl).filter(tbl.id == id).first()
        if DEBUG : print(r)
        return r
    
    # レコード削除
    def delete(self, rec):
        print("delete", rec)
        self.session.delete(rec)
        self.session.commit()

    # レコード更新
    def update(self, rec):
        print("update", rec)
        self.session.commit()


