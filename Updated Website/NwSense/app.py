from flask import Flask,render_template,request,json
import requests
app=Flask(__name__)

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    userId=request.form.get('userId')
    password=request.form.get('password')
    response = requests.get("http://54.165.49.28:4444/authen")
    data = json.loads(response.content)
    #checks for authentication
    return render_template('login.html')
    
@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/blockWebs",methods=['POST'])
def blockWebs():
    message=["Succesfully Blocked !"]
    deviceBlocked=[]
    response = requests.get("http://54.165.49.28:4444/blockWebs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata= data.get("blockWebs")
    
    blockwebList=listdata
    fb1=request.form.get('fb')
    tw1=request.form.get('twitter')
    bd=request.form.get('bigdaddy')
    mn=request.form.get('msn')
    youtube=request.form.get('youtube')
    url=request.form.get('websitename')

    if fb1 !=None and fb1 not in blockwebList :
        blockwebList.append(fb1)
    if tw1 !=None and tw1 not in blockwebList :
        blockwebList.append(tw1)
    if bd !=None and bd not in blockwebList :
        blockwebList.append(bd)
    if mn !=None and mn not in blockwebList :
        blockwebList.append(mn)  
    if youtube !=None and youtube not in blockwebList :
        blockwebList.append(youtube)  
    if url !="" and url not in blockwebList :
        blockwebList.append(url)                   
   
    payload = {
	    "userId":"b539ab74bc9bc3e43a4b40040a66fa35",
	    "blockWebs":blockwebList
            }
    r = requests.put("http://54.165.49.28:4444/blockWebs", json=payload)
    response = requests.get("http://54.165.49.28:4444/blockWebs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata1= data.get("blockWebs")
    return render_template('blockWebsite.html', msg=message , ls=listdata1)

@app.route("/blockWebsite")
def blockWebsite():
    response = requests.get("http://54.165.49.28:4444/blockWebs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata= data.get("blockWebs")
    message=[""]
    return render_template('blockWebsite.html', msg=message,ls=listdata)

@app.route("/blockMac",methods=['POST','GET'])
def blockMac(): 
    message=[]
    msg=""
    addr=[]
    response = requests.get("http://54.165.49.28:4444/blockMacs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata= data.get("blockMacs")
    for l in listdata:
        addr.append(l.get("addr"))

    if request.method == "POST":
        selected_macs = request.form.getlist("macs")
        msg="Successfully Blocked"
        payload = {
	    "userId":"b539ab74bc9bc3e43a4b40040a66fa35",
	    "blockMacs":selected_macs
            }
        r = requests.put("http://54.165.49.28:4444/append/blockMacs", json=payload)    
        # put request
    add=[]       
    response = requests.get("http://54.165.49.28:4444/unregMacs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata= data.get("unregMacs")
    for l in listdata:
        add.append(l.get("addr"))
    message.append(msg)  
    message=[]
    msg=""
    addr=[]
    response = requests.get("http://54.165.49.28:4444/blockMacs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata= data.get("blockMacs")
    for l in listdata:
        addr.append(l.get("addr"))  
    return render_template('blockMacs.html', macList=add ,msg=message,ls=addr)
   

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/registerMacs",methods=['POST','GET'])
def registerMacs():
    if request.method == "POST":
        regMac=request.form.get('deviceMac')
        regMacList=[]
        regMacList.append(regMac)
        payload = {
	    "userId":"b539ab74bc9bc3e43a4b40040a66fa35",
	    "regMacs":regMacList
            }
        r = requests.put("http://54.165.49.28:4444/append/regMacs", json=payload)  

    return render_template('registerMacs.html')    

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)