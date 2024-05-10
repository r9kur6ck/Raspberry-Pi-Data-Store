#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import requests
import json

config = {}

# 初期化
api_url = "http://192.168.3.3:8000"
def set_url(url):
    global api_url
    api_url = url
    return



# データ保存
def send_data(channel, measurement, source, data):
    try:
        url = api_url + "/data/" + channel + "/" + measurement
        data = {"source":source, "data":data}
        resp = requests.post(url, json=data)
        r = resp.status_code
    except Exception as e:
        r = 500
        print(sys._getframe().f_code.co_name+":post failed")
        print(e)

    return r


# ファイル保存
def send_file(channel, name, path):
    try:
        url = api_url + "/data/" + channel
        resp = requests.post(url, files={'file':(path, open(path, 'rb'))}, data={'name': name})
        r = resp.status_code

    except Exception as e:
        r = 500
        print(sys._getframe().f_code.co_name+":post failed")
        print(e)

    return r



if __name__ == '__main__':

    load_config('./config.json')
    set_url("http://" + config['server'] + ":" + str(config['port']))
    data = [{"temperature":38.0},{"pressure":1000},{"humidity":90}]
    send_data("mybucket","dev1m", "raspi", data)
    send_file("mybucket", "myfile", "/tmp/test.file")


