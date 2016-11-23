from libnmap.process import NmapProcess
import getIPAddr
import json

ipaddr = getIPAddr.getMyIpAddr(None)

mask = ipaddr[:len(ipaddr)-2]
mask += '*'

nm = NmapProcess(mask,options = "-p 80 --open")
rc = nm.run()

if nm.rc == 0:
     print (nm.stdout)
else: 
    print (nm.stderr)

#print (json.dumps(nm.stdout))