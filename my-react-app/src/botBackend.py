import os
import psycopg2
import subprocess
#import mySql

# 


# def retrieveURL():

# 	# Running the following from Python: $heroku config:get DATABASE_URL --app your-app-name
# 	heroku_app_name = "botproject-csce315"
# 	raw_db_url = subprocess.run(
# 	    ["heroku", "config:get", "DATABASE_URL", "--app", heroku_app_name],
# 	    capture_output=True  # capture_output arg is added in Python 3.7
# 	).stdout 

# 	# Convert binary string to a regular string & remove the newline character
# 	db_url = raw_db_url.decode("ascii").strip()

# 	# Convert "postgres://<db_address>"  --> "postgresql+psycopg2://<db_address>" needed for SQLAlchemy
# 	final_db_url = "postgresql+psycopg2://" + db_url.lstrip("postgres://")  # lstrip() is more suitable here than replace() function since we only want to replace postgres at the start!

# 	return final_ db_url
#     #sudo su postgres -c passed
#     #su postgres -c psql template1brexddb_url


# # read database connection url from the enivron variable we just set.
# DATABASE_URL = os.environ.get(retrieveURL())
# con = None
# try:
#     # create a new database connection by calling the connect() function
#     con = psycopg2.connect(DATABASE_URL, sslmode = 'require')

#     #  create a new cursor
#     cur = conn.cursor()
    
#     # execute an SQL statement to get the HerokuPostgres database version
#     print('PostgreSQL database version:')
#     cur.execute('SELECT version()')

#     # display the PostgreSQL database server version
#     db_version = cur.fetchone()
#     print(db_version)
       
#      # close the communication with the HerokuPostgres
#     cur.close()
# except Exception as error:
#     print('Cause: {}'.format(error))

# finally:
#     # close the communication with the database server by calling the close()
#     if con is not None:
#         con.close()
#         print('Database connection closed.')

HEROKU_APP_NAME = "botproject-csce315"
#TABLE_NAME = "the_table_you_want_to_query_in_this_example"
import subprocess, psycopg2

conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", HEROKU_APP_NAME], stdout = subprocess.PIPE)
connuri = conn_info.stdout.decode('utf-8').strip()
conn = psycopg2.connect(connuri)
cursor = conn.cursor()
cursor.execute("CREATE TABLE Newegg (id SERIAL PRIMARY KEY, gpu_name VARCHAR(255) NOT NULL)")
#count = cursor.fetchall()
#print(count)
conn.commit();
cursor.close()
conn.close()


