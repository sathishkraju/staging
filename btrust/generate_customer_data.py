import requests
import json
import sys
sys.path.append('../config')
import config
import base64
import xlsxwriter
userpass = config.clientId+":"+config.skey
auth_access=base64.b64encode(userpass.encode()).decode()

payload='grant_type=client_credentials'
headers = {
  'Authorization': "Basic :"+auth_access,
  'Content-Type': 'application/x-www-form-urlencoded',
}
response = requests.request("POST", config.aurl, headers=headers, data=payload)
access_token = (json.loads(response.content)["access_token"])
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'X-BT-Pagination-Total':''
}
bearer="Bearer "+access_token
com_file='account_group.xlsx';
xlsx_File = xlsxwriter.Workbook(com_file)
bold = xlsx_File.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'color':'white',
    'fg_color': '#1e4f87'})
merge_format = xlsx_File.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'color':'white',
    'fg_color': '#879b20'})

payload = "{subject:TestSubject,description:TestDescription,priority:Very Low}"
headers = {
  'Authorization': bearer,
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
pNo=0
exNo=0
perPage=100
n=0
sheet_schedule = xlsx_File.add_worksheet("Account Group")
sheet_schedule.write(0,0,"Id",bold)
sheet_schedule.write(0,1,"Name",bold)
for number in range(0, 100):
    if exNo==0:
        pNo = pNo+1
        url = config.epurl+"/api/config/v1/vault/account-group?per_page="+str(perPage)+"&current_page="+str(pNo)
        cl_resp = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(cl_resp.text)       
        tot_len=len(resp)        
        if tot_len==perPage:
            for i in resp:
                n=n+1                
                sheet_schedule.write(n,0,str(i["id"]))
                sheet_schedule.write(n,1,str(i["name"]))
        elif tot_len<perPage:
            if exNo==0:
                for i in resp:
                    n=n+1
                    sheet_schedule.write(n,0,str(i["id"]))
                    sheet_schedule.write(n,1,str(i["name"]))
                exNo=1
                tot_len=0
            else:
                exit
xlsx_File.close()    