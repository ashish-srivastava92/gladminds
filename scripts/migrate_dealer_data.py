import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

POOL = Pool(50)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'gladminds')
MIGRATE_DB = os.environ.get('MIGRATE_DB','gladmindsdb')
OFFSET = int(os.environ.get('OFFSET',0))
TOTAL_START_TIME = time.time()


DB_OLD = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

CUR_OLD = DB_OLD.cursor()

CUR_OLD.execute("select d.*, a.* from aftersell_registereddealer as d,\
                auth_user as a where d.dealer_id=a.username and d.role!='asc'")
DEALER_DATA = CUR_OLD.fetchall()

DB_OLD.close()
FILE = open('dealer.out', 'a+')

def process_query(data):
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

    cur_new = db_new.cursor()
    try:
        today = datetime.now()
        cur_new.execute("INSERT INTO auth_user (password, last_login, is_superuser, \
        username, first_name, last_name, email, is_staff, is_active, date_joined)\
            VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)",(data.get('password'),
                data.get('last_login'), data.get('is_superuser'),data.get('username'),
                data.get('first_name'), data.get('last_name'), data.get('email'),
                data.get('is_staff'), data.get('is_active'),
                data.get('date_joined')))
        
        query = "select id from auth_user where username  = %(username)s"
        cur_new.execute(query, {'username': data.get('username')})
        dealer = cur_new.fetchall()[0]
        
        cur_new.execute("INSERT INTO bajaj_userprofile (user_id, address, created_date, modified_date) VALUES (%s, %s, %s, %s)",(dealer[0], data.get('address'), today, today))
        
        query2 = "select * from bajaj_userprofile where user_id  = %(user_id)s"
        cur_new.execute(query2, {'user_id': dealer[0]})
        dealer_pro = cur_new.fetchall()[0]
         
        cur_new.execute("INSERT INTO bajaj_dealer (user_id, dealer_id, created_date, modified_date) VALUES (%s, %s, %s, %s)",(dealer_pro[11], data.get('dealer_id'), today, today))

        cur_new.execute("select * from auth_group where name = 'Dealers'")

        dealer_group = cur_new.fetchall()[0]
        
        cur_new.execute("INSERT INTO auth_user_groups (user_id, group_id)\
          VALUES (%s, %s)",(dealer[0], dealer_group[0]))
        db_new.commit()
    except Exception as ex:
        db_new.rollback()
        e='[Error]: {0} {1}'.format(data.get('dealer_id'), ex)
        FILE.write(str(e) + '\n')
    db_new.close()

def format_data(dealer_data):
    dealers=[]
    for data in dealer_data:
        temp = {}
        temp['id'] = data[0]
        temp['dealer_id'] = data[1]
        temp['address'] = data[2]
        temp['role'] = data[3]
        temp['dependent_on'] = data[4]
        temp['password'] = data[6]
        temp['last_login'] = data[7]
        temp['is_superuser'] = data[8]
        temp['username'] = data[9]
        temp['first_name'] = ' '
        temp['last_name'] = ' '
        temp['email'] = data[12]
        temp['is_staff'] = data[13]
        temp['is_active'] = data[14]
        temp['date_joined'] = data[15]
        dealers.append(temp)
    POOL.map(process_query, dealers)
    
format_data(DEALER_DATA)
TOTAL_END_TIME = time.time()
FILE.write(str("..........Total TIME TAKEN......... {0}".format(TOTAL_END_TIME-TOTAL_START_TIME)) + '\n')
FILE.close()