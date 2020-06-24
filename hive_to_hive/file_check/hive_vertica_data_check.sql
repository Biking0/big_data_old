
# 建表
CREATE TABLE CHK_RESULT (
 DATA_SOURCE    STRING          COMMENT '数据源'
,DES_TBL        STRING          COMMENT '目标表名'
,CYCLICAL       STRING          COMMENT '周期'
,COUNT1         STRING          COMMENT '数据统计'
,SUM1           STRING          COMMENT '求和' sum()
,REMARK         STRING          COMMENT '备注'
,CHK_DT         int             COMMENT '检核时间'
)
COMMENT '数据质量检核结果表'
PARTITION BY (CHK_TD DATE)
ROW FORMAT DELIMITED FILEDS TERMINATED BY ' ';


样例：
hive原表

test_hyn
id(int)

对应的hive稽核表
test_hyn_check

table_name string
count_data string
sum_column1 string
remark string
chk_dt string



# 非分区表
对应hive表


# 插入数据

# sql拼接字段
select concat(nvl(leix01,''),nvl(leix02,''),nvl(leix03,'')) from dim_ivr_dictionary where ivr_table like 'zj%' and bm='40102'

select concat(nvl(leix01,''),nvl(leix02,''),nvl(leix03,'')) from dim_ivr_dictionary where ivr_table like 'zj%' and bm='40102'

create table test_hyn (id int ,name int) ; values ()

insert into test_hyn (id,name ) values (2,3)


select concat(nvl(id,''),nvl(name,'')) from test_hyn;





