import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

TOTAL_START_TIME = time.time()
POOL = Pool(50)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'gladminds')
MIGRATE_DB = os.environ.get('MIGRATE_DB','gladmindsdb')
OFFSET = int(os.environ.get('OFFSET',0))



DB_OLD = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base

CUR_OLD = DB_OLD.cursor()

CUR_OLD.execute("select d.*, a.* from aftersell_serviceadvisor as d, auth_user as a where d.service_advisor_id=a.username")
SA_DATA = CUR_OLD.fetchall()
DB_OLD.close()

FILE = open('service_advisor.out', 'a+')

def process_query(data):
    active_asc=active_dealer=None
    status='N'
    db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                         user=DB_USER, # your username
                          passwd=DB_PASSWORD, # your password
                          db="bajaj") # name of the data base
    
    cur_new = db_new.cursor()
    db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db=MIGRATE_DB) # name of the data base
    cur_old = db_old.cursor()
    try:
        today = datetime.now()
        cur_new.execute("INSERT INTO auth_user (password, last_login, is_superuser, \
        username, first_name, last_name, email, is_staff, is_active, date_joined)\
            VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)",(data.get('password'),
                data.get('last_login'), data.get('is_superuser'),data.get('username'),
                data.get('name'), data.get('last_name'), data.get('email'),
                data.get('is_staff'), data.get('is_active'),
                data.get('date_joined')))
        
        query = "select id from auth_user where username  = %(username)s"
        cur_new.execute(query, {'username': data.get('username')})
        sa = cur_new.fetchall()[0]
        
        cur_new.execute("INSERT INTO bajaj_userprofile (user_id, address,\
         created_date, modified_date, phone_number) VALUES (%s, %s, %s, %s, %s)",(sa[0],
                                            data.get('address'), today, today, data.get('phone_number')))
        
        query2 = "select * from bajaj_userprofile where user_id  = %(user_id)s"
        cur_new.execute(query2, {'user_id': sa[0]})
        sa_pro = cur_new.fetchall()[0]
        
        
        #fetch the associated dealer
        query3 = "select dealer_id_id, status from \
        aftersell_serviceadvisordealerrelationship where\
        service_advisor_id_id= %(service_advisor_id_id)s"
        cur_old.execute(query3, {'service_advisor_id_id': data.get('id')})
        sa_dealer_data = cur_old.fetchone()
        
        if sa_dealer_data:
            query4 = "select * from aftersell_registereddealer where id  = %(id)s"
            cur_old.execute(query4, {'id': sa_dealer_data[0]})
            asstd_dealer = cur_old.fetchone()
            if asstd_dealer[3]=='asc':
                query5 = "select * from bajaj_authorizedservicecenter where asc_id  = %(asc_id)s"
                cur_new.execute(query5, {'asc_id': asstd_dealer[1]})
                active_asc = cur_new.fetchone()[3]
                
            else:
                query5 = "select * from bajaj_dealer where dealer_id  = %(dealer_id)s"
                cur_new.execute(query5, {'dealer_id': asstd_dealer[1]})
                active_dealer = cur_new.fetchone()[3]
            status=sa_dealer_data[1]
            
        cur_new.execute("INSERT INTO bajaj_serviceadvisor (user_id, \
        service_advisor_id, status, dealer_id, asc_id, created_date, \
        modified_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",(sa_pro[11],
        data.get('service_advisor_id'),
        status, active_dealer, active_asc, today, today))
        
        
        cur_new.execute("select * from auth_group where name = 'sas'")
        sa_group = cur_new.fetchall()[0]
        
        cur_new.execute("INSERT INTO auth_user_groups (user_id, group_id)\
          VALUES (%s, %s)",(sa[0], sa_group[0]))
        db_new.commit()
    except Exception as ex:
        db_new.rollback()
        e='[Error]: {0} {1}'.format(data.get('service_advisor_id'), ex)
        FILE.write(str(e) + '\n')
    db_new.close()
    db_old.close()

def format_data(dealer_data):
    dealers=[]
    for data in dealer_data:
        temp = {}
        temp['id'] = data[0]
        temp['service_advisor_id'] = data[1]
        temp['name'] = data[2]
        temp['phone_number'] = data[3]
        temp['order'] = data[4]
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

format_data(SA_DATA)
TOTAL_END_TIME = time.time()
FILE.write(str("..........Total TIME TAKEN......... {0}".format(TOTAL_END_TIME-TOTAL_START_TIME)) + '\n')
FILE.close()