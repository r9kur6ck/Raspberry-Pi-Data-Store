#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from APP import channel

DEBUG = False # True


class Channel(BaseModel):
    id: str
    name: Optional[str] = None
    owner: Optional[str] = None
    

router = APIRouter(
    prefix="/channel",
    tags=["channel"],
)


@router.get("/")
async def channel_list():
    print("channel_list")

    """
    DBを検索してチャネル一覧を取得して返す、結果はid,nameのリスト
    """

    c_list = channel.list_channel()
    
    return {"Status": "OK", "channel":c_list}

@router.post("/")
async def create_channel(ch: Channel):
    print("create_channel", ch)
    """
    ユーザを登録する
    リクエストボディでid,name,ownerをもらう
    """

    res = channel.create_channel(ch.id, ch.name, ch.owner)
    
    return {"Status": "OK"}

@router.get("/{channel_id}", response_model=Channel)
async def get_channel(channel_id: str):
    print("get_channelt", channel_id)
    """
    channel_idでチャネルを検索して情報を返す
    """
    res = channel.get_channel(channel_id)
    c = None
    if res:
        c = Channel(id=res.id, name=res.name, owner=res.owner)
    
    return c


@router.delete("/{channel_id}")
async def delete_channel(channel_id: str):
    print("delete_channel", channel_id)

    res = channel.delete_channel(channel_id)
    
    return {"Status": "OK"}
