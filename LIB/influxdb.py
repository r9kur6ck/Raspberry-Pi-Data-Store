#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import json
import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

DEBUG = False # True

# InfluxDBにアクセスするライブラリ

class InfluxDB:
    # コンストラクタ
    def __init__(self, url, org, token):
        print("Constructor of InfluxDB")
        self.url = url
        self.organization = org
        self.api_token = token
        # InfluxDBへ接続するクライアント作成
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )
        # Bucket API呼び出し準備
        self.bucket_api = self.client.buckets_api()
        # 検索API呼び出し準備
        self.query_api = self.client.query_api()
        # 書き込みAPI呼び出し準備
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    # デストラクタ
    def __del__(self):
        print("Destructor of InfluxDB")


    # Bucket作成
    def create_bucket(self, bucket_name):
        print("create_bucket")
        # bucket存在確認
        bkt = self.bucket_api.find_bucket_by_name(bucket_name=bucket_name)
        if DEBUG : print(bkt)

        # 存在しなければbucket作成
        if bkt == None:
            print("bucket " + bucket_name + " is Not exist.")
            self.bucket_api.create_bucket(bucket_name=bucket_name, org=self.organization)


    # Bucket削除
    def delete_bucket(self, bucket_name):
        print("delete_bucket")
        # bucket存在確認
        bkt = self.bucket_api.find_bucket_by_name(bucket_name=bucket_name)
        if DEBUG : print(bkt)

        # 存在すればbucket削除
        if bkt != None:
            print("bucket " + bucket_name + " exist.")
            self.bucket_api.delete_bucket(bkt)

    def json2point(self, measurement, data_json):
        data =json.loads(data_json)
        if DEBUG : print(data)

        # tag
        p = influxdb_client.Point(measurement).tag("source", data['source'])

        # timestamp
        if 'timestamp' in data:
            if data['timestamp']:
                p.time(datetime.datetime.strptime(data['timestamp'], "%Y%m%d%H%M%S"))

        # field
        r = []
        it = None
        for d in data['data']:
            if DEBUG : print(d)
            for k,v in d.items():
                if DEBUG : print(k,v)
                p.field(k, v)

        return p


    # データ保存
    """
    データは以下のJSON形式でもらう。timestampはUTCで指定。
    {
	"timestamp":,
	"source":,
	"data":[]
    }
    """
    def put_data(self, bucket_name, measurement, data):
        print("put_data:", measurement, data)
        r = self.json2point(measurement, data)
        self.write_api.write(bucket=bucket_name, org=self.organization, record=r)


    # データ取得
    def get_data(self, bucket_name, measurement, start=None, stop=None, source=None):
        print("get_data:",bucket_name, measurement, start, stop)
        # 検索
        """
        start,stopはUTCで指定。
        """
        range = ''
        if start != None:
            range = '|> range(start: ' + str(int(datetime.datetime.strptime(start, "%Y%m%d%H%M%S").replace(tzinfo=datetime.timezone.utc).timestamp()))
        else:
            range = '|> range(start: 0'

        if stop != None:
            range = range + ', stop: ' + str(int(datetime.datetime.strptime(stop, "%Y%m%d%H%M%S").replace(tzinfo=datetime.timezone.utc).timestamp())) + ')'
        else:
            range = range + ', stop: now())'

        query = ' from(bucket:"' + bucket_name + '") ' + range
        
        if measurement:
            query = query + '|> filter(fn:(r) => r._measurement == "' + measurement + '")'
            
        if source:
            query = query + '|> filter(fn:(r) => r.source == "' + source + '")'
        
            
        if DEBUG : print(query)

        result = self.query_api.query(org=self.organization, query=query)

        if DEBUG:
            for table in result:
                #print(table)
                for record in table.records:
                    print(record.get_measurement())
                    print(record.get_time())
                    print(record.get_field())
                    print(record.get_value())
                    for v in record.values:
                        print(v)
                        print(record[v])


        """
        結果は、以下の形式で返す
        {
    		"start":"",
    		"stop":"",
    		"bucket":
		data:[{"timestamp":"xxx","measurement":"mmm", "source":"xxx", フィールド:値},...]
    	}

        """
        res = {"start":start,"stop":stop, "bucket":bucket_name}
        dp = []
        for table in result:
            for record in table.records:
                if DEBUG: print("RECORD: ",record)
                d = {"timestamp":record.get_time().strftime('%Y%m%d%H%M%S'), "measurement":record.get_measurement(), "source":record['source'], record.get_field():record.get_value()}
                if DEBUG : print(d)
                dp.append(d)

        res['data'] = dp
        if DEBUG : print(res)

        return res
