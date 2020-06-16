
beeline -u 'jdbc:hive2://hua-dlzx2-a0202:10000/default' -n ocdp -p 1q2w1q@W

beeline -u "jdbc:hive2://hua-dlzx2-a0202:10000/default" -n ocdp -p 1q2w1q@W -e "show databases"

# 本地集群
beeline -u "jdbc:hive2://hua-dlzx2-a0202:10000/default" -n ocdp -p 1q2w1q@W -e "show databases"

# 远程集群
beeline -u "jdbc:hive2://192.168.190.88:10000/default" -n ocdp -p 1q2w1q@W -e "show databases"


# 远程主机
ssh hive@192.168.190.91


