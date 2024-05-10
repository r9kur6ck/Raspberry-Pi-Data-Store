#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import sys
import json
import libdata
import traceback
import BME280.bme280_sample as MySensor

# configファイルのロード
def load_config(path='./config.json'):
    global config
    f = open(path, 'r')
    config = json.load(f)
    f.close()
    print(config)

load_config('./config.json')
libdata.set_url("http://" + config['server'] + ":" + str(config['port']))

# チャネル(bucket)
CHANNEL = config['channel']

# measurement
MEASUREMENT = config['measurement']

# データ送信間隔
INTERVAL = 60

# データ取得・送信を無限ループ
while True:
    try:
        # データを読み込む                                                                                                                     
        data = MySensor.get_data()
        print(data)

        # データを保存                                                                                                                         
        libdata.send_data(CHANNEL, MEASUREMENT, "raspi", data)

    except KeyboardInterrupt:
        break
    except:
        print(traceback.format_exc())
        pass


    # 指定時間待ち                                                                                                                                 
    time.sleep(INTERVAL)
        

