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

''' To migrate UCN RECOVERY DATA'''

CUR_OLD.execute("SELECT c.*, a.username FROM aftersell_ucnrecovery as u, auth_user as a where u.user_id=a.id")
ucnrecover_data = CUR_OLD.fetchall()

DB_OLD.close()

def process_query_ucnrecover(data):
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

    cur_new = db_new.cursor() 
    try:
        today = datetime.now()
        query = "select id from auth_user where username  = %(username)s"
        cur_new.execute(query, {'username': data.get('username')})
        dealer = cur_new.fetchall()[0]
        
        query2 = "select * from bajaj_userprofile where user_id  = %(user_id)s"
        cur_new.execute(query2, {'user_id': dealer[0]})
        dealer_pro = cur_new.fetchall()[0]
        
        cur_new.execute("INSERT INTO bajaj_ucnrecovery (id, created_date, modified_date,\
        reason, customer_id, file_location, unique_service_coupon, user_id) VALUES\
         (%s, %s, %s, %s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        data.get('reason'), data.get('customer_id'),
        data.get('file_location'), data.get('unique_service_coupon'), dealer_pro[11]))
        
        db_new.commit()        
    except Exception as ex:
        db_new.rollback()
        print '[Error]:', data.get('id'), ex
    db_new.close()
    
 
def format_data_ucnrecover(ucnrecover_data):
    start_time = time.time()
    ucnrecovers=[]
    for data in ucnrecover_data:
        temp = {}
        temp['id'] = data[0]
        temp['reason'] = data[1]
        temp['user_id'] = data[2]
        temp['sap_customer_id'] = data[3]
        temp['file_location'] = data[4]
        temp['request_date'] = data[5]
        temp['unique_service_coupon'] = data[6]
        temp['username'] = data[7]
        ucnrecovers.append(temp)
    POOL.map(process_query_ucnrecover, ucnrecovers)
    end_time = time.time()
    print "..........Total TIME TAKEN.........", end_time-start_time

format_data_ucnrecover(ucnrecover_data)
