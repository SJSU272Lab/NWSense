from NmapScan import getOnlineHosts
import datetime
import getIPAddr



#get registered mac addresses
registered_macs = [mac.rstrip('\n') for mac in open("registered_mac.txt",'r')]

online_hosts = getOnlineHosts()
print ('Found %s hosts up:\n' %len(online_hosts))

#output to connection_report.txt
output = open('connection_report.txt','a')
output.write('Scan at ' +  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
output.write('\tFound %s hosts up:\n' %len(online_hosts))

unregistered = []

output.write('\t\tRegistered devices\n')
for host in online_hosts:
    h = host[0]
    m = host[1]
    if m in registered_macs:
        output.write('\t\t\t'+ h +  "\t:   " + m + '\n')
        print ('\t'+ h + '\t:  ' + m + "\t:  registered")
    else:
        unregistered.append(host)

output.write('\t\tSuspicious devices\n')
print('\n')
for host in unregistered:
    h = host[0]
    m = host[1]
    output.write('\t\t\t'+ h +  "\t:   " + m + '\n')
    print ('\t' + h + '\t:  ' + m + "\t:  SUSPICIOUS") 

output.write('\n')
output.close()

