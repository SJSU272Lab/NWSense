import nmap
import getIPAddr
import json
import datetime


nm = nmap.PortScanner()
ipAddr = getIPAddr.getMyIpAddr(None)
command = 'nmap -p80'
port = '80'

target = open('connection_report.txt','w')
target.write('scan at ' +  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
nm.scan(ipAddr,port)
target.write('found %s hosts up\n' %len(nm.all_hosts()))

#target.write(json.dumps(nm))
for host in nm.all_hosts():
    if nm[host].state() == 'up':
        target.write('\t'+host+'\n')
    

target.close()

