from flask import *
from openpyxl import load_workbook
import requests
import json
import sys
sys.path.append('apicommon')
import apicommon
import base64
  
app = Flask(__name__) #creating the Flask class object   
app=Flask(__name__,template_folder='templates')
 
@app.route('/') #decorator drfines the   
def index():
    book = load_workbook("account_group.xlsx")
    sheet = book.active
    return render_template('login.html',sheet=sheet) 

@app.route('/account_group/',methods=['GET', 'POST'])  
def home():
    ulstr=[]
    gid=""
    glid=""
    passwd=""
    if request.method == 'POST':
        gid = request.form.get('group_account')
        glid = request.form.get('group_account_list')
        passwd = request.form.get('pass')
            
    if gid!="":        
        userpass = apicommon.clientId+":"+apicommon.skey
        auth_access=base64.b64encode(userpass.encode()).decode()
        payload='grant_type=client_credentials'
        headers = {
        'Authorization': "Basic :"+auth_access,
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", apicommon.aurl, headers=headers, data=payload)
        access_token = (json.loads(response.content)["access_token"])
        headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-BT-Pagination-Total':''
        }
        bearer="Bearer "+access_token
        pNo=0
        exNo=0
        perPage=100
        n=0
        
        for number in range(0, 100):
            if exNo==0:
                pNo = pNo+1
                url = apicommon.epurl+"/api/config/v1/vault/account?account_group_id="+str(gid)+"&per_page="+str(perPage)+"&current_page="+str(pNo)
                cl_resp = requests.request("GET", url, headers=headers, data=payload)
                resp = json.loads(cl_resp.text)       
                tot_len=len(resp)        
                if tot_len==perPage:
                    for i in resp:
                        n=n+1  
                        ulstr.append(str(i["id"])+","+str(i["name"]))                    
                elif tot_len<perPage:
                    if exNo==0:
                        for i in resp:
                            n=n+1
                            ulstr.append(str(i["id"])+","+str(i["name"])) 
                        exNo=1
                        tot_len=0
                    else:
                        exit
                
        if passwd!="":
            url1 = "https://nwncarousel.beyondtrustcloud.com/api/config/v1/vault/account/"+glid
            payload1 = json.dumps({
              "password": passwd,
              "private_key": passwd
            })
            headers1 = {
              'Content-Type': 'application/json',
              'Authorization': f'Bearer {access_token}',
            }
            response = requests.request("PATCH", url1, headers=headers1, data=payload1)
            print(response)
    book = load_workbook("account_group.xlsx")
    sheet = book.active
    return render_template('login.html',sheet=sheet,len = len(ulstr), ulstr = ulstr,gid=gid,glid=glid,passwd=passwd)   

@app.route('/login',methods = ['POST'])  
def login():  
      uname=request.form['uname']  
      passwrd=request.form['pass']  
      if uname=="ayush" and passwrd=="google":  
          return "Welcome %s" %uname  
    
if __name__ =='__main__':  
    app.run(debug = True)