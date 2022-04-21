#from asyncio.windows_events import NULL
import psycopg2
import subprocess
import os
from flask import Flask, send_from_directory, request, jsonify
import json
import requests
 
app = Flask(__name__,
           static_url_path='',
           static_folder = 'build')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder+ '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
 
#local function for connecting via a one input string
def HerokuExecutionSQL(Input):
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute(Input)
    conn.commit()
    cursor.close()
    conn.close()
 
@app.route('/LoginValidation',methods=['POST'])
def LoginValidation():
    userName = ""
    userPass = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        userName = data['userName']
        userPass = data['pass']
    #print(userName)
    #print(userPass)
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE Username = " + "\'"+ userName + "\'" + " AND Password = " + "\'"+ userPass + "\'" + ";")
    a = cursor.fetchall()
    print(a[0][0])
    print(a[0][1])
    if (userName == a[0][0] and userPass == a[0][1]) :
        print ("Access granted")
        return jsonify({"loggedIn": True})
    else:
        print("Incorrect Info")
        return jsonify({"loggedIn": False})
    cursor.close()
    conn.close()
 
@app.route('/EnterUserToTable',methods=['POST'])
def EnterUserToTable():
    userName = ""
    userPass = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        userName = data['userName']
        userPass = data['pass']
    HerokuExecutionSQL("INSERT INTO Users VALUES(" + "\'"+ userName + "\'," + "\'" + userPass + "\'," + '0, 0);')
    print("Updated Users Table with -", userName)
 
@app.route('/RemoveUserFromTable',methods=['POST'])
def RemoveUserFromTable():
    userName = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        userName = data['userName']
    HEROKU_APP_NAME = "botproject-csce315"
    HerokuExecutionSQL("DELETE FROM Users WHERE Username = " + "\'" + userName + "\';")
    print("Deleted -", userName, "- From the table Users")  
 
@app.route('/UpdateEmail',methods=['POST'])
def UpdateEmail():
    userName = ""
    userEmail = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        userName = data['userName']
        userEmail = data['Email']
    HerokuExecutionSQL("UPDATE Users SET Email ="  + "\'" + userEmail  + "\'" + "WHERE Username = "  + "\'" + userName  + "\';")
    print("Updated User -", userName, " - with Email -", userEmail)
 
############################### NEEDS TO BE TESTES ##############################
@app.route('/UpdatePhone',methods=['POST'])
def UpdatePhone():
    userName = ""
    userPhone = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        userName = data['userName']
        userPhone = data['Phone']
    HerokuExecutionSQL("UPDATE Users SET Phone ="  + "\'" + userPhone  + "\'" + "WHERE Username = "  + "\'" + userName  + "\';")
    print("Updated User -", userName, " - with Phone -", userPhone)
 

############################### Tracking List Back end ##############################
@app.route('/NewTrackingTable',methods=['POST'])
def NewTrackingTable():
    userName = ""
    if request.method == 'POST':
        data = json.loads(request.data)
        userName = data['userName']
    HerokuExecutionSQL("CREATE TABLE " + userName + " (Gpu TEXT, Price TEXT, Stock TEXT, Location_table TEXT);")
    print("Updated User -", userName, " - with New Table")
 
@app.route('/addtoTable')
def addtoTable(userName, api_gpu_info):
    gpu_name = api_gpu_info[0]
    gpu_price = api_gpu_info[1]
    gpu_stock = api_gpu_info[2]
    gpu_location = api_gpu_info[3]
    HerokuExecutionSQL("INSERT INTO " + userName + " VALUES ("+ "\'" + gpu_name  + "\'"  + ", "+"\'" + gpu_price  + "\'"+","+"\'" + gpu_stock  + "\'"+", "+"\'" + gpu_location  + "\'"+");")
    print("Updated User -", userName, "'s table with gpu - ", gpu_name,";")
 
@app.route('/deletefromTable')
def deletefromTable(userName, api_gpu_info):
    gpu_name = api_gpu_info[0]
    gpu_location = api_gpu_info[3]
    HerokuExecutionSQL("DELETE FROM " + userName + " WHERE gpu = " + "\'" + gpu_name + "\'" + " AND Location_table = " + "\'" + gpu_location + "\'" +" ;")
 
@app.route('/deleteEntireTable')
def deleteEntireTable(userName):
    HerokuExecutionSQL("DROP TABLE " + userName + ";")
 
############################### API Calls ##############################
#Assuming the API is in the 4 string list input  list[] = [s1,s2,s3,s4], Name of Table
#make table
@app.route('/MakeAPITable')
def MakeAPITable(Name):
    HerokuExecutionSQL("CREATE TABLE " + Name + " (Gpu TEXT, Price TEXT, Stock TEXT, URL TEXT);")
    print("Updated ", Name, " - with New Table")
 
#delete table
@app.route('/DeleteAPITable')
def DeleteAPITable(Name):
    HerokuExecutionSQL("DROP TABLE " + Name + ";")
 
#isert into location
@app.route('/InsertIntoAPITable')
def InsertIntoAPITable(Table, table_info):
    HerokuExecutionSQL("INSERT INTO " + Table + " VALUES ("+ "\'" + table_info[0]  + "\'"  + ", "+"\'" + table_info[1]  + "\'"+","+"\'" + table_info[2]  + "\'"+", "+"\'" + table_info[3]  + "\'"+");")
    print("Updated ", Table, "'s table with gpu - ", table_info[0],";")
 
#delete from location
@app.route('/DeleteFromAPITable')
def DeleteFromAPITable(Table, table_info):
    HerokuExecutionSQL("DELETE FROM TABLE " + Table + " WHERE Gpu = " + "\'" + table_info[0] + "\'" + " AND Price = "+ "\'" + table_info[1] + "\'" + " AND Stock = "+ "\'" + table_info[2] + "\'" + " AND URL = "+ "\'" + table_info[3] + "\'" +" ;")
    print("deleted from ", Table, "'s table with gpu - ", table_info[0],";")
#cycling
 
#Serch
@app.route('/Searching')
def Searching(Input, TableNames):
    # a part or complete match
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    for i in range(TableNames):
        n += cursor.execute("SELECT * FROM "+TableNames[i]+" WHERE gpu LIKE '%'"+Input+"'%' OR gpu LIKE '"+Input+"'%';")
    conn.commit()
    cursor.close()
    conn.close()
    print("Search Completed")
    return n
######### API'S ##############

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


#Request Limit: 20/day
#Change the URL to retrieve GPU information #WARNING: URL can only be from a listing where GPU is SOLD BY Newegg
#Provides:
#SKU
#Price
#Soldout -- False or True
def neweggAPI():

    url = "https://retail-store-product-information.p.rapidapi.com/getproductv2"

    querystring = {"url":"https://www.newegg.com/zotac-geforce-rtx-3060-ti-zt-a30610h-10mlhr/p/N82E16814500518"}

    headers = {
        "X-RapidAPI-Host": "retail-store-product-information.p.rapidapi.com",
        "X-RapidAPI-Key": "c921f8d06amsh9d092ba59855fe5p1d3e4ajsn23ea68d6d328"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    jprint(response.json())



#API KEY: qhqws47nyvgze2mq3qx4jadt
#Request Limit: 50,000/day and 5/second
#Provides:
#Name
#Availability -- False or True
#Price
#SKU
def bestbuyAPI():
    url = "https://api.bestbuy.com/v1/products/6439402.json?apiKey=qhqws47nyvgze2mq3qx4jadt&show=sku,name,salePrice,onlineAvailability" #<----- Change SKU to request details for specifc GPU : /products/SKU

    response = requests.request("GET", url)

    jprint(response.json())



#Request Limit: NONE
#Change Amazon product key(ASIN) at the end of URL to retrieve GPU info from listing
#Provides:
#Pricing ---> if NULL then its out of stock
#Available Quanity 
def amazonAPI():
    url = "https://amazon24.p.rapidapi.com/api/product/B09CLN62M9" #<----Product Key(ASIN)

    querystring = {"country":"US"}

    headers = {
        "X-RapidAPI-Host": "amazon24.p.rapidapi.com",
        "X-RapidAPI-Key": "c921f8d06amsh9d092ba59855fe5p1d3e4ajsn23ea68d6d328"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    jprint(response.json()) 


 
#neweggAPI()
# if __name__ == '__main__':
#     #app.run(debug=True)
#     app.run()






