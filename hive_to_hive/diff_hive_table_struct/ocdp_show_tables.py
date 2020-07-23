#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：ocdp_show_tables.py
# 功能描述：迁移Hive表
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20200617
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python ocdp_show_tables.py
# ***************************************************************************

import os
import sys

# 功能
# 1.show_tables到列表变量
# 2.过滤符号排序，输出到文件

# 连接ocdp集群
excute_ocdp_sh = "beeline -u 'jdbc:hive2://hua-dlzx2-a0202:10000/csap' -n ocdp -p 1q2w1q@W -e "


def show_tables():
    show_tables_sql = 'show tables;'
    show_tables_sh = excute_ocdp_sh + '\"' + show_tables_sql + '\"'

    print show_tables_sh

show_tables()