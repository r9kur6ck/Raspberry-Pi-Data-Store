#!/bin/bash

export PYTHONPATH="`pwd`:`pwd`/LIB:`pwd`/APP:$PYTHONPATH"
export MYDATASERVER_APP_CONFIG_PATH=`pwd`/APP
export MYDATASERVER_LIB_CONFIG_PATH=`pwd`/LIB

./mydata_server.py
