import socket
import fcntl
import struct
import config

default_ifname = config.default_ifname
#default_ifname = "wlp2s0"

class IFConfig():
    def __init__(self,ifname):
        if ifname == None:
            self.ifname = default_ifname
        else:
            self.ifname = ifname
    
    def getIP(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',self.ifname[:15]))[20:24])

    def getMask(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x891b,struct.pack('256s',self.ifname[:15]))[20:24])

    def getDefaultGW(self):
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if (fields[0] != self.ifname) or (fields[1] != '00000000') or not (int(fields[3], 16) & 2):
                    continue
                else:
                    break
            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
        return None

if __name__ == "__main__":
    ifconfig = IFConfig(None)
    print (ifconfig.getIP())
    print (ifconfig.getMask())
    print(ifconfig.getDefaultGW())

