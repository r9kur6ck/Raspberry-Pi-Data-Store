#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import os
import datetime
import uvicorn

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from routers import channel_rt, data_rt, file_rt, bchain_data_rt, nft_rt
from APP import event


IP="0.0.0.0"
PORT=8000


# 初期化
app = FastAPI()

# イベント処理ミドルウェア
evt = event.Event()
@app.middleware("http")
async def process_event(request: Request, call_next):
    print("START process_event", request)

    # 処理前イベント
    res = evt.pre_event(request)

    # NFT対応の特殊処理
    if 'MyPhotoNFT' in res:
        r = res['MyPhotoNFT']
        print(r)

        if r['status'] != 0:
            print("NO call_next")
            return JSONResponse(content=r['data'], status_code=403)

    # 処理実態
    response = await call_next(request)

    # 処理後イベント
    res = evt.post_event(request, response)

    print("END process_event", response)
    
    return response


# CORS対応
origins = [
    "http://localhost",
    "http://localhost:"+str(PORT),
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API処理)の登録
app.include_router(data_rt.router)
app.include_router(channel_rt.router)
app.include_router(bchain_data_rt.router)
app.include_router(file_rt.router)
app.include_router(nft_rt.router)

   
# システム情報
class SystemInfo(BaseModel):
    System = "My Data Server"
    Version = "1.0b"
    Release = "2022/08/31"

@app.get("/info", response_model=SystemInfo)
def read_root():
    return SystemInfo()

# 画面表示用の静的ファイル
top_path = os.getenv('MYDATASERVER_TOP')
if top_path == None : top_path = ""
app.mount("/dataserver", StaticFiles(directory=top_path+"html"), name="html")

@app.get("/")
async def read_root():
    return {"My Data Server"}

if __name__ == "__main__":
    uvicorn.run(app, host=IP, port=PORT)
