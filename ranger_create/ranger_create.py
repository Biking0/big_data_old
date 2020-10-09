#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：ranger_create.py
# 功能描述：31省策略生成
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20201009
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python ranger_create.py
# ***************************************************************************

import os
import sys
import json
import time
import requests

import config

url = "http://172.19.168.231:6080/service/public/v2/api/policy"

headers = {
    'X-XSRF-HEADER': "valid",
    'Content-Type': "application/json",
    # 'Authorization': "Basic YWRtaW46MXEydyFRQFc=",
    'Cache-Control': "no-cache",
    # 'Postman-Token': "569270c0-c554-424a-9260-7cb22b3dfdd6"
    'Cookie':""
    }

response = requests.request("POST", url, data=config.policy_json, headers=headers)

print response.text
print response.status_code


