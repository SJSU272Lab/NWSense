from flask import Flask,redirect
from flask import render_template
from flask import request
import os, json
import time

import ibmiotf.application

options = json.load(open("IoTcred.json"))

try:
  client = ibmiotf.application.Client(options)
  client.connect()
  client.publishCommand('raspberry','b827ebb5fcf3','blockWebs','json',data = {'args':"block_list"})
  client.publishCommand('raspberry','seema','blockWebs','json',data={'args':["aaaaa.com","bbbb.com"]})
  client.publishCommand('raspberry','amay','blockWebs','json',data={'args':["aaaaa.com","bbbb.com"]})
  client.disconnect()
except ibmiotf.ConnectionException as e:
  print e
