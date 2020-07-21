#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：pubUtil.py
# 功能描述：公共工具包
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20200706
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python pubUtil.py
# ***************************************************************************

import os
import sys
import time
import datetime


# 获取当天日期字符串
def get_today():
    today = datetime.date.today()

    today = str(today + datetime.timedelta(days=0)).replace('-', '')

    return today


# 获取当天前一天日期字符串
def get_pre_day():
    today = datetime.date.today()

    pre_day = str(today + datetime.timedelta(days=-1)).replace('-', '')

    return pre_day


# 获取当月前一个月
def get_pre_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    pre_month = str(last_month.strftime("%Y%m"))

    return pre_month


# 获取主机名，判断当前代码运行主机
def get_hostname():
    hostname_sh = 'hostname -i'
    hostname_str = os.popen(hostname_sh).readline().replace('\n', '')
    return hostname_str


# 清理tb*文件
def clear_tb_file():
    clear_sh = 'rm ./tb*.txt'
    os.popen(clear_sh)


get_pre_day()
get_pre_month()
get_today()
