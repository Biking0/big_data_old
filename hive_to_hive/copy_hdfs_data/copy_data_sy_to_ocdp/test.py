
# # 文件名管理
    # random_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    #
    # file_name = table_name + '_' + partition_date + '_' + random_str + '.txt'
    #
    # print file_name
    #
    # check_date_sql_sh = mysql_sh + check_date_sql + '\' > ' + get_task_file

import datetime

print str(datetime.datetime.now())[0:19]
print datetime.date.today()