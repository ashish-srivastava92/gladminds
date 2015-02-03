from django.db import connections
from gladminds.core.core_utils.utils import dictfetchall
from gladminds.core.constants import CouponStatus
import logging

logger = logging.getLogger("gladminds")

def update_coupon_history_table():
    logger.info("updating_coupon_history_data")
#     query_coupon = "select status,count(*) as count from bajaj_coupondata c where \
#     DATE(c.created_date)=DATE_SUB(CURDATE(), INTERVAL 1 DAY) group by status;"
    query_coupon = "select status,count(*) as count from bajaj_coupondata c group by status;"
#     query_coupon_history_daily = 'select * from bajaj_couponfact c inner join bajaj_datedimension d on \
#     c.date_id=d.date_id where d.date=DATE_SUB(CURDATE(), INTERVAL 2 DAY) and data_type="DAILY"'
#     query_coupon_history_total = 'select * from bajaj_couponfact c inner join bajaj_datedimension d on \
#     c.date_id=d.date_id where d.date=DATE_SUB(CURDATE(), INTERVAL 2 DAY) and data_type!="DAILY"'
    date_query = 'select date_id from bajaj_datedimension d where d.date=DATE_SUB(CURDATE(), INTERVAL 1 DAY)'
    conn = connections['bajaj']
    cursor = conn.cursor()
    cursor.execute(query_coupon)
    data_coupon = dictfetchall(cursor)
    cursor.execute(date_query)
    date_data = dictfetchall(cursor)
    coupon_count = {}
    for data in data_coupon:
        coupon_count[data['status']] = data['count']
#     cursor.execute(query_coupon_history_daily)
#     data_coupon_history_daily = dictfetchall(cursor)
#     cursor.execute(query_coupon_history_total)
#     data_coupon_history_total = dictfetchall(cursor)
    params = {}
    params['inprogress'] = coupon_count.get(CouponStatus.IN_PROGRESS, 0) 
    params['closed'] = coupon_count.get(CouponStatus.CLOSED, 0)
    params['unused'] = coupon_count.get(CouponStatus.UNUSED, 0)
    params['exceeds'] = coupon_count.get(CouponStatus.EXCEEDS_LIMIT, 0)
    params['expired'] = coupon_count.get(CouponStatus.EXPIRED, 0)
    params['data_type'] = 'TOTAL'
    params['date_id'] = date_data[0]['date_id']
    insert_query = 'insert into bajaj_couponfact(date_id, inprogress, closed, expired, unused, exceeds, data_type) \
    values(%(date_id)s, %(inprogress)s,%(closed)s,%(expired)s,%(unused)s,%(exceeds)s, %(data_type)s)'
    delete_query = 'delete from bajaj_couponfact where date_id = %(date_id)s and data_type=%(data_type)s'
    update_query = 'UPDATE `bajaj_couponfact SET inprogress`=%(inprogress),closed`=%(closed) \
    expired`=%(expired), unused`=%(unused) WHERE date_id =%(date_id)s'
    try:
        cursor.execute(insert_query, params)
    except:
        cursor.execute(update_query, params)
    conn.close()

