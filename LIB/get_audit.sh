#!/bin/bash

TOP=$HOME/Desktop/tsuyo/CQ/mydata_server/
export PYTHONPATH="$TOP:%TOP/LIB:$TOP/APP:$PYTHONPATH"
export MYDATASERVER_APP_CONFIG_PATH=$TOP/APP
export MYDATASERVER_LIB_CONFIG_PATH=$TOP/LIB

./get_event_contract.py

