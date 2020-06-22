# encoding=utf8

# partition_sort.py
import os
import sys


# 统计分区字段种类
def save_partition_sort():
    partition_result_list = []

    partition_name_list = []

    partition_sort_list = open('./check_result.txt', 'r').readlines()
    for i in range(len(partition_sort_list)):
        partition_str_list = partition_sort_list[i].split(' ')

        # 检测多个分区，目前没有多分区表
        if len(partition_str_list) > 2:
            print partition_sort_list[i]
            # break
        table_name = partition_str_list[0]
        partition_name = partition_str_list[1].replace('[', '').replace(']', '').replace('\'', '').replace('\n', '')

        if partition_name in partition_name_list:
            continue

        partition_name_list.append(partition_name)

        partition_result_list.append([table_name, partition_name])
        # if partition_name not in partition_result_list[i][1]:
        #     partition_result_list.append([table_name, partition_name])

        # 分区去重
        flag = 0
        for j in range(len(partition_result_list)):

            if partition_result_list[j][1] == partition_name:
                flag = 1
                break
    print '分区种类：',len(partition_result_list)
    for i in partition_result_list:
        print i
    # print partition_result_list


save_partition_sort()
