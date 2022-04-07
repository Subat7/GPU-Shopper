#from asyncio.windows_events import NULL
import psycopg2
import subprocess

def LoginValidation(Input1, Input2):
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    n = ""
    cursor.execute("SELECT * FROM Users WHERE Username = " + "\'"+ Input1 + "\'" + " AND Password = " + "\'"+ Input2 + "\'" + ";")
    n = cursor.fetchone()
    cursor.close()
    conn.close()
    #print(n)
    if type(n) != type(None):
    	print ("Access Granted:" + Input1)
    	return True
    else:
    	print("Incorrect Info")
    	return False


############################### NEEDS TO BE TESTES ##############################
def EnterUserToTable(Username, Password):
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users VALUES(" + "\'"+ Username + "\'," + "\'" + Password + "\'," + '0, 0);')
    conn.commit()
    cursor.close()
    conn.close()
    print("Updated Users Table with -", Username)

############################### NEEDS TO BE TESTES ##############################
def RemoveUserFromTable(Username):
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE Username = " + "\'" + Username + "\';")
    conn.commit()
    cursor.close()
    conn.close()
    print("Deleted -", Username, "- From the table Users")   

############################### NEEDS TO BE TESTES ##############################
def UpdateEmail(Username, Email):
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Email ="  + "\'" + Email  + "\'" + "WHERE Username = "  + "\'" + Username  + "\';")
    conn.commit()
    cursor.close()
    conn.close()
    print("Updated User -", Username, " - with Email -", Email)

############################### NEEDS TO BE TESTES ##############################
def UpdatePhone(Username, Phone):
    HEROKU_APP_NAME = "botproject-csce315"
    import subprocess, psycopg2
    # connection and execution
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    conn = psycopg2.connect(connuri)
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET Phone ="  + "\'" + Phone  + "\'" + "WHERE Username = "  + "\'" + Username  + "\';")
    conn.commit()
    cursor.close()
    conn.close()
    print("Updated User -", Username, " - with Phone -", Phone)


inputUser = input()
#inputPass = input()

RemoveUserFromTable(inputUser)