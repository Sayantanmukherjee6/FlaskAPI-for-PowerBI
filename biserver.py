from flask import  Flask, render_template, flash
from flask import jsonify
from flask import Flask,g,request,session
import requests,pyodbc,urllib2
from urllib2 import Request,urlopen
from embedtoken import EmbedToken


app = Flask(__name__)

clientid=
clientsecret=
username=
password=
groupid=
datasetid= 
reportid=
tablename= 

def updateData(dist,access_token, dataset_id, table_name): 

    initial_json="""
         {
             "rows": ["""
    middle_json = ""
    end_json = """]
          }
        """
    each = 0

    saleinvoiceid = []
    saleorderid = []
    productid = []
    amount = []
    saleorderdate = []
    saleinvoicedate = []
    distributor_id = []
    distributor_name = []
    delivery_address = []
    product_name = []
    orderqty = []
    gross_amount = []
    net_amount = []

    if (dist=="All Distributors"):
        cnxn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=DELHI;Trusted_Connection=yes;')
        cursor = cnxn.cursor()  
        cursor.execute(" select top(2000) a.SALEINVOICEID,a.SALEORDERID,a.PRODUCTID,a.AMOUNT,CONVERT(nvarchar,a.SALEORDERDATE , 106) as SALEORDERDATE,CONVERT(nvarchar,b.SALEINVOICEDATE , 106) as SALEINVOICEDATE,b.DISTRIBUTORID,b.DISTRIBUTORNAME,b.DELIVERYADDRESS,c.PRODUCTNAME,c.ORDERQTY,d.GROSSAMOUNT,d.NETAMOUNT from DELHI.dbo.T_SALEINVOICE_DETAILS a,DELHI.dbo.T_SALEINVOICE_HEADER b,DELHI.dbo.T_SALEORDER_DETAILS c,DELHI.dbo.T_SALEINVOICE_FOOTER d where a.SALEINVOICEID = b.SALEINVOICEID and a.SALEORDERID = c.SALEORDERID and a.SALEINVOICEID = d.SALEINVOICEID")
        for row in cursor:
            saleinvoiceid.append(str(row[0]))
            saleorderid.append(str(row[1]))
            productid.append(str(row[2]))
            amount.append(float(row[3]))
            saleorderdate.append(str(row[4]))
            saleinvoicedate.append(str(row[5]))
            distributor_id.append(str(row[6]))
            distributor_name.append(str(row[7]))
            delivery_address.append(str(row[8]))
            product_name.append(unicode(row[9]).encode('utf-8'))
            orderqty.append(str(row[10]))
            gross_amount.append(float(row[11]))
            net_amount.append(float(row[12]))
        
        cnxn.close()

    else:
        cnxn = pyodbc.connect(r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=DELHI;Trusted_Connection=yes;')
        cursor = cnxn.cursor()  
        cursor.execute(" select top(2000) a.SALEINVOICEID,a.SALEORDERID,a.PRODUCTID,a.AMOUNT,CONVERT(nvarchar,a.SALEORDERDATE , 106) as SALEORDERDATE,CONVERT(nvarchar,b.SALEINVOICEDATE , 106) as SALEINVOICEDATE,b.DISTRIBUTORID,b.DISTRIBUTORNAME,b.DELIVERYADDRESS,c.PRODUCTNAME,c.ORDERQTY,d.GROSSAMOUNT,d.NETAMOUNT from DELHI.dbo.T_SALEINVOICE_DETAILS a,DELHI.dbo.T_SALEINVOICE_HEADER b,DELHI.dbo.T_SALEORDER_DETAILS c,DELHI.dbo.T_SALEINVOICE_FOOTER d where a.SALEINVOICEID = b.SALEINVOICEID and a.SALEORDERID = c.SALEORDERID and a.SALEINVOICEID = d.SALEINVOICEID and b.DISTRIBUTORNAME='"+dist+"'")
        for row in cursor:
            saleinvoiceid.append(str(row[0]))
            saleorderid.append(str(row[1]))
            productid.append(str(row[2]))
            amount.append(float(row[3]))
            saleorderdate.append(str(row[4]))
            saleinvoicedate.append(str(row[5]))
            distributor_id.append(str(row[6]))
            distributor_name.append(str(row[7]))
            delivery_address.append(str(row[8]))
            product_name.append(unicode(row[9]).encode('utf-8'))
            orderqty.append(str(row[10]))
            gross_amount.append(float(row[11]))
            net_amount.append(float(row[12]))
            
        cnxn.close()


    while each<len(amount):
         
        content =  """{
                "productid": '"""+productid[each]+"""',
                "amount": """+str(float(amount[each]))+""",
                "saleinvoicedate": '"""+saleinvoicedate[each]+"""',
                "distributor_name": '"""+distributor_name[each]+"""',
                "delivery_address": '"""+delivery_address[each]+"""',
                "product_name": '"""+product_name[each]+"""',
                "orderqty": '"""+orderqty[each]+"""',
                "gross_amount": """+str(float(gross_amount[each]))+""",
                "net_amount": """+str(float(net_amount[each]))+""",

              },"""
        middle_json = middle_json+content
        each=each+1

    values = initial_json+middle_json+end_json
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }

    response = requests.post('https://api.powerbi.com/v1.0/myorg/groups/'+groupid+'/datasets/'+dataset_id+'/tables/'+table_name+'/rows', data=values, headers=headers)
    
    print response


def get_access_token():
    data = {
        'grant_type': 'password',
        'resource': r'https://analysis.windows.net/powerbi/api',
        'client_id': clientid ,
        'client_secret': clientsecret ,
        'username': username,
        'password': password
    }
    response = requests.post('https://login.microsoftonline.com/common/oauth2/token', data=data)
    return response.json()

def clear_dataset(access_token, dataset_id, table_name):
    headers = {
            'Authorization': 'Bearer ' + access_token
        }
    request = Request(
            'https://api.powerbi.com/v1.0/myorg/groups/'+groupid+'/datasets/'+dataset_id+'/tables/'+table_name+'/rows',headers=headers)
    request.get_method = lambda: 'DELETE'

    response_body = urlopen(request).read()
    return response_body


@app.route('/token',methods=['GET','POST'])
def bidemotoken():
    data=request.form["key1"]
    if data=="sendToken":
        a=get_access_token()
        conf = EmbedToken(str(a['access_token']),username,password,clientid,clientsecret,reportid,groupid)
        token = conf.get_embed_token()
        print token
        returnData = {'selectedReport':token.get('report_id'),'embedToken':token.get('token')}
        return jsonify(returnData)

  
@app.route('/api',methods=['GET','POST'])
def bidemodata():
    data=request.form["key2"]
    a=get_access_token() #access_token
    clear_dataset(str(a['access_token']), datasetid, tablename)
    updateData(data,str(a['access_token']), datasetid, tablename)   
    return "Report Updated"


if __name__ == '__main__':
    app.run()
