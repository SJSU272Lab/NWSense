from flask import Flask,redirect, make_response, abort
from flask import render_template
from flask import request
import os, json

app = Flask(__name__)

from twilio.rest import TwilioRestClient
twilioNumber = "+12568407597"
twiliocred = json.loads(open("twilioCred.json",'r').read())
twilioClient = TwilioRestClient(twiliocred['account'],twiliocred['token'])


from cloudant.client import Cloudant
credentials = json.load(open('userCred.json'))
client =  Cloudant(credentials['username'],credentials['password'],url = credentials['url'])
client.connect()
userDB = client['user']

@app.route('/<string:fileName>',methods=['PUT'])
def updateFiles(fileName):
    if request.method == 'PUT':
        json_request = json.loads(request.data)
        userId = json_request['userId']

        try:
            doc = userDB[userId]
        except Exception as e:
            print (e)
            abort(404)

        docFile = json_request[fileName]
        doc[fileName] =  docFile
        doc.save()

        import ibmiotf.application
        regPis = [pi for pi in doc['regPi']]
        try:
            client = ibmiotf.application.Client(json.load(open("iotCred.json")))
            client.connect()
            for pi in regPis:
                if 'type' in pi and 'id' in pi:
                    client.publishCommand(pi['type'],pi['id'],'blockWebs','json',data = {'args':doc[fileName]})
            client.disconnect()
            response = make_response()
            response.status_code = 202
            return response
        except ibmiotf.ConnectionException as e:
            print (e)
        



@app.route('/<string:fileName>/<string:userId>',methods=['GET'])
def getBlockWebs(fileName,userId):
    if request.method == 'GET':
        #userId = str(userId)
        #get blockWebs
        try:
            doc = userDB[userId]
            blockWebs = {}
            blockWebs[fileName] =  doc[fileName]
            response = make_response(str(blockWebs))
            response.status_code = 200
            return response
        except Exception as e:
            print (e)
            abort(404)
        

@app.route('/authen',methods=['GET'])
def getAuthen():
    if request.method == 'GET':
        users = {"users":[]}
        for user in userDB:
            usr={}
            usr['email'] = user['authen']['email']
            usr['password'] = user['authen']['password']
            usr['id'] = user['_id']
            print (usr)
            users['users'].append(usr)
            print (users)
        response = make_response(str(users))
        response.status_code = 200
        return response

@app.route('/suspiciousMacs',methods=['POST'])
def sendNotification():
    if request.method == 'POST':
        json_request = json.loads(request.data)
        userId = str(json_request['userId'])

        if 'suspiciousMacs' in json_request:
            suspiciousMacs = json_request['suspiciousMacs']
        if len(suspiciousMacs) < 1:
            abort (404)

        smsMacs = []
        try:
            doc = userDB[userId]
            for mac in suspiciousMacs:
                if mac['addr'] not in [m['addr'] for m in doc['unregMacs']]:
                    doc['unregMacs'].append(mac)
                    smsMacs.append(mac['addr'])
            doc.save()
        except Exception as e:
            print (e)
            abort(404)
        
        response = make_response()
        response.status_code = 202

        if len(smsMacs) == 0:
            return response

        if 'phoneNumber' in doc:
            suspiciousMacsBody = "%d new suspicious device(s) have accessed to your home network:\n"%(len(smsMacs))
            count = 0
            for macAddr in smsMacs:
                suspiciousMacsBody += macAddr + "\n"
            for number in doc['phoneNumber']:
                twilioClient.sms.messages.create(to = number, from_=twilioNumber,body = suspiciousMacsBody)
        
        #update unregMacs to all devices
        import ibmiotf.application
        regPis = [pi for pi in doc['regPi']]
        try:
            client = ibmiotf.application.Client(json.load(open("iotCred.json")))
            client.connect()
            unregMacs = [mac['addr'] for mac in doc['unregMacs']]
            for pi in regPis:
                if 'type' in pi and 'id' in pi:
                    client.publishCommand(pi['type'],pi['id'],'unregMacs','json',data = {'args':unregMacs})
            client.disconnect()
        except ibmiotf.ConnectionException as e:
            print (e)

        
        return response


        




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port = 4444)