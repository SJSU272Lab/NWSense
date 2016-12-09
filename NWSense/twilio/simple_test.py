from twilio.rest import TwilioRestClient
import json


twiliocred = json.loads(open("twilioCred.json",'r').read())
client = TwilioRestClient(twiliocred['account'],twiliocred['token'])
numbers = json.loads(open('phone_number.json').read())
message = client.sms.messages.create(to=numbers['seema'],from_=numbers['twilio'],body="some one is trying to access your home network. mac addr is 12345789")

