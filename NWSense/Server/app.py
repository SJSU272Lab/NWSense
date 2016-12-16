from flask import Flask,redirect, make_response, abort
from flask import Response
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
            print "not found id"
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
                    client.publishCommand(pi['type'],pi['id'],fileName,'json',data = {'args':doc[fileName]})
            client.disconnect()
            response = make_response()
            response.status_code = 202
            return response
        except ibmiotf.ConnectionException as e:
            print (e)

@app.route('/append/blockMacs',methods=['PUT'])
def appendBlockMacs(): 
    if request.method == 'PUT':
        json_request = json.loads(request.data)
        userId = json_request['userId']

        try:
            doc = userDB[userId]
        except Exception as e:
            print "not found id"
            print (e)
            abort(404)

        appendMacs = json_request['blockMacs']
        blockMacs = doc['blockMacs']
        unregMacs = doc['unregMacs']
        for mac in appendMacs:
            urM = [ur['addr'] for ur in unregMacs]
            if mac in urM:
                index = urM.index(mac)
                transfer = unregMacs[index]
                unregMacs.remove(transfer)
                blockMacs.append(transfer)
        doc['blockMacs'] = blockMacs
        doc['unregMacs'] = unregMacs
        doc.save()

        import ibmiotf.application
        regPis = [pi for pi in doc['regPi']]
        try:
            client = ibmiotf.application.Client(json.load(open("iotCred.json")))
            client.connect()
            for pi in regPis:
                if 'type' in pi and 'id' in pi:
                    client.publishCommand(pi['type'],pi['id'],'blockMacs','json',data = {'args':doc['blockMacs']})
                    client.publishCommand(pi['type'],pi['id'],'unregMacs','json',data = {'args':doc['unregMacs']})
            client.disconnect()
        except ibmiotf.ConnectionException as e:
            print (e)

        if 'phoneNumber' in doc:
            print True
            appendMacsBody = "you have successfully BLOCK %d MAC addresses from your home network:\n"%(len(appendMacs))
            for macAddr in appendMacs:
                appendMacsBody += macAddr + "\n"
            for number in doc['phoneNumber']:
                twilioClient.sms.messages.create(to = number, from_=twilioNumber,body = appendMacsBody)

        return Response(status = 202)

@app.route('/append/regMacs',methods=['PUT'])
def appendRegMacs(): 
    if request.method == 'PUT':
        json_request = json.loads(request.data)
        userId = json_request['userId']

        try:
            doc = userDB[userId]
        except Exception as e:
            print "not found id"
            print (e)
            abort(404)

        appendMacs = json_request['regMacs']
        regMacs = doc['regMacs']
        unregMacs = doc['unregMacs']
        for mac in appendMacs:
            urM = [ur['addr'] for ur in unregMacs]
            if mac in urM:
                index = urM.index(mac)
                transfer = unregMacs[index]
                unregMacs.remove(transfer)
                regMacs.append(transfer)
        doc['regMacs'] = regMacs
        doc['unregMacs'] = unregMacs
        doc.save()

        import ibmiotf.application
        regPis = [pi for pi in doc['regPi']]
        try:
            client = ibmiotf.application.Client(json.load(open("iotCred.json")))
            client.connect()
            for pi in regPis:
                if 'type' in pi and 'id' in pi:
                    client.publishCommand(pi['type'],pi['id'],'regMacs','json',data = {'args':doc['regMacs']})
                    client.publishCommand(pi['type'],pi['id'],'unregMacs','json',data = {'args':doc['unregMacs']})
            client.disconnect()
        except ibmiotf.ConnectionException as e:
            print (e)

        if 'phoneNumber' in doc:
            print True
            appendMacsBody = "you have successfully REGISTER %d MAC addresses from your home network:\n"%(len(appendMacs))
            for macAddr in appendMacs:
                appendMacsBody += macAddr + "\n"
            for number in doc['phoneNumber']:
                twilioClient.sms.messages.create(to = number, from_=twilioNumber,body = appendMacsBody)

        return Response(status = 202)
        

@app.route('/<string:fileName>/<string:userId>',methods=['GET'])
def getFile(fileName,userId):
    if request.method == 'GET':
        #userId = str(userId)
        #get File
        try:
            doc = userDB[userId]
            getFile = {}
            getFile[fileName] =  doc[fileName]
            response = Response(response = json.dumps(getFile), status = 200, mimetype = 'application/json')
            #response.status_code = 200
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
            users['users'].append(usr)
        #response = make_response(str(users))
        #response.status_code = 200
        response = Response(response = json.dumps(users),status = 200, mimetype='application/json')
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