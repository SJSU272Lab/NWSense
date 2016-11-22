# NWSense
**NWSense** is a web app based internet security system for home networks which provides security over the whole network. It provides allows the user to monitor the network and block IP addresses or websites which are to be accessed on the network. It also allows the user to view a detailed analysis.
The web app requires the user to login with the username and password. The system then fetches the IP address/MAC address of the router. This provides the user with the configuration of the system, and the feature to edit the configuration.
After the configuration has been saved, the blocked IP addresses will not be able to access the network, and the users will not be able to surf the blocked websites.
The user can also see and monitor what all devices are connected to the network. The user can also see a detailed analysis of what is happening inside the network, e.g., what websites are most visited, what users make the most use of network, etc.

**Internal Implementation:**

We can access our router from the external network using DDNS and port forwarding. An exception is that these capabilities are not available on all routers.
For solving this problem ,internally **NWSense** will be using a dedicated IOT device for running the nmap , tshark and other utilities within the home network for capturing data packets,port scanning and will be pushing this data to the server. 
On the server analysis will be done over this data using technologies like Spark.
The user can select IP's , websites to block on the website. This information will be pushed to the Rasberry-Pi from the server.
The Rasberry-Pi will provide a wifi-end point to which other devices in the home network will connect to. So the IOT device acts as layer over the Router. The proxy server/gateway present on the Rasberry Pi will filter each request it gets from the connected device and then forward it to the router. 
The proxy server present on the Rasberry pi can be accessed from any external network.

## Architectural Flow Diagram
![alt tag](https://raw.githubusercontent.com/SJSU272Lab/Fall16-Team13/master/ArchitecturalFlowDiagram.png)

## User Stories

### User Story 1:
As a network owner, I can login in my application so that I can block the websites.

### User Story 2:
As a user, I can monitor all devices connected to my network, so that I can check for unauthorized users/devices.

### User Story 3:
As a user, I can see detailed analytics of network, so that I can monitor data usage by each device.
 
## Personas
### Persona 1:
Home Network Owner
### Persona 2:
Home Network User

