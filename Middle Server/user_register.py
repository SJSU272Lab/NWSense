from cloudant.client import Cloudant
import json
import random

credentials = json.load(open('userCred1.json'))
client =  Cloudant(credentials['username'],credentials['password'],url = credentials['url'])
client.connect()
print client.all_dbs()

doc = json.load(open("data_schema.json"))
user = doc['user']
#userId = 'u'+str(random.getrandbits(128))
#user['_id'] = userId



#userDB = client.create_database("user")
userDB = client['user']
userDB.create_document(user)