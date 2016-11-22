import nmap
from getIPAddr import IFConfig
import os
import re


nm = nmap.PortScanner()
ifconfig = IFConfig(None)

myAddr = ifconfig.getIP()
myMask = ifconfig.getMask()
gateW = ifconfig.getDefaultGW()

pat = ""
mask = ""

if(myMask == '255.255.255.0'):
    pat = r'(\d+\.\d+\.\d+\.)\d+'
    mask = '0/24'

if (myMask == '255.255.0.0'):
    pat = r'(\d+\.\d+\.)\d+\.\d+'
    mask = '0.0/16'

r = re.search(pat,myAddr,re.I)


ipAddr = r.group(1) + mask

print ipAddr

def getOnlineHosts():
    #for quick determination of online hosts only do ping scan
    nm.scan(ipAddr,arguments='-sn')
    results = []
    for h in nm.all_hosts():
        host_mac = ()
        if os.getuid() == 0 and 'mac' in nm[h]['addresses']:
            host_mac = (h,nm[h]['addresses']['mac'])
        else:
            host_mac = (h,"--:--:--:--:--:--")
        if h == myAddr or h == gateW:
            continue
        else:
            results.append(host_mac)
    return results



