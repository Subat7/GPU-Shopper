#from asyncio.windows_events import NULL
import psycopg2
import subprocess
import os
from flask import Flask, send_from_directory, request, jsonify
import json
import requests
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
from bs4 import BeautifulSoup
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
 
api_names = ["neweggapi","bestbuyapi","amazonapi"]
inStockRegister = []

app = Flask(__name__,
           static_url_path='',
           static_folder = 'build')

@app.route('/', defaults={'path': ''})
@app.route("/<string:path>")
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder+ '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
 
 
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
    print(table_info)
    HerokuExecutionSQL("INSERT INTO " + Table + " VALUES ("+ "\'" + table_info[0]  + "\'"  + ", "+"\'" + table_info[1]  + "\'"+", "+"\'" + table_info[2]  + "\'"+", "+"\'" + table_info[3]  + "\'" + ", "+ "\'" + table_info[4] + "\'" + ", "+ "\'" + table_info[5] + "\'" + ");")
    print("Updated ", Table, "'s table with gpu - ", table_info[0],";")
 
#delete from location
@app.route('/DeleteFromAPITable')
def DeleteFromAPITable(Table, table_info):
    HerokuExecutionSQL("DELETE FROM " + Table + " WHERE gpu = " + "\'" + table_info[0] + "\'" + ";")
    print("deleted from ", Table, "'s table with gpu - ", table_info[0],";")
    


############################### Print Functions #######################################

@app.route('/print_api_results', methods = ['POST'])
def print_api_results():

    sizeData = []
    rowSize = 0
    for i in range(len(api_names)):
        sizeData = herokuRetrieveData("SELECT  count(*) as row_size FROM "  + api_names[i] + ";")
        rowSize += sizeData[0][0]

    dataList = [{}] * rowSize
    count = 0
    for i in range(len(api_names)):

        results = herokuRetrieveData("SELECT * FROM " + api_names[i] + ";")
      
        for i in range(len(results)):

            dictList = { 'label' : results[i][0], 'price': results[i][1], 'url': results[i][3], 'image': results[i][4], 'stock': results[i][2], 'item number': results[i][5]}
            dataList[i+count] = dictList

        count+= len(results)
        #print(count)

    print("Search Completed")
    final = json.dumps(dataList, indent=2)
    #print(final)
    return final

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

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)



############################### Heroku SQL Command Calls ##############################

def HerokuExecutionSQL(Input):
    HEROKU_APP_NAME = "botproject-csce315"
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    # DATABASE_URL = os.environ['DATABASE_URL']
    # conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = conn.cursor()
    cursor.execute(Input)
    conn.commit()
    cursor.close()
    conn.close()

def herokuRetrieveData(command):
        ## access table and return users table list[tuple[4], tuple [4]]
        HEROKU_APP_NAME = "botproject-csce315"
        # connection and execution
        conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
        connuri = conn_info.stdout.decode('utf-8').strip()
        conn = psycopg2.connect(connuri)
        # DATABASE_URL = os.environ['DATABASE_URL']
        # conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        cursor = conn.cursor()
        cursor.execute(command)
        listData = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return listData


############################### Email and Tracking List ################################

def email_send(Username, Info):
#BotNetGPUs@gmail.com Email Info
#Password: BotNetisCool1234
    EMAIL_ADDRESS = 'BotNetGPUs@gmail.com'
    EMAIL_PASSWORD = 'BotNetisCool1234'

    print("Within email send")
    #print(Info)

    #msg = EmailMessage()
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Bot Net GPUS Notification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = Username

    Intro = "Dear " + Username + "<br>" + "These GPUs are currently in-stock for a limited time!<br>"

    html = """\
    <html>
        <body>
            <p>""" + Intro + """</p>
        </body>
    </html>
    """

    for i in Info:

        gpuListingInfo = i[0] + "<br>" + "Price: " + i[1] + "<br>" + " URL: " + i[3] + "<br>" 

        # set an alternative html body
        html += """\
        <html>
            <body>
                <img  src = """ + i[4] + """ width: "100" height: "100" >
                <p>""" + gpuListingInfo + """</p>
            </body>
        </html>
        """

    part = MIMEText(html, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
        print("email sent")
        smtp.quit()


def emailList():

    trackingList = herokuRetrieveData("SELECT * FROM users;")
    userList = herokuRetrieveData("SELECT DISTINCT email FROM users;")


    for i in userList:
        inStockUserList = []
        for j in trackingList:
            flag = False

            if i[0] == j[0]:

                for k in inStockRegister:
                    #print("Comparing " + k[0] + " with " + j[1])
                    if k[0] == j[1] and j[3] == '0': #checking if gpu names equal to the instock register and what is in the tracking list as well as if the stock is 0 meaning the user hasnt been emailed
                        #GPUS added to email list are set to 1 for stock to signify the person has been emailed for this GPU already and not to repeat
                        HerokuExecutionSQL("UPDATE users" + " SET stock = " + '\'' + "1" + '\'' + " WHERE email = " + '\'' + i[0] + '\''+" and gpu_name = " + '\'' + j[1] + '\''+ ";") 
                        inStockUserList.append(k)
                        flag = True
                        break
                    elif k[0] == j[1] and j[3] == '1':
                        flag = True
                        print("Email already sent before")
                        break
            
                if flag == False and j[3] == '1':
                    HerokuExecutionSQL("UPDATE users" + " SET stock = " + '\'' + "0" + '\'' + " WHERE email = " + '\'' + i[0] + '\''+" and gpu_name = " + '\'' + j[1] + '\''+ ";") 
        


        #print(inStockUserList)
        if len(inStockUserList) != 0:
            email_send(i[0], inStockUserList)
        else:
            print("No tracking list matches for user: " + i[0])



############################### Tracking Table Functionality ##########################
user_email_account = ""
#add in a new user/call every time 
@app.route('/update_users', methods=['POST']) 
def update_users():
    UserEmail = ""
    global user_email_account

    if request.method == 'POST':
       data = json.loads(request.data)
       UserEmail = data['UserEmail']
       user_email_account = UserEmail
       print(UserEmail)

    return user_email_account


@app.route('/addUserTracking',methods=['POST'])
def addUserTracking():
    email = user_email_account

    gpu=[]
    if request.method == 'POST':
       data = json.loads(request.data)
       #print(data)
       gpu.append(data['selectedGPU']['label'])
       gpu.append(data['selectedGPU']['price']) 
       gpu.append(data['selectedGPU']['stock']) 
       gpu.append(data['selectedGPU']['url']) 
       gpu.append(data['selectedGPU']['image']) 
    #    gpu.append(data['selectedGPU']['item number']) 
       #print(data)

    dataExists = herokuRetrieveData("SELECT email, gpu_name FROM users WHERE email = " + "'" + email + "'" + "and gpu_name = " + "'" + gpu[0] + "'" + ";")
    #print(dataExists)

    if len(dataExists) == 0:

        HerokuExecutionSQL("INSERT INTO users VALUES(" + "'"+ email + "'," + "'" + gpu[0] + "'," + "'" + gpu[1] + "'," + "'" + "0" + "'," + "'" + gpu[3] + "'," + "'" + gpu[4] + "'" + ");")
        print("Updated User " + email + " tracking list with " + gpu[0])

    else:
        print("Tracking for " + gpu[0] + " for user " + email + " already in database")

    return data



@app.route('/removeUserTracking',methods=['POST'])
def removeUserTracking():
    email = user_email_account
    gpu=[]
    if request.method == 'POST':
       data = json.loads(request.data)
       #print(data)
       gpu.append(data['selectedGPU']['label'])
       gpu.append(data['selectedGPU']['price']) 
    #    gpu.append(data['selectedGPU']['stock']) 
    #    gpu.append(data['selectedGPU']['url']) 
    #    gpu.append(data['selectedGPU']['image']) 
    #    gpu.append(data['selectedGPU']['item number']) 
       #print(data)

    dataExists = herokuRetrieveData("SELECT email, gpu_name FROM users WHERE email = " + "'" + email + "'" + "and gpu_name = " + "'" + gpu[0] + "'" + ";")
    #print(dataExists)

    if len(dataExists) == 0:

        print("Tracking for " + gpu[0] + " for user " + email + " has already been removed")

    else:
        HerokuExecutionSQL("DELETE FROM users WHERE email = " + "'" + email + "'" + "and gpu_name = " + "'" + gpu[0] + "'" + " AND price = '"+gpu[1]+"';")
        print("Removed Users " + email + " tracking of " + gpu[0] + " from list" )
    return "Done"

@app.route('/retrieveTrackingList', methods=['POST'])
def retrieveTrackingList():

    sizeData = []
    rowSize = 0
    sizeData = herokuRetrieveData("SELECT  count(*) as row_size FROM users WHERE email = '"+user_email_account+"';")
    rowSize += sizeData[0][0]

    dataList = [{}] * rowSize
    count = 0

    results = herokuRetrieveData("SELECT * FROM users WHERE email = '"+user_email_account+"';")

    for i in range(len(results)):
        dictList = { 'label' : results[i][1], 'price': results[i][2], 'stock': results[i][3], 'url': results[i][4], 'image_url': results[i][5]} #leave out email
        dataList[i+count] = dictList

    count+= len(results)
    #print(count)

    #print("Search Completed")
    trackingList = json.dumps(dataList, indent=2)
    #print(trackingList)
    return trackingList


############################### API CALLS #############################################

def apiUpdateStock(apiTable):

    apiData = herokuRetrieveData("Select * FROM " + apiTable + ";")
    inStockRegister = []

    for i in apiData:
        if apiTable == 'bestbuyapi':
            sku = i[5]
            stock = i[2]
            newData = bestbuyAPI(sku)
            updatedStock = newData[2]
            
            if stock != updatedStock:
                HerokuExecutionSQL("UPDATE " + apiTable + " SET stock = " + '\'' + updatedStock + '\'' + " WHERE sku = " + '\'' + sku + '\''+ ";")

            if updatedStock == '1':
                inStockRegister.append(newData)


        elif apiTable == 'neweggapi':
            url = i[3]
            itemNum = i[5]
            stock = i[2]
            newData = neweggCall(url)
            updatedStock = newData[2]
            
            if stock != updatedStock:
                HerokuExecutionSQL("UPDATE " + apiTable + " SET stock = " + '\'' + updatedStock + '\'' + " WHERE item_number = " + '\'' + itemNum + '\''+ ";")

            if updatedStock == '1':
                inStockRegister.append(newData)

        elif apiTable == 'amazonapi':
            asin = i[5]
            stock = i[2]
            newData = amazonAPI(asin)
            updatedStock = newData[2]
            
            if stock != updatedStock:
                HerokuExecutionSQL("UPDATE " + apiTable + " SET stock = " + '\'' + updatedStock + '\'' + " WHERE asin = " + '\'' + asin + '\''+ ";")

            if updatedStock == '1':
                inStockRegister.append(newData)

    #print(inStockRegister)
    return inStockRegister


def neweggCall(url):

    #print("Running Newegg Api")

    urls = url

    response = requests.get(urls).text

    #print(response)

    pageData = BeautifulSoup(response, "html.parser")
    nameGPU = pageData.find("h1", {"class": "product-title"}).text
    priceGPU = pageData.find("li", {"class": "price-current"}).text
    urlGPU = urls
    imageGPU = pageData.find("img", {"class": "product-view-img-original", "src" : True})['src']
    stockGPU = pageData.find("div", {"class": "product-inventory"}).text
    itemNumGPU = pageData.find("em").text

    strResponse = {'name': nameGPU, 'price': priceGPU, 'url': urlGPU, 'image': imageGPU, 'stock': stockGPU, 'item number': itemNumGPU}

    nameGPU = strResponse['name'] #name key used to retrive GPU name from response dictionary
    priceGPU = str(strResponse['price'])#price key used to retrive GPU price from response dictionary
    urlGPU = strResponse['url']#url key used to retrive GPU url listing from response dictionary
    imageGPU = strResponse['image']#image key used to retrive GPU image url from response dictionary
    itemNumGPU = str(strResponse['item number'])#item number key used to retrive GPU image url from response dictionary


    if strResponse['stock'] != ' OUT OF STOCK.': # checking GPU stock state from response
        stockGPU = '1' #if in stock set stock to 1 
    else:
        stockGPU = '0' #if not in stock set stock to 0

    dataList = [nameGPU, priceGPU, stockGPU, urlGPU, imageGPU, itemNumGPU ]

    return dataList

    #print(dataList)


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

    nameGPU = strResponse['name'] #name key used to retrive GPU name from response dictionary
    priceGPU = str(strResponse['price'])#price key used to retrive GPU price from response dictionary
    urlGPU = strResponse['link']#link key used to retrive GPU url listing from response dictionary
    imageGPU = strResponse['image']#image key used to retrive GPU image url from response dictionary

    if strResponse['soldout'] == False: #soldout key used to retrive GPU stock from response dictionary
        stockGPU = '1' #if in stock set stock to 1 
    else:
        stockGPU = '0' #if not in stock set stock to 0

    dataList = [nameGPU, priceGPU, stockGPU, urlGPU, imageGPU]
    #print(dataList)

    return dataList




#API KEY: qhqws47nyvgze2mq3qx4jadt
#Request Limit: 50,000/day and 5/second
#Provides:
#Name
#Availability -- False or True
#Price
#SKU
def bestbuyAPI(sku):
    #print("Running Best Buy Api")

    time.sleep(0.3)
    url = "https://api.bestbuy.com/v1/products/" + str(sku) + ".json?apiKey=qhqws47nyvgze2mq3qx4jadt&show=sku,name,salePrice,onlineAvailability,image,url" #<----- Change SKU to request details for specifc GPU : /products/SKU

    response = requests.request("GET", url)

    #jprint(response.json())

    strResponse = response.json()

    nameGPU = strResponse['name'] #name key used to retrive GPU name from response dictionary
    priceGPU = str(strResponse['salePrice'])#salePrice key used to retrive GPU price from response dictionary
    urlGPU = strResponse['url']#url key used to retrive GPU url listing from response dictionary
    imageGPU = strResponse['image']#image key used to retrive GPU image url from response dictionary
    skuGPU = str(strResponse['sku'])#sku key used to retrive GPU image url from response dictionary

    if strResponse['onlineAvailability'] == True: #onlineAvailability key used to retrive GPU stock from response dictionary
        stockGPU = '1' #if in stock set stock to 1 
    else:
        stockGPU = '0' #if not in stock set stock to 0

    dataList = [nameGPU, priceGPU, stockGPU, urlGPU, imageGPU, skuGPU]
    #print(dataList)

    return dataList


#Request Limit: 5,000/Month
#Change Amazon product key(ASIN) at the end of URL to retrieve GPU info from listing
#Provides:
#Pricing ---> if NULL then its out of stock
#Available Quanity 
def amazonAPI(asin):
    #print("Running Amazon Api")

    url = "https://amazon24.p.rapidapi.com/api/product/" + asin #<----Product Key(ASIN)

    querystring = {"country":"US"}

    headers = {
        "X-RapidAPI-Host": "amazon24.p.rapidapi.com",
        "X-RapidAPI-Key": "c921f8d06amsh9d092ba59855fe5p1d3e4ajsn23ea68d6d328"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #jprint(response.json()) 

    strResponse = response.json() #Response is retrieved as json which within python is made a Dictionary data type=

    nameGPU = strResponse['product_title']#product_title key used to retrive GPU name from response dictionary

    if 'app_sale_price' in strResponse:
        priceGPU = str(strResponse['app_sale_price'])#app_sale_price key used to retrive GPU price from response dictionary
    else:
        priceGPU = str(strResponse['price_information']['app_sale_price'])#['price_information']['app_sale_price'] key used to retrive GPU price from response dictionary
    
    urlGPU = strResponse['product_detail_url']#product_detail_url key used to retrive GPU url listing from response dictionary
    imageGPU = strResponse['product_main_image_url']#product_main_image_url key used to retrive GPU image url from response dictionary
    asinGPU = str(strResponse['product_id'])


    if priceGPU != 'None': #availabe_quanity key used to retrive GPU stock from response dictionary
        stockGPU = '1' #if in stock set stock to 1 
    else:
        stockGPU = '0' #if not in stock set stock to 0

    dataList = [nameGPU, priceGPU, stockGPU, urlGPU, imageGPU, asinGPU]
    #print(dataList)

    return dataList

#######################################################################################

def main_call_frame():
    #O(n^2) longest funciton in the program
    print("API LIST CALLED " + api_names[0] + " " + api_names[1] + " " + api_names[2])
    global inStockRegister

    inStockRegister = []


    #################API's are called to check stock of current GPUs in database#######################
    inStockRegister += apiUpdateStock('bestbuyapi')
    #inStockRegister += apiUpdateStock('amazonapi'); ### Disabled due to having a 5000/month limit so its not constantly running
    inStockRegister+= apiUpdateStock('neweggapi')

    emailList()

    return inStockRegister

    # if any stock are at a values other than 0 send the reminder

# ## this code makes the call go out once every day    
# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler(timezone='MST')
# scheduler.add_job(main_call_frame, 'interval', seconds=30)
# scheduler.start()
