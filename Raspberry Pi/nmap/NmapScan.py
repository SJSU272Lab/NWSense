import nmap
from getIPAddr import IFConfig
import os
import re
import time



ifconfig = IFConfig(None)

myAddr = ifconfig.getIP()
myMask = ifconfig.getMask()
gateW = ifconfig.getDefaultGW()

pat = ""
mask = ""

#if(myMask == '255.255.255.0'):
pat = r'(\d+\.\d+\.\d+\.)\d+'
mask = '0/24'
#else:
#    exit(1)

#if (myMask == '255.255.0.0'):
#    pat = r'(\d+\.\d+\.)\d+\.\d+'
#    mask = '0.0/16'

r = re.search(pat,myAddr,re.I)


ipAddr = r.group(1) + mask

class IPScan():
    def __init__(self):
        self.nm = nmap.PortScanner()
    
    def getScanTimeSecond(self):
        return self.elapsed_time

    def getScanTime(self):
        m,s = divmod(self.elapsed_time,60)
        h,m = divmod(m,60)
        return (h,m,s)

    def getOnlineHosts(self):
        #for quick determination of online hosts only do ping scan
        start_time = time.time()
        self.nm.scan(ipAddr,arguments='-sn')
        self.elapsed_time = time.time() - start_time
        results = []
        hosts = self.nm.all_hosts()
        hosts.remove(myAddr)
        if gateW in hosts:
            hosts.remove(gateW)
        for h in hosts:
            host_mac = (h,"--:--:--:--:--:--")
            if os.getuid() == 0 and 'mac' in self.nm[h]['addresses']:
                host_mac = (h,self.nm[h]['addresses']['mac'])
            results.append(host_mac)
        return results



if __name__ == "__main__":
    aaa = IPScan()
    
    print aaa.getOnlineHosts()
    print aaa.getScanTimeSecond()