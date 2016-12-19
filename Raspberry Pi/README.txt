- NodeRed, nmap/python-nmap, and squid/squid-guard services on raspberryPi work coherently.
Therefore, they need to be configured properly all together.

- NodeRed service is able to blockWebs command and update the file containing blocking websites.
This file is named "testdomains" and it squid-guard configuration is currently using this file to block a website. 
When a change is made in this file's location, its new location should be modified according in both NodeRed update blocking website module
and squid-guard configuration.

- NodeRed detect Strange Mac Addr module runing using a python script requiring python-nmap library and nmap installed in raspberry. 
These dependency is listed in file "requirement.txt" in nmap folder.

- NodeRed detect Strange Mac Addr module runing a python script named "app.py" which currently resides in nmap folder.
A concrete location in a real RaspberryPi needs to be update in NodeRed.
The python script works with two external file "regMacs.txt" and "unregMacs.txt" to generate useful output. 
Absolute locations of these two files need to be updated in file "configure.txt" residing in the same folder - nmap folder

- NodeRed service will update regMacs.txt and unregMacs.txt when there is a change.
This allows synchronization between different Pi registered under one account.
Absolute path of these two files also need to update in two NodeRed modules - update registered Mac Addr, and update unregistered Mac Addr.

- all IBM IOT nodes need to have appropriate authentication (matches with IBM Iot Flatform setup) to be able to receive all update commands.

- currently, no data is pushed to IBM Iot Flatform, but it can be enabled by an output IBM IoT node with proper authentication.