import json
import os

import time

from search_engines.utils.log import log
from search_engines.utils.db import db

def get_root_path():
    root_path = os.path.dirname(os.path.realpath(__file__))
    return root_path

# 获取配置信息
def config(name) :
    try:
        config_path = get_root_path() + '/config/app.json'
        with open(config_path) as f:
            res = f.read()
            res = res.encode('utf-8').decode('utf8')
            res = json.loads(res)
            return res.get(name)
    except Exception as e:
        raise Exception (e)

def db_Model():
    db_model = db(config('mysql'))
    return db_model

def add_log(content):
    try:
        print(content)
        print(888)
        logModel = log()
        dir_name = get_root_path() + '/log/' + time.strftime('%Y-%m',time.localtime())
        if os.path.exists(dir_name) == False :
            os.mkdir(dir_name)
        date = time.strftime('%Y-%m-%d',time.localtime())
        file_name = date+'.log'
        logModel.add_log(dir_name + '/' + file_name,content)
    except Exception as e:
        print(e)


