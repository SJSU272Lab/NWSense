from cloudant.client import Cloudant
import json
import random

credentials = json.load(open('userCred1.json'))
client =  Cloudant(credentials['username'],credentials['password'],url = credentials['url'])
client.connect()
print client.all_dbs()



#userDB = client.create_database("user")
userDB = client['user']