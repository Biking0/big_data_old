#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：copy_hive_table.py
# 功能描述：迁移Hive表
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20200617
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python copy_hive_table.py
# ***************************************************************************

import os
import sys

# 常量定义

# 连接旧集群
old_hive = "beeline -u 'jdbc:hive2://192.168.190.88:10000/csap' -e 'show create table "

# 连接新集群
new_hive = "beeline -u 'jdbc:hive2://172.19.168.101:10000/default' -n ocdp -p 1q2w1q@W -e \" "


# 获取表结构，封装完整hive创建语句
def get_table_struct(table_name):
    table_struct_sh = old_hive + table_name + '\' > test1.txt'

    table_struct_str = os.popen(table_struct_sh).readlines()
    f = open('table_struct.txt', 'w')
    f.write(str(table_struct_str))
    f.close()

    print table_struct_sh
    print table_struct_str

    data = ''
    with open("./test1.txt", "r") as f:  # 打开文件
        data = f.read()  # 读取文件
        if 'LOCATION' in data:
            print(data)

    print '###########'
    data = data.replace('+', '').replace('-', '').replace('+', '').replace('createtab_stmt', '').replace('|',
                                                                                                         '').replace(
        '\'\'', '\'|\'').replace('\n', '').replace('  ', '').replace('`', '')
    print data

    local_localtion = data.find('LOCATION')
    print local_localtion
    result = data[0:local_localtion]
    print '***********'
    print result

    create_table(result)


# 新集群建表操作
def create_table(create_table_sql):
    create_table_sh = new_hive + create_table_sql + '\"'

    print create_table_sh


get_table_struct('tb_si_cu_voma_limit_whitelist_day')
