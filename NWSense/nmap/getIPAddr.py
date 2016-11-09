import socket
import fcntl
import struct

interface = 'wlp2s0'

def getIPAddr(ifname):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])


def getMyIpAddr(ifname):
    if ifname is None:
        ifname = interface
    return getIPAddr(ifname)


