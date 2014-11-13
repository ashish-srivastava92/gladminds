import MySQLdb
import time
import os
from multiprocessing.dummy import Pool
from datetime import datetime

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

db_old = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="gladminds") # name of the data base

cur_old = db_old.cursor() 

db_new = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASSWORD, # your password
                      db="bajaj") # name of the data base

cur_new = db_new.cursor() 

cur_old.execute("select d.*, a.* from aftersell_serviceadvisor as d, auth_user as a where d.service_advisor_id=a.username")
sa_data = cur_old.fetchall()

def process_query(data):
    active_asc=active_dealer=None
    status='N'
    print "-------------------------------------------"
    print "service advisor", data.get('service_advisor_id')
    try:
        today = datetime.now()
        cur_new.execute("INSERT INTO auth_user (password, last_login, is_superuser, \
        username, first_name, last_name, email, is_staff, is_active, date_joined)\
            VALUES (%s, %s, %s, %s, %s, %s, %s,  %s, %s, %s)",(data.get('password'),
                data.get('last_login'), data.get('is_superuser'),data.get('username'),
                data.get('first_name'), data.get('last_name'), data.get('email'),
                data.get('is_staff'), data.get('is_active'),
                data.get('date_joined')))
        print "created user"
        
        query = "select id from auth_user where username  = %(username)s"
        cur_new.execute(query, {'username': data.get('username')})
        sa = cur_new.fetchall()[0]
        print "fetched service advisor user", sa[0]
        
        cur_new.execute("INSERT INTO bajaj_userprofile (user_id, address,\
         created_date, modified_date) VALUES (%s, %s, %s, %s)",(sa[0],
                                            data.get('address'), today, today))
        print "created service advisor profile"
        
        query2 = "select * from bajaj_userprofile where user_id  = %(user_id)s"
        cur_new.execute(query2, {'user_id': sa[0]})
        sa_pro = cur_new.fetchall()[0]
        print "fetched service advisor profile", sa_pro[11]
        
        #fetch the associated dealer
        query3 = "select dealer_id_id, status from \
        aftersell_serviceadvisordealerrelationship where\
        service_advisor_id_id= %(service_advisor_id_id)s"
        print "---------------- sa id", data.get('id')
        cur_old.execute(query3, {'service_advisor_id_id': data.get('id')})
        sa_dealer_data = cur_old.fetchone()
        print "----------------------- Got dealer-sa", sa_dealer_data
        if sa_dealer_data:
            query4 = "select * from aftersell_registereddealer where id  = %(id)s"
            cur_old.execute(query4, {'id': sa_dealer_data[0]})
            asstd_dealer = cur_old.fetchone()
            print "--------------- fetched associated dealer", asstd_dealer
            if asstd_dealer[3]=='asc':
                query5 = "select * from bajaj_authorizedservicecenter where asc_id  = %(asc_id)s"
                cur_new.execute(query5, {'asc_id': asstd_dealer[1]})
                active_asc = cur_new.fetchone()[3]
                
            else:
                query5 = "select * from bajaj_dealer where dealer_id  = %(dealer_id)s"
                cur_new.execute(query5, {'dealer_id': asstd_dealer[1]})
                active_dealer = cur_new.fetchone()[3]
            status=sa_dealer_data[1]
            
        print "-----Vaues--------------", active_asc, active_dealer, status
        print "-----Order--------------", data.get('order')
        cur_new.execute("INSERT INTO bajaj_serviceadvisor (user_id, \
        service_advisor_id, status, dealer_id, asc_id, created_date, \
        modified_date) VALUES (%s, %s, %s, %s, %s, %s, %s)",(sa_pro[11],
        data.get('service_advisor_id'),
        status, active_dealer, active_asc, today, today))
        print "created service advisor"
        
        
        cur_new.execute("select * from auth_group where name = 'sas'")
        sa_group = cur_new.fetchall()[0]
        print "Fetched service advisor group"
        
        cur_new.execute("INSERT INTO auth_user_groups (user_id, group_id)\
          VALUES (%s, %s)",(sa[0], sa_group[0]))
        print "created user service advisor"
        db_new.commit()
        print "---------------DONE-----------------------"
    except Exception as ex:
        db_new.rollback()
        print "----------------------something went wrong--------------------", ex

def format_data(dealer_data):
    start_time = time.time()
    pool = Pool(1)
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
    pool.map(process_query, dealers)
    end_time = time.time()


'''In case the service advisor has no auth_user entry'''
cur_old.execute("select * from aftersell_serviceadvisor")


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