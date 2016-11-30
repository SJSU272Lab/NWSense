from twilio.rest import TwilioRestClient
import json


twiliocred = json.loads(open("twiliocred.json",'r').read())
client = TwilioRestClient(twiliocred['account'],twiliocred['token'])
numbers = json.loads(open('phone_number.json').read())
message = client.sms.messages.create(to=numbers['prachi'],from_=numbers['twilio'],body="hey prachi,this is Khoa's message from python code :))")

