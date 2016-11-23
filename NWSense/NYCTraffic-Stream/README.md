#Streaming Ananlytics Traffic Starter Application
Welcome to the Streaming Analytics service powered by IBM InfoSphere Streams! The starter application demonstrates how to configure and control the Streaming Anayltics service through its REST API. The application is written in java using the Liberty for Java Runtime. You can modify the application code and push your changes back to the Bluemix environment.

Licensed under the Apache License (see [License.txt](https://hub.jazz.net/project/streamscloud/NYCTraffic/overview#https://hub.jazz.net/git/streamscloud%252FNYCTraffic/contents/master/License.txt)).

## Getting Bluemix ready for the starter application

To get Bluemix ready for the Streaming Analytics starter application, you need to:
1. Sign up for [Bluemix](https://ace.ng.bluemix.net/) and log in.

- [Install the cf command-line tool](https://www.ng.bluemix.net/docs/starters/install_cli.html).

- Create an application in the Bluemix web interface using the **Liberty for Java** runtime. Remember the name you give your application, you will need it later on. 

- Add the Streaming Analytics service to your application from the Bluemix web interface.


## Pushing the starter application into Bluemix

After you meet these prerequisites, you are ready to download and push the starter application to Bluemix:

1. Click the **download** button "Download the contents of this branch as a zip file" in this browser tab.


- After the download completes, extract the .zip file.

- Rename the directory NYCTrafficSample in the extracted files to match the name you gave your application in Bluemix earlier.
		
- On the command line, `cd` to the renamed directory. For example:
		cd myapp
		
- Connect to Bluemix:

		cf api https://api.ng.bluemix.net

- Log into Bluemix and set your target org when prompted:

		cf login

- Deploy your app. For example:

		cf push myapp

- Access your app from the dashboard in Bluemix.
