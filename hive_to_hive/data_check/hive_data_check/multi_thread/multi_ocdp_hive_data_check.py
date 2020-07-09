#!/usr/bin/env python
# -*-coding:utf-8 -*-
# ***************************************************************************
# 文件名称：multi_ocdp_hive_data_check.py
# 功能描述：hive表数据稽核
# 输 入 表：
# 输 出 表：
# 创 建 者：hyn
# 创建日期：20200624
# 修改日志：
# 修改日期：
# ***************************************************************************
# 程序调用格式：python multi_ocdp_hive_data_check.py
# ***************************************************************************

# 1. 分析hive库表结构，获取int字段，将所有表存到列表里
# 2. 构造数据稽核sql，分析周期（分区），sum字段
# 3. 抽取两个库的表文件到本地，进行对比

import os
import sys
import time
import datetime
import config
import pubUtil
import threading

# 生产环境
# excute_desc_sh = "beeline -u 'jdbc:hive2://192.168.190.88:10000/csap' -n hive -p %Usbr7mx -e "
excute_desc_sh = "beeline -u 'jdbc:hive2://hua-dlzx2-a0202:10000/csap' -n ocdp -p 1q2w1q@W -e "


# 测试环境
# excute_desc_sh = "beeline -u 'jdbc:hive2://172.22.248.19:10000/default' -n csap -p @WSX2wsx -e "


# 生成desc表结构文件
def create_desc(table_name):
    # 生产环境
    desc_sh = "beeline -u 'jdbc:hive2://hua-dlzx2-a0202:10000/csap' -n ocdp -p 1q2w1q@W -e 'desc  " + table_name + ' \' >> /home/ocdp/hyn/data_check/hive_data_check/' + table_name + '.txt'

    # 测试环境
    # desc_sh = "beeline -u 'jdbc:hive2://172.22.248.19:10000/default' -n csap -p @WSX2wsx -e 'desc  " + table_name + ' \' > ./' + table_name + '.txt'

    print desc_sh
    os.popen(desc_sh).readlines()
    desc_parser(table_name)


# 解析desc表结构
def desc_parser(table_name):
    desc_list = open('/home/ocdp/hyn/data_check/hive_data_check/' + table_name + '.txt', 'r').readlines()

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
    check_partition(table_name, result_list)


# 分区检测，构造分区，根据需要稽核的时间段，循环生成相应的分区，判断是否为分区表,line(table_name)
def check_partition(line, result_list):
    desc_list = open('/home/ocdp/hyn/data_check/hive_data_check/' + line + '.txt', 'r').readlines()

    # result_list = []
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
            last_month = last_month.strftime("%Y%m")
            print '# last_month', last_month
            partition = 'partition_month=' + str(last_month).replace('-', '')

        # 日分区，取前一天，前一个周期
        elif partition_list[0] == 'statis_date':
            today = datetime.date.today()

            yestoday = today + datetime.timedelta(days=-1)

            print '# yestoday', yestoday

            partition = 'statis_date=' + str(yestoday).replace('-', '')

        elif partition_list[0] == 'statis_month':
            today = datetime.date.today()
            first = today.replace(day=1)
            last_month = first - datetime.timedelta(days=1)
            last_month = last_month.strftime("%Y%m")
            print '# last_month', last_month
            partition = 'statis_date=' + str(last_month).replace('-', '')

        # 其他分区，先不检测，记录到文件
        else:
            chk_error = open('/home/ocdp/hyn/data_check/hive_data_check/chk_error.txt', 'a+')
            chk_error.write(str(partition_list))
            chk_error.close()

    # 创建查询sql
    create_sql(line, result_list, partition)


# 创建sql，进行查询,输入表名，int字段
def create_sql(table_name, table_int_list, partition):
    sql_part1 = ''
    sql_part3 = ''

    # 无分区
    if partition == '':
        partition = 'no_partition'
        sql_part1 = "select 'DATA_SOURCE','" + table_name + "','" + partition + "', count(*)"
        sql_part3 = ",'REMARK',from_unixtime(unix_timestamp()) " + " from " + table_name + " ;"

    else:
        # select 'DATA_SOURCE',table_name,'partition',count(*),concat(nvl(sum(id),''),nvl(sum(name),'')),'REMARK',from_unixtime(unix_timestamp()) from table_name where patitions='';
        sql_part1 = "select 'DATA_SOURCE','" + table_name + "','" + partition + "', count(*)"

        # todo 无分区表，增量数据无法稽核，全表可稽核
        sql_part3 = ",'REMARK',from_unixtime(unix_timestamp()) " + " from " + table_name + " where " + partition + ";"

    table_int_str = ''
    for i in range(len(table_int_list)):
        table_int_str = table_int_str + "nvl(sum(%s),''),'_'," % (table_int_list[i])

    print 'table_int_str', table_int_str

    sql_part2 = ",concat(%s)" % (table_int_str[0:-5])

    sql = sql_part1 + sql_part2 + sql_part3

    print 'sql select :', sql

    # 执行查询
    select_sql_sh = excute_desc_sh + ' \" ' + sql + ' \"'
    print select_sql_sh
    # os.popen(select_sql_sh).readlines()

    insert_table(table_name, sql)

    # 删除表结构文本文件
    delete_sh = 'rm ' + table_name + '.txt'
    # os.popen(delete_sh).readlines()


# 构造出sql，将查询结果插入稽核结果表中
def insert_table(table_name, sql):
    chk_table_name = 'chk_result'
    insert_sql = " use csap; insert into table " + chk_table_name + " partition (static_date=" + time.strftime("%Y%m%d",
                                                                                                               time.localtime(
                                                                                                                   time.time())) + ") " + sql
    print insert_sql

    # 执行插入语句
    insert_sql_sh = excute_desc_sh + ' \" ' + insert_sql + ' \" '
    print insert_sql_sh
    os.popen(insert_sql_sh).readlines()

    # export_chk_result(table_name)


# 获取表结构
def get_table_struct(table_name):
    pass


# 导出稽核结果表到文件
def export_chk_result(table_name):
    export_sql = 'use csap; select DES_TBL,CYCLICAL,COUNT1,SUM1,REMARK from chk_result;'

    export_sh = excute_desc_sh + ' \" ' + export_sql + ' \" ' + ' >> chk_result.txt'

    print 'export_sh', export_sh

    os.popen(export_sh).readlines()


# 将苏研集群稽核表迁移到oadp集群
def distcp_sy_to_ocdp():
    # ocdp集群添加分区

    add_partition_sh = "beeline -u 'jdbc:hive2://hua-dlzx2-a0202:10000/csap' -n ocdp -p 1q2w1q@W -e " + 'alter table '


# 对比数据，废弃该方法
def diff_data():
    pass


# 读取表名
def read_table_name():
    f = open('/home/ocdp/hyn/data_check/hive_data_check/test_table_name.txt', 'r')
    i = 1

    multi_list = []

    for line in f.readlines():
        line = line.strip('\n')

        print 1, ' #########################'
        print line
        multi_list.append(line)

        # 开始解析
        # create_desc(line)

        # 连续读取目标表
        # break

    multi_thread(multi_list)


# 遍历列表
def read_list(num, tar_list):
    for i in tar_list:
        try:
            print 'table_name', i
            create_desc(i)
        except Exception as e:
            print e
            continue


# 多线程
def multi_thread(multi_list):

    print 'multi_list',multi_list

    print '1',multi_list[0:2]
    print '2',list(multi_list[0:2])
    # list分块，调用多线程
    multi1 = threading.Thread(target=read_list, args=(5, multi_list[0:15]))
    multi2 = threading.Thread(target=read_list, args=(5, multi_list[15:30]))
    multi3 = threading.Thread(target=read_list, args=(5, multi_list[30:45]))
    multi4 = threading.Thread(target=read_list, args=(5, multi_list[45:60]))
    multi5 = threading.Thread(target=read_list, args=(5, multi_list[60:75]))
    multi6 = threading.Thread(target=read_list, args=(5, multi_list[75:90]))
    multi7 = threading.Thread(target=read_list, args=(5, multi_list[90:105]))
    multi8 = threading.Thread(target=read_list, args=(5, multi_list[105:120]))
    multi9 = threading.Thread(target=read_list, args=(5, multi_list[120:135]))
    multi10 = threading.Thread(target=read_list, args=(5, multi_list[135:165]))
    multi11 = threading.Thread(target=read_list, args=(5, multi_list[165:180]))
    multi12 = threading.Thread(target=read_list, args=(5, multi_list[180:195]))
    multi13 = threading.Thread(target=read_list, args=(5, multi_list[195:210]))
    multi14 = threading.Thread(target=read_list, args=(5, multi_list[210:225]))
    multi15 = threading.Thread(target=read_list, args=(5, multi_list[225:270]))
    multi16 = threading.Thread(target=read_list, args=(5, multi_list[270:285]))
    multi17 = threading.Thread(target=read_list, args=(5, multi_list[285:300]))
    multi18 = threading.Thread(target=read_list, args=(5, multi_list[300:305]))
    multi19 = threading.Thread(target=read_list, args=(5, multi_list[305:309]))
    multi20 = threading.Thread(target=read_list, args=(5, multi_list[309:313]))

    multi1.start()
    multi2.start()
    multi3.start()
    multi4.start()
    multi5.start()
    multi6.start()
    multi7.start()
    multi8.start()
    multi9.start()
    multi10.start()
    multi11.start()
    multi12.start()
    multi13.start()
    multi14.start()
    multi15.start()
    multi16.start()
    multi17.start()
    multi18.start()
    multi19.start()
    multi20.start()


# 运行之前清理结果表分区，添加重跑功能
def clear_ocdp_partition():
    # 清理ocdp集群分区
    sql = "alter table chk_result drop if exists partition(static_date=" + pubUtil.get_today() + ");"

    clear_sql_sh = config.excute_ocdp_sh + sql + '\''

    print clear_sql_sh

    # os.popen(clear_sql_sh)


read_table_name()
