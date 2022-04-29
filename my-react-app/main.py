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
 
api_names = ["neweggapi","bestbuyapi","amazonapi"]
inStockRegister = []

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
    print(table_info)
    HerokuExecutionSQL("INSERT INTO " + Table + " VALUES ("+ "\'" + table_info[0]  + "\'"  + ", "+"\'" + table_info[1]  + "\'"+", "+"\'" + table_info[2]  + "\'"+", "+"\'" + table_info[3]  + "\'" + ", "+ "\'" + table_info[4] + "\'" + ", "+ "\'" + table_info[5] + "\'" + ");")
    print("Updated ", Table, "'s table with gpu - ", table_info[0],";")
 
#delete from location
@app.route('/DeleteFromAPITable')
def DeleteFromAPITable(Table, table_info):
    HerokuExecutionSQL("DELETE FROM " + Table + " WHERE gpu = " + "\'" + table_info[0] + "\'" + ";")
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

############################### Print Functions #######################################

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

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)



############################### Heroku SQL Command Calls ##############################

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

def herokuRetrieveData(command):
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


############################### Email and Tracking List ################################

def email_send(Username, Info):
#BotNetGPUs@gmail.com Email Info
#Password: BotNetisCool1234
    EMAIL_ADDRESS = 'BotNetGPUs@gmail.com'
    EMAIL_PASSWORD = 'BotNetisCool1234'

    Intro = "Dear " + Username + "<br>" + "These GPUs are currently in-stock for a limited time!<br>"
    gpuListingInfo = Info[0] + "<br>" + "Price: " + Info[1] + "<br>" + " URL: " + Info[3] + "<br>" 



    #msg = EmailMessage()
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Bot Net GPUS Notification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = Username + '@gmail.com'
    #msg.set_content(Information_parsed)

    # now create a Content-ID for the image
    image_cid = make_msgid(domain="")
    # if `domain` argument isn't provided, it will 
    # use your computer's name

    # set an alternative html body
    html = """\
    <html>
        <body>
            <p>""" + Intro + """</p>
            <img  src = """ + Info[4] + """ width: "100" height: "100" >
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

######## LEFT TO DO ############
#Automize the cross checking user tracking lists with in-stock GPUs
#to then send corresponding emails to those user
 
@app.route('/email_list')
def email_list(register):
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






############################### API CALLS #############################################

def apiUpdateStock(apiTable):

    apiData = herokuRetrieveData("Select * FROM " + apiTable + ";")
    inStockRegister = [];

    for i in apiData:
        if apiTable == 'bestbuyapi':
            sku = i[5]
            stock = i[2]
            newData = bestbuyAPI(sku)
            updatedStock = newData[2]
            
            if stock != updatedStock:
                HerokuExecutionSQL("UPDATE " + apiTable + " SET stock = " + '\'' + updatedStock + '\'' + " WHERE sku = " + '\'' + sku + '\''+ ";")

            if updatedStock == '1':
                inStockRegister += newData


        elif apiTable == 'neweggapi':
            url = i[3]
            itemNum = i[5]
            stock = i[2]
            newData = neweggCall(url)
            updatedStock = newData[2]
            
            if stock != updatedStock:
                HerokuExecutionSQL("UPDATE " + apiTable + " SET stock = " + '\'' + updatedStock + '\'' + " WHERE item_number = " + '\'' + itemNum + '\''+ ";")

            if updatedStock == '1':
                inStockRegister += newData

        elif apiTable == 'amazonapi':
            asin = i[5]
            stock = i[2]
            newData = amazonAPI(asin)
            updatedStock = newData[2]
            
            if stock != updatedStock:
                HerokuExecutionSQL("UPDATE " + apiTable + " SET stock = " + '\'' + updatedStock + '\'' + " WHERE asin = " + '\'' + asin + '\''+ ";")

            if updatedStock == '1':
                inStockRegister += newData

    print(inStockRegister)
    return inStockRegister


def neweggCall(url):

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
    register = [] # stores all with a stock of > 0


    #################API's are called to check stock of current GPUs in database#######################
    register += apiUpdateStock('bestbuyapi');
    #register += apiUpdateStock('amazonapi'); ### Disabled due to having a 5000/month limit so its not constantly running
    register += apiUpdateStock('neweggapi');

    # #################################
    # for i in range(len(a)):
    #     name = "amazonapi"
    #     try: 
    #         #test the delete function seperately as this is very important
    #         DeleteFromAPITable(name, a[i]) # will error so if it does that means it doesnt exist thus continue
    #     except Exception:
    #         pass

    #     InsertIntoAPITable(name, a[i])
    #     if(int(a[i][2]) > 0):
    #         regester += a[i]

    # #################################
    # for i in range(len(b)):
    #     name = "neweggapi"
    #     try: 
    #         #test the delete function seperately as this is very important
    #         DeleteFromAPITable(name, b[i]) # will error so if it does that means it doesnt exist thus continue
    #     except Exception:
    #         pass

    #     InsertIntoAPITable(name, b[i])
    #     if(int(b[i][2]) > 0):
    #         regester += b[i]

    # #################################
    # for i in range(len(c)):
    #     name = "bestbuyapi"
    #     try: 
    #         #test the delete function seperately as this is very important
    #         DeleteFromAPITable(name, c[i]) # will error so if it does that means it doesnt exist thus continue
    #     except Exception:
    #         pass

    #     InsertIntoAPITable(name, c[i])
    #     if(int(c[i][2]) > 0):
    #         regester += c[i]  

    return register         
    # if any stock are at a values other than 0 send the reminder

## this code makes the call go out once every day    
# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(main_call_frame(['']), 'interval', hours=24)
# scheduler.start()




######################Used to initialize api data tables###############################

##Insert intial gpu data into bestbuy data table##
# gpuList = [6496088, 6467840, 6501113, 6475237, 6439402, 6429442, 6465789, 6429440, 6462956, 6429434, 6502626]

# for i in gpuList:

#     gpuData = bestbuyAPI(i);

#     #print(gpuData)

#     InsertIntoAPITable("bestbuyapi", gpuData)


##Insert intial gpu data into amazon data table##
# gpuList = ["B09QH9NT3V", "B096WM6JFS", "B09CBS8ZF3", "B0971BG25M", "B09719T6FT", "B097J5CZTJ", "B097CMQVF4", "B08KTWVHQP", "B08L8L71SM", "B091MNBNWT", "B08L8LG4M3" ]

# for i in gpuList:

#     print("Current GPU being retrieved:" + i)

#     gpuData = amazonAPI(i);


#     InsertIntoAPITable("amazonapi", gpuData)


##Insert intial gpu data into newegg data table##
# gpuList = ["https://www.newegg.com/asus-geforce-rtx-3070-ti-tuf-rtx3070ti-o8g-gaming/p/N82E16814126512?Item=N82E16814126512&Description=RTX%20CARD&cm_re=RTX_CARD-_-14-126-512-_-Product",
#     "https://www.newegg.com/msi-geforce-rtx-3070-ti-rtx-3070-ti-suprim-x-8g/p/N82E16814137665?Item=N82E16814137665&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-137-665-_-Product&quicklink=true",
#     "https://www.newegg.com/gigabyte-geforce-rtx-3060-gv-n3060eagle-oc-12gd/p/N82E16814932434?Item=N82E16814932434&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-932-434-_-Product",
#     "https://www.newegg.com/evga-geforce-rtx-3050-08g-p5-3553-kr/p/N82E16814487555?Item=N82E16814487555&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-487-555-_-Product",
#     "https://www.newegg.com/evga-geforce-rtx-3080-12g-p5-4865-kl/p/N82E16814487557?Item=N82E16814487557&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-487-557-_-Product&quicklink=true",
#     "https://www.newegg.com/asus-geforce-rtx-3060-ph-rtx3060-12g-v2/p/N82E16814126532?Item=N82E16814126532&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-126-532-_-Product",
#     "https://www.newegg.com/asus-geforce-rtx-3070-ko-rtx3070-o8g-v2-gaming/p/N82E16814126530?Item=N82E16814126530&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-126-530-_-Product",
#     "https://www.newegg.com/zotac-geforce-rtx-3070-zt-a3070f-10p/p/N82E16814500512?Item=N82E16814500512&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-500-512-_-Product",
#     "https://www.newegg.com/asus-geforce-rtx-3080-rtx3080-o10g-wht-v2/p/N82E16814126533?Item=N82E16814126533&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-126-533-_-Product",
#     "https://www.newegg.com/asus-geforce-rtx-3090-ti-tuf-rtx3090ti-o24g-gaming/p/N82E16814126555?Item=N82E16814126555&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-126-555-_-Product",
#     "https://www.newegg.com/msi-geforce-rtx-3050-rtx-3050-ventus-2x8g/p/N82E16814137715?Item=N82E16814137715&Description=rtx%20graphics%20card&cm_re=rtx_graphics%20card-_-14-137-715-_-Product"]

# for i in gpuList:

#     #print("Current GPU being retrieved:" + i)

#     gpuData = neweggCall(i);

#     InsertIntoAPITable("neweggapi", gpuData)

#######################################################################################

# gpuData = bestbuyAPI(6467840);
# email_send("daviddk226", gpuData)

# liststock = main_call_frame()
# print(liststock)


