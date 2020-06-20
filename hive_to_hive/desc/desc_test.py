# encoding=utf8
import sys


# desc_test.py

def desc_parser():
    desc_list = open('./desc.txt', 'r').readlines()

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
            print '#'
       
        # # 忽略表头
        # if line_list[2] == 'col_name':
        #     continue

        # if line[1] == ' ':
        #     continue

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

                break

            print desc_list[i]
            continue

        # table_str=desc_list[i].replace(' ', '')
        # print 'table_str',table_str
        # # table_str=table_str.encode(encoding='utf8')
        #
        # # list输出乱码,python2输出以16进制输出内容
        #
        #
        #
        # print table_str.split('|')
        # print table_str.split('|')[3]
        # print '\n'.join(table_str.split('|'))

        # break

    # i = 1
    # for line in f.readlines():
    #     line = line.strip('\n')
    #
    #     # print 1, ' #########################'
    #
    #     if line[0] == '+':
    #         continue
    #
    #     # if line[1] == ' ':
    #     #     continue
    #
    #     if line[2] == '#':
    #         print line
    #         continue
    #
    #     print line.replace(' ','')
    # break


desc_parser()
