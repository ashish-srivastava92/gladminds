import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

MIGRATE_DB = os.environ.get('MIGRATE_DB','gladminds')
db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

cur_old = db_old.cursor()  

db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

cur_new = db_new.cursor() 

'''In case the service advisor has no auth_user entry'''
cur_old.execute("select * from aftersell_serviceadvisor")
sa_data = cur_old.fetchall()

def process_query(data):
    active_asc=active_dealer=None
    status='N'
    print "-------------------------------------------"
    print "service advisor", data.get('service_advisor_id')
    try:
        today = datetime.now()
        cur_old.execute("INSERT INTO auth_user (password, last_login, is_superuser, \
        username, first_name, last_name, email, is_staff, is_active, date_joined)\
            VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)",(data.get('password'),
                data.get('last_login'), data.get('is_superuser'),data.get('username'),
                data.get('first_name'), data.get('last_name'), data.get('email'),
                data.get('is_staff'), data.get('is_active'),
                data.get('date_joined')))
        print "created user"
        db_old.commit()
        print "---------------DONE-----------------------"
    except Exception as ex:
        db_old.rollback()
        print "----------------------something went wrong--------------------", ex

        
def format_data(dealer_data):
     start_time = time.time()
     pool = Pool(1)
     dealers=[]
     today = datetime.now()
     for data in dealer_data:
         temp = {}
         temp['id'] = data[0]
         temp['service_advisor_id'] = data[1]
         temp['name'] = data[2]
         temp['phone_number'] = data[3]
         temp['order'] = data[4]
         temp['password'] = data[1]+'@123'
         temp['last_login'] = today
         temp['is_superuser'] = 0
         temp['username'] = data[1]
         temp['first_name'] = ' '
         temp['last_name'] = ' '
         temp['email'] = ''
         temp['is_staff'] = 0
         temp['is_active'] = 1
         temp['date_joined'] = today
         dealers.append(temp)
     pool.map(process_query, dealers)
     end_time = time.time()
     print "..........Total TIME TAKEN.........", end_time-start_time
     
format_data(sa_data)