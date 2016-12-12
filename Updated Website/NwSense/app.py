from flask import Flask,render_template,request,json
import requests
import urllib2
app=Flask(__name__)

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/blockWebs",methods=['POST'])
def blockWebs():
    message=["Succesfully Blocked !"]
  
    blockwebList=[]
    fb1=request.form.get('fb')
    tw1=request.form.get('twitter')
    bd=request.form.get('bigdaddy')
    mn=request.form.get('msn')
    youtube=request.form.get('youtube')
    url=request.form.get('websitename')

    if fb1 !=None:
        blockwebList.append(fb1)
    if tw1 !=None:
        blockwebList.append(tw1)
    if bd !=None:
        blockwebList.append(bd)
    if mn !=None:
        blockwebList.append(mn)  
    if youtube !=None:
        blockwebList.append(youtube)  
    if url !="":
        blockwebList.append(url)                   

    payload = {
	    "userId":"b539ab74bc9bc3e43a4b40040a66fa35",
	    "blockWebs":blockwebList
            }
    r = requests.put("http://54.165.49.28:4444/blockWebs", json=payload)
    return render_template('blockWebsite.html', msg=message)

@app.route("/blockWebsite")
def blockWebsite():
    response = requests.get("http://54.165.49.28:4444/blockWebs/b539ab74bc9bc3e43a4b40040a66fa35")
    print response.json
    message=[""]
    return render_template('blockWebsite.html', msg=message)

@app.route("/blockMac",methods=['POST','GET'])
def blockMac(): 
    message=[]
    msg=""
    if request.method == "POST":
        selected_macs = request.form.getlist("macs")
        msg="Successfully Blocked"
        # put request
    add=[]       
    response = requests.get("http://54.165.49.28:4444/unregMacs/b539ab74bc9bc3e43a4b40040a66fa35")
    data = json.loads(response.content) 
    listdata= data.get("unregMacs")
    for l in listdata:
        add.append(l.get("addr"))
    message.append(msg)    
    return render_template('blockMacs.html', macList=add ,msg=message)
   

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)