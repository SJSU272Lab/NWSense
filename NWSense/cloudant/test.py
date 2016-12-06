from cloudant.client import Cloudant
import json

credentials = json.load(open('credentials.json'))
client =  Cloudant(credentials['username'],credentials['password'],url = credentials['url'])
client.connect()
print client.all_dbs()
mydb = client['iotp_g5lb4t_default_2016-11-28']
print mydb
for doc in mydb:
    print doc['data']