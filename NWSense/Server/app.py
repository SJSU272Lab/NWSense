from flask import Flask,redirect, make_response
from flask import render_template
from flask import request
import os, json


app = Flask(__name__)

from cloudant.client import Cloudant
credentials = json.load(open('userCred.json'))
client =  Cloudant(credentials['username'],credentials['password'],url = credentials['url'])
client.connect()
userDB = client['user']


@app.route('/update/blockWebs',methods=['POST'])
def updateBlockWebs():
    if request.method == 'POST':
        json_request = json.loads(request.data)
        userId = json_request['userId']
        
        #update blockWebs
        doc = userDB[userId]
        blockWebs = json_request['blockWebs']
        doc['blockWebs'] =  blockWebs
        doc.save()

        #notify... raspberry
        import ibmiotf.application
        regPis = [pi for pi in doc['regPi']]
        print regPis
        try:
            client = ibmiotf.application.Client(json.load(open("iotCred.json")))
            client.connect()
            for pi in regPis:
                if 'type' in pi and 'id' in pi:
                    client.publishCommand(pi['type'],pi['id'],'blockWebs','json',data = {'args':doc['blockWebs']})
            client.disconnect()
        except ibmiotf.ConnectionException as e:
            print e
        response = make_response()
        response.status_code = 201
        return response

@app.route('/getAuthen',methods=['GET'])
def getAuthen():
    if request.method == 'GET':
        users = {"users":[]}
        print 'here'
        for user in userDB:
            usr={}
            usr['email'] = user['authen']['email']
            usr['password'] = user['authen']['password']
            usr['id'] = user['_id']
            print usr
            users['users'].append(usr)
            print users
        response = make_response(str(users))
        response.status_code = 200
        return response
    



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port = 4444)