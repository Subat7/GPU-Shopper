#from asyncio.windows_events import NULL
import psycopg2
import subprocess
import os
from flask import Flask, send_from_directory, request, jsonify
import json
import requests
import smtplib
from email.message import EmailMessage
 
api_names = ["neweggapi","bestbuyapi","amazonapi"]
list_of_users = ['developer1']

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
    print(Table)
    print(table_info[0])
    HerokuExecutionSQL("INSERT INTO " + Table + " VALUES ("+ "\'" + table_info[0]  + "\'"  + ", "+"\'" + table_info[1]  + "\'"+","+"\'" + table_info[2]  + "\'"+", "+"\'" + table_info[3]  + "\'"+");")
    print("Updated ", Table, "'s table with gpu - ", table_info[0],";")
 
#delete from location
@app.route('/DeleteFromAPITable')
def DeleteFromAPITable(Table, table_info):
    HerokuExecutionSQL("DELETE FROM TABLE " + Table + " WHERE gpu = " + "\'" + table_info[0] + "\'" + ";")
    print("deleted from ", Table, "'s table with gpu - ", table_info[0],";")
#cycling

#add in a new user/call every time 
@app.route('/update_users') 
def update_users(UserEmail):
    if UserEmail in list_of_users:
        print("Already in the database")
        return False
    else:
        print("Entered new user" + UserEmail)
        list_of_users.add(UserEmail)
    return True

#Serch
@app.route('/Searching', methods=['POST'])
def Searching(Input1):
    #Input1 = ""
    #if request.method == 'POST':
    #    data = json.loads(request.data)
    #    Input1 = data['Search']
    # a part or complete match
    search_results = []
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    for i in range(len(api_names)):
        cursor.execute("SELECT * FROM "+api_names[i]+" WHERE gpu LIKE '%"+ Input1 +"%' OR gpu LIKE '"+ Input1 +"%';") 
        search_results += cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    print("Search Completed")
    return search_results

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
############################################################################### print function ## fixed
@app.route('/print_api_results')
def print_api_results():
    search_results_print = []
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    for i in range(len(api_names)):
        cursor.execute("SELECT * FROM " + api_names[i] + ";")
        search_results_print += cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    print("Search Completed")
    return search_results_print

@app.route('/print_tracker_list')
def print_tracker_list(tracker_list_username):
    search_results_print = []
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM " + tracker_list_username + ";")
    search_results_print += cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    print("Search Completed")
    return search_results_print
######################call abck to recall api's#################################
regester = [] # stores all with a stock of > 0

def api_call():
    # get n based on input or just get all n's
    a = amazonAPI() # [[1,2,3,4,5]]
    b = neweggAPI()
    c = bestbuyAPI()
    # -> one 2d list
    n = a + b + c
    print(n)
    return n


def herokuExecute(command):
        ## access table and return users table list[tuple[4], tuple [4]]
        HEROKU_APP_NAME = "botproject-csce315"
        # connection and execution
        conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
        connuri = conn_info.stdout.decode('utf-8').strip()
        conn = psycopg2.connect(connuri)
        cursor = conn.cursor()
        cursor.execute(command)
        listData = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return listData


def email_send(Username, Info):
#BotNetGPUs@gmail.com Email Info
#Password: BotNetisCool1234
    EMAIL_ADDRESS = 'BotNetGPUs@gmail.com'
    EMAIL_PASSWORD = 'BotNetisCool1234'
    # a list of tuple quadrapairs
    Information_parsed = "Dear " + Username + ", \n \t These GPU's are currently in-stock for a limited time!"
    for I in range(len(Info)):
        #Information_parsed += "Name: \n" + Info[I][0] + "Price: \n" + Info[I][1]+" URL: \n" + Info[I][3] + " \n" 

        Information_parsed += "Hello this is BotNet" + Info 
# me == the sender's email address
# you == the recipient's email address
    msg = EmailMessage()
    msg['Subject'] = "Bot Net GPUS Notification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = Username + '@gmail.com'
    msg.set_content(Information_parsed)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        print("email sent")
        smtp.quit()


@app.route('/email_list')
def email_list(regester):
    # called in the main call frame
    for i in list_of_users:
        info = []
        Username = i

        strCommand = "Select * From " + Username +";"
        Tracking_List = herokuExecute(strCommand)

        print(i)
        ## access regester and return regester table list[strings]
        for j in range(len(Tracking_List)):
            for z in range(len(regester)):
                #[1,2,3,4,1,2,3,4,1,2,3,4]
                #0,4,8, ENDS
                if((z*4) >= len(regester)):
                    print("No matches")
                    break
                elif(Tracking_List[j][0] == regester[0+z*4]):
                    # send email here
                    info += Tracking_List[j]
                    print("added info")
        #email_send(Username,info)
    #Might wanna do this in the main call frame...


def main_call_frame():
    #O(n^2) longest funciton in the program
    print("API LIST CALLED" + api_names[0] + api_names[1] + api_names[2])
    regester = [] # stores all with a stock of > 0
    a = amazonAPI() # [[1,2,3,4,5]]
    b = neweggAPI()
    c = bestbuyAPI()
    for i in range(len(a)):
        name = "amazonapi"
        #try: 
            #test the delete function seperately as this is very important
        DeleteFromAPITable(name, a[i]) # will error so if it does that means it doesnt exist thus continue
        #except Exception:
        #    pass
        print(a[i])
        InsertIntoAPITable(name, a[i])
        if(int(a[i][2]) > 0):
            regester += a[i]
    for i in range(len(b)):
        name = "neweggapi"
        try: 
            #test the delete function seperately as this is very important
            DeleteFromAPITable(name, b[i]) # will error so if it does that means it doesnt exist thus continue
        except Exception:
            pass
        InsertIntoAPITable(name, b[i])
        if(int(b[i][2]) > 0):
            regester += b[i]
    for i in range(len(c)):
        name = "bestbuyapi"
        try: 
            #test the delete function seperately as this is very important
            DeleteFromAPITable(name, c[i]) # will error so if it does that means it doesnt exist thus continue
        except Exception:
            pass
        InsertIntoAPITable(name, c[i])
        if(int(c[i][2]) > 0):
            regester += c[i]  
    return regester         
    # if any stock are at a values other than 0 send the reminder

## this code makes the call go out once every day    
# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(main_call_frame(['']), 'interval', hours=24)
# scheduler.start()



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

    strResponse = response.json()

    #print(strResponse)



    #n = [['GIGABYTE Eagle RTX 3070 Ti','699.99','1','Normal_URL', 'Image_URL']]
    #return n



#API KEY: qhqws47nyvgze2mq3qx4jadt
#Request Limit: 50,000/day and 5/second
#Provides:
#Name
#Availability -- False or True
#Price
#SKU
def bestbuyAPI():
    url = "https://api.bestbuy.com/v1/products/6439402.json?apiKey=qhqws47nyvgze2mq3qx4jadt&show=sku,name,salePrice,onlineAvailability,image,url" #<----- Change SKU to request details for specifc GPU : /products/SKU

    response = requests.request("GET", url)

    #jprint(response.json())

    strResponse = response.json()

    nameGPU = strResponse['name'] #name key used to retrive GPU name from response dictionary
    priceGPU = str(strResponse['salePrice'])#salePrice key used to retrive GPU price from response dictionary
    urlGPU = strResponse['url']#url key used to retrive GPU url listing from response dictionary
    imageGPU = strResponse['image']#image key used to retrive GPU image url from response dictionary

    if strResponse['onlineAvailability'] == True: #onlineAvailability key used to retrive GPU stock from response dictionary
        stockGPU = '1' #if in stock set stock to 1 
    else:
        stockGPU = '0' #if not in stock set stock to 0

    dataList = [[nameGPU, priceGPU, stockGPU, urlGPU, imageGPU]]
    print(dataList)

    return dataList



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

    #jprint(response.json()) 

    strResponse = response.json() #Response is retrieved as json which within python is made a Dictionary data type=

    print(strResponse['product_title'])

    nameGPU = strResponse['product_title']#product_title key used to retrive GPU name from response dictionary
    priceGPU = str(strResponse['currency'])#currency key used to retrive GPU price from response dictionary
    urlGPU = strResponse['product_detail_url']#product_detail_url key used to retrive GPU url listing from response dictionary
    imageGPU = strResponse['product_main_image_url']#product_main_image_url key used to retrive GPU image url from response dictionary

    if strResponse['available_quantity'] != 0: #availabe_quanity key used to retrive GPU stock from response dictionary
        stockGPU = '1' #if in stock set stock to 1 
    else:
        stockGPU = '0' #if not in stock set stock to 0

    dataList = [[nameGPU, priceGPU, stockGPU, urlGPU, imageGPU]]
    print(dataList)

    return dataList



#email_send("daviddk226", "1234")
amazonAPI()




