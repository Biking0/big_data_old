#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：get_dataos_database.py
# 功能描述：获取sy数据源信息
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20200922
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python get_dataos_database.py
# ***************************************************************************

import os
import sys
import conn_dataos_db
import json


# 获取数据源信息，获取列表类型数据
def get_info():
    get_info_sql = "select ds_name as name ,ds_acct as username,md5(ds_auth) as password,ds_conf from  dacp_meta_datasource "

    result_list = conn_dataos_db.select(get_info_sql)

    data_list = []
    # 将元组转为list
    for i in result_list:
        data_list.append(list(i))

    insert_info(data_list)


# 插入本地库
def insert_info(result_list):
    for i in result_list:
        # print i

        json_data = json.loads(i[3])

        if json_data['dsType']=='sftp':


        if json_data['dsType'] != 'mysql':
            print i

            break

        # break


get_info()
