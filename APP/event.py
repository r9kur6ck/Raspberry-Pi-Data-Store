#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json

from LIB import db
from LIB import ethereum

DEBUG = False # True


class Event:
    # コンストラクタ
    def __init__(self):
        print("Constructor of Event")
        self.event_list = {}
        self.eth_rec = None

        s = db.DB()
        # Ethereumへの接続設定
        eth_rec = s.select(db.DsEthereum, "Ethereum")

        if eth_rec:
            url = "http://" + eth_rec.address + ":" + str(eth_rec.port)
            account = eth_rec.account
            password = eth_rec.password
            private_key = eth_rec.private_key
            self.eth = ethereum.Ethereum(url, account, password, private_key)

        # イベント登録
        self.events = s.list(db.DsEvent)
        for rec in self.events:
            if DEBUG : print(rec.id, rec.name, rec.func_id)

            rec.key = rec.method + rec.url
            rec.call = self.call_contract

            # Function情報の取得
            rec.func = s.select(db.DsFunction, rec.func_id)
            if DEBUG : print(rec.func)
            if rec.func:
                # コントラクトの実行準備
                self.eth.set_event_contract(rec.func_id, rec.func.address, rec.func.abi)

        if DEBUG:
            for rec in self.events:
                print(rec,id,rec.method,rec.url,rec.call,rec.func)
        

    # デストラクタ
    def __del__(self):
        print("Destructor of Event")


    # コントラクト実行
    def call_contract(self, evt, request, response):
        print("call_contract", evt, request, response)
        print("event = ", evt.id, evt.name)

        account = None
        if evt.func:
            params = {}
            params['name'] = evt.id
            params['url'] = request.url.path
            params['method'] = request.method
            params['user'] = request.client.host

            if 'user' in request.query_params:
                params['user'] = request.query_params['user']
            if 'account' in request.query_params:
                params['account'] = request.query_params['account'].lower()
                account = params['account']
            if 'need_token' in request.query_params:
                params['need_token'] = request.query_params['need_token']

            print("PARAM for eth.put_event_contract:", evt.func_id, params)
            self.eth.put_event_contract(evt.func_id, account, params)

            res = {}
            if evt.func_id == 'MyPhotoNFT' and 'need_token' in params and params['need_token'].lower() == 'true':	# for NFT
                params["mode"] = "owned"	# urlで指定されたファイルのトークンを持っているか確認する指示
                print("PARAM for eth.get_event_contract:", evt.func_id, params)
                r = self.eth.get_event_contract(evt.func_id, params)
                res = json.loads(r);

            return res


    # イベント実行チェック
    def check_event(self, request, check_point):
        # リクエスと情報取り出し
        method = request.method
        path = request.url.path
        user = request.client.host
        print(method, path, user)

        # 実行するイベントを探す
        event_list = []
        for evt in self.events:
            if DEBUG : print(evt.id, evt.method, evt.url, method, path, check_point)
            if check_point.lower() == 'pre' and evt.act_pre != True:
                continue
            elif check_point.lower() == 'post' and evt.act_post != True:
                continue
            
            if evt.method != '*' and evt.method != method:
                continue
            if evt.url != '*' and path.startswith(evt.url) != True:
                continue

            if DEBUG :print(evt.id, "in event list")

            event_list.append(evt)

        return event_list
        

    # 処理前イベント
    def pre_event(self, request):
        if DEBUG : print("pre_event", request)

        # 実行イベントを探す
        event_list = self.check_event(request, 'pre')
        if DEBUG : print(event_list)

        # イベント実行
        res = {}
        for evt in event_list:
            r = evt.call(evt, request, None)
            if r : res[evt.id] = r

        return res


    # 処理後イベント
    def post_event(self, request, response):
        if DEBUG : print("post_event", request, response)

        # 実行イベントを探す
        event_list = self.check_event(request, 'post')
        if DEBUG : print(event_list)

        # イベント実行
        res = {}
        for evt in event_list:
            r = evt.call(evt, request, response)
            if r : res[evt.id] = r

        return res



    


