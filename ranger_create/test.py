import apache_ranger.client.ranger_client as client

url = 'http://172.19.168.231:6080/service/public/v2/api/policy'
username = 'admin'
password = '1q2w!Q@W'

ranger_client = client.RangerClient(url, username, password)

print(ranger_client.url)
print(ranger_client.get_policy_by_id('36'))
# print(ranger_client.get_all_role_names('csap','csap_hive'))
# print(ranger_client.get_policy_by_id('36'))
