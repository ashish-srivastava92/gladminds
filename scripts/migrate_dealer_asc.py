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

cur_old.execute("select d.*, a.* from aftersell_registereddealer as d, auth_user as a where d.dealer_id=a.username and d.role!='asc'")
dealer_data = cur_old.fetchall()

cur_old.execute("select d.*, a.* from aftersell_registereddealer as d, auth_user as a where d.dealer_id=a.username and d.role='asc' and d.id='1379'")
asc_data = cur_old.fetchall()

def process_query(data):
    print "----------------------------------", cur_new
    print "dealer", data.get('dealer_id')
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
        dealer = cur_new.fetchall()[0]
        print "fetched dealer", dealer[0]
        
        cur_new.execute("INSERT INTO bajaj_userprofile (user_id, address, created_date, modified_date) VALUES (%s, %s, %s, %s)",(dealer[0], data.get('address'), today, today))
        print "created userprofile"
        
        query2 = "select * from bajaj_userprofile where user_id  = %(user_id)s"
        cur_new.execute(query2, {'user_id': dealer[0]})
        dealer_pro = cur_new.fetchall()[0]
        print "fetched dealer profile", dealer_pro[11]
         
#         cur_new.execute("INSERT INTO bajaj_dealer (user_id, dealer_id, created_date, modified_date) VALUES (%s, %s, %s, %s)",(dealer_pro[11], data.get('dealer_id'), today, today))
#         print "created dealer"

        dealer_dependent=data.get('dependent_on')
        print "----------------", dealer_dependent
        if dealer_dependent:
            query3 = "select * from bajaj_dealer where dealer_id  = %(dealer_id)s"
            cur_new.execute(query3, {'dealer_id': dealer_dependent})
            dealer_dep = cur_new.fetchall()[0]
            dealer_dependent=dealer_dep[3]
            print "fetched dependent dealer profile", dealer_dependent
        cur_new.execute("INSERT INTO bajaj_authorizedservicecenter (user_id, asc_id, created_date, modified_date, dealer_id) VALUES (%s, %s, %s, %s, %s)",(dealer_pro[11], data.get('dealer_id'), today, today, dealer_dependent))
        print "created asc"
# 
        cur_new.execute("select * from auth_group where name = 'ascs'")       
#         cur_new.execute("select * from auth_group where name = 'dealers'")

        dealer_group = cur_new.fetchall()[0]
        print "Fetched dealer group"
        
        cur_new.execute("INSERT INTO auth_user_groups (user_id, group_id)\
          VALUES (%s, %s)",(dealer[0], dealer_group[0]))
        print "created user goup"
        db_new.commit()
        print "---------------DONE--------------------"
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
    pool.map(process_query, dealers)
    end_time = time.time()