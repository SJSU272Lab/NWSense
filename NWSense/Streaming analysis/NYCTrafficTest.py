import requests
import json

#uri = "http://207.251.86.229/nyc-links-cams/LinkSpeedQuery.txt"
#response = requests.get(uri)
#content = response.content
f = open('test.txt','r')
content = f.read()
f.close()

content = content.replace('"','')
print content
lines = content.split('\r\n')
tokens = []
for line in lines:
    tokens.append( line.split('\t'))
tokens = [token for token in tokens if len(token) == 13 and token[0] != 'Id']

#get out id -0, speed-1, dataasof-4, owner-9, transcom_id-10,Borough -11,LinkName-12;
out = [tokens[i] for i in [0,1,4,9,10,11,12]]
print (out)

