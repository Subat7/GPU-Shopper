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
    n = cursor.execute("SELECT * FROM Users WHERE Username = " + "\'"+ Input1 + "\'" + " AND Password = " + "\'"+ Input2 + "\'" + ";")
    if n != "":
    	print ("Access Granted:" + Input1)
    	return True
    #conn.commit()
    cursor.close()
    conn.close()

LoginValidation("developer1", "T33")