#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：hive_data_check.py
# 功能描述：hive表数据稽核
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20200624
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python hive_data_check.py
# ***************************************************************************

# 1. 分析hive库表结构，获取int字段，将所有表存到列表里
# 2. 构造数据稽核sql，分析周期（分区），sum字段
# 3. 抽取两个库的表文件到本地，进行对比

import os
import sys
import time
import datetime


# 生成desc表结构文件
def create_desc(table_name):
    # 生产环境
    # desc_sh = "beeline -u 'jdbc:hive2://192.168.190.88:10000/csap' -n hive -p %Usbr7mx -e 'desc  " + line + ' \' > ./desc.txt'

    # 测试环境
    desc_sh = "beeline -u 'jdbc:hive2://172.22.248.19:10000/default' -n csap -p @WSX2wsx -e 'desc  " + table_name + ' \' > ./' + table_name + '.txt'

    print desc_sh
    os.popen(desc_sh).readlines()
    desc_parser(table_name)


# 解析desc表结构
def desc_parser(table_name):
    desc_list = open('./' + table_name + '.txt', 'r').readlines()

    result_list = []

    for i in range(len(desc_list)):

        # 忽略其他行
        if desc_list[i][0] == '+':
            continue
        line_list = desc_list[i].strip().replace(' ', '').replace('\t', '').replace('\n', '').split('|')

        # 忽略表头
        if line_list[1] == 'col_name' or 'NULL' in line_list[1]:
            continue

        if 'Partition' not in line_list[1]:
            print line_list[1], line_list[2], line_list[3],

            # 封装表结构int字段
            if line_list[2] == 'int':
                result_list.append(line_list[1])

            # print '#'

        # 检测分区数量
        if desc_list[i][2] == '#':
            check_partition_list = desc_list[i].split(' ')

            if check_partition_list[2] == 'Partition':
                print '### 分区键'

                for j in range(i + 1, len(desc_list)):

                    # 忽略其他行
                    if desc_list[j][0] == '+':
                        continue

                    if desc_list[j][3] == ' ':
                        continue
                    print desc_list[j].split(' ')[1]

                # 重要
                break

            print desc_list[i]
            continue
        #

        # break

    # 封装表结构int字段
    print 'int colume:'
    print result_list

    # 分区检测
    check_partition(table_name)

    # 创建查询sql
    create_sql(table_name, result_list)


# 分区检测，构造分区，根据需要稽核的时间段，循环生成相应的分区，判断是否为分区表,line(table_name)
def check_partition(line):
    desc_list = open('./' + line + '.txt', 'r').readlines()

    result_list = []
    partition_list = []

    for i in range(len(desc_list)):

        # 忽略其他行
        if desc_list[i][0] == '+':
            continue
        line_list = desc_list[i].strip().replace(' ', '').replace('\t', '').replace('\n', '').split('|')

        # 忽略表头
        if line_list[1] == 'col_name' or 'NULL' in line_list[1]:
            continue

        if 'Partition' not in line_list[1]:
            print line_list[1], line_list[2], line_list[3],
            print '#'

        # 检测分区数量
        if desc_list[i][2] == '#':
            check_partition_list = desc_list[i].split(' ')

            if check_partition_list[2] == 'Partition':
                print '### 分区键'

                # partition_list = []
                for j in range(i + 1, len(desc_list)):

                    # 忽略其他行
                    if desc_list[j][0] == '+':
                        continue

                    if desc_list[j][3] == ' ':
                        continue
                    partition_key = desc_list[j].split(' ')[1]
                    print partition_key
                    partition_list.append(partition_key)

                if len(partition_list) > 1:
                    print '### 多个分区', line, partition_list
                    # check_result = open('/home/hive/hyn/hive_to_hive/check_result.txt', 'a+')
                    # check_result.write(line + ' ' + str(partition_list) + '\n')
                    # check_result.close()

                else:
                    print '### 1个分区', line, partition_list
                    # check_result = open('/home/hive/hyn/hive_to_hive/desc/check_result.txt', 'a+')
                    # check_result.write(line + ' ' + str(partition_list) + '\n')
                    # check_result.close()
            else:
                print line, '无分区'

            # 重要勿删，上一步分区已遍历完
            break

    # 分区处理
    print '# partition_list', partition_list

    partition = ''

    # 无分区表
    if len(partition_list) == 0:
        pass

    else:
        # 月分区，取上个月，前一个周期
        if partition_list[0] == 'partition_month':
            today = datetime.date.today()
            first = today.replace(day=1)
            last_month = first - datetime.timedelta(days=1)
            last_month=last_month.strftime("%Y%m")
            print '# last_month', last_month

        # 日分区，取前一天，前一个周期
        elif partition_list[0] == '':
            today = datetime.date.today()

            yestoday = today + datetime.timedelta(days=-1)

            print '# yestoday', yestoday

            # 其他分区，先不检测，记录到文件
        else:
            chk_error = open('./chk_error.txt', 'w')
            chk_error.write(str(partition_list))
            chk_error.close()


# 创建sql，进行查询,输入表名，int字段
def create_sql(table_name, table_int_list):
    # select 'DATA_SOURCE',table_name,'partition',count(*),concat(nvl(sum(id),''),nvl(sum(name),'')),'REMARK',from_unixtime(unix_timestamp()) from table_name where patitions='';
    sql_part1 = "select 'DATA_SOURCE','" + table_name + "','partition', count(*)"
    sql_part3 = ",'REMARK',from_unixtime(unix_timestamp()) from loc_use_base_momth;"

    table_int_str = ''
    for i in range(len(table_int_list)):
        table_int_str = table_int_str + "nvl(sum(%s),'')," % (table_int_list[i])

    print 'table_int_str', table_int_str

    sql_part2 = ",concat(%s)" % (table_int_str[0:-1])

    sql = sql_part1 + sql_part2 + sql_part3

    print 'sql select :', sql
    insert_table(sql)

    # 删除表结构文本文件
    delete_sh = 'rm ' + table_name + '.txt'
    os.popen(delete_sh).readlines()


# 构造出sql，将查询结果插入稽核结果表中
def insert_table(sql):
    chk_table_name = 'chk_result'
    insert_sql = 'insert into table ' + chk_table_name + ' ' + sql
    print insert_sql


# 获取表结构
def get_table_struct(table_name):
    pass


# 导出文件到数据

# 对比数据，废弃该方法
def diff_data():
    pass


# 读取表名
def read_table_name():
    f = open('./test_table_name.txt', 'r')
    i = 1
    for line in f.readlines():
        line = line.strip('\n')

        print 1, ' #########################'
        print line
        create_desc(line)
        break


read_table_name()