import MySQLdb
import time
from datetime import datetime
from multiprocessing.dummy import Pool

db_old = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="gladminds", # your password
                      db="gladmindsdb") # name of the data base

cur_old = db_old.cursor() 

db_new = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="gladminds", # your password
                      db="bajaj") # name of the data base

cur_new = db_new.cursor() 

cur_old.execute("SELECT r.*,c.unique_service_coupon,s.service_advisor_id FROM gladminds_serviceadvisorcouponrelationship as r, gladminds_coupondata as c, aftersell_serviceadvisor as s where r.unique_service_coupon_id=c.id and r.service_advisor_phone_id=s.id and c.unique_service_coupon in ('UJ00006', 'GJ01131')")
coupon_data = cur_old.fetchall()


def process_query(data):
    print "--------------------coupons--------------", data.get('unique_service_coupon')
    try:
        today = datetime.now()
        print "get the coupon", data.get('unique_service_coupon')
        query1 = "select * from bajaj_coupondata where unique_service_coupon  = %(unique_service_coupon)s"
        cur_new.execute(query1, {'unique_service_coupon': data.get('unique_service_coupon')})
        coupon = cur_new.fetchone()
        print "--------------- fetched associated coupon------------------------", coupon
        
        
        print "get the new sa", data.get('service_advisor_id')
        query2 = "select * from bajaj_serviceadvisor where service_advisor_id  = %(service_advisor_id)s"
        cur_new.execute(query2, {'service_advisor_id': data.get('service_advisor_id')})
        sa_new = cur_new.fetchone()
        sa=sa_new[4]
        
        print "---------------------coupon-sa------------------",coupon[0], sa    
        cur_new.execute("INSERT INTO bajaj_serviceadvisorcouponrelationship (id, created_date, modified_date,\
        unique_service_coupon_id, service_advisor_id) VALUES\
        (%s, %s, %s, %s, %s)",(data.get('id'),today, today,\
        coupon[0], sa))
        db_new.commit()
        print "---------------DONE--------------------"
    except Exception as ex:
        db_new.rollback()
        print "----------------------SOMETHING WENT WRONG--------------------", ex
    
 
def format_data(coupon_data):
    start_time = time.time()
    pool = Pool(1)
    coupons=[]
    for data in coupon_data:
        temp = {}
        temp['id'] = data[0]
        temp['unique_service_coupon_id'] = data[1]
        temp['service_advisor_phone_id'] = data[2]
        temp['unique_service_coupon'] = data[4]
        temp['service_advisor_id'] = data[5]
        coupons.append(temp)
    pool.map(process_query, coupons)
    end_time = time.time()

format_data(coupon_data)