#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime

import boto3

DEBUG = False # True 

# Storage(MinIO)にアクセスするライブラリ

class Storage:
    # コンストラクタ
    def __init__(self, url, key_id, access_key):
        print("Constructor of Storage")
        self.url = url
        self.access_key_id = key_id
        self.secret_access_key = access_key
        # S3への接続
        self.c = boto3.resource(
            service_name = 's3',
            use_ssl=False,
            endpoint_url=url,
            aws_access_key_id=key_id,
            aws_secret_access_key=access_key)

    # デストラクタ
    def __del__(self):
        print("Destructor of Storage")


    # バケット名補正
    def bucket_name(self, bucket_name):
        # 小文字で3文字以上
        if len(bucket_name) < 3:
            print("at least 3 charactors.")
            return None
        
        return bucket_name.lower()
    

    # バケット作成
    def create_bucket(self, bucket_name):
        print("create_bucket: " + bucket_name)
        name = self.bucket_name(bucket_name)
        if name == None:
            print("Invalid name")
            return None
        bkt = self.c.Bucket(name)
        res = bkt.create()
        return res
        

    # バケット削除
    def delete_bucket(self, bucket_name):
        print("delete_bucket")
        name = self.bucket_name(bucket_name)
        if name == None:
            print("Invalid name")
            return None
        bkt = self.c.Bucket(name)
        res = bkt.delete()
        return res
        

    # ファイル保存
    def put_file(self, bucket_name, file_name, file):
        print("put_file", bucket_name, file_name)

        obj = self.c.Object(bucket_name, file_name)
        res = obj.put(Body=file)
        return res

        
    # ファイル取り出し
    def get_file(self, bucket_name, file_name, path=None):
        print("get_file", bucket_name, file_name)
        try:
            obj = self.c.Object(bucket_name, file_name)
            if path:
                res = obj.download_file(path)
                return res
            else:
                res = obj.get()
                f = res['Body'].read()
                return f
        except:
            return None

    # ファイル削除
    def delete_file(self, bucket_name, file_name):
        print("delete_file", bucket_name, file_name)
        obj = self.c.Object(bucket_name, file_name)
        res = obj.delete()
        print(res)
        return res
        

    # ファイル一覧
    def list_file(self, bucket_name):
        print("list_file")
        bkt = self.c.Bucket(bucket_name)
        res = []
        for obj in bkt.objects.all():
            res.append(obj.key)
            
        return res




