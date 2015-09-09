from django.db import transaction, connections
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from gladminds.core.managers.audit_manager import sms_log
from gladminds.core.services import message_template as templates
from gladminds.core.model_fetcher import get_model
from gladminds.afterbuy import models as afterbuy_models
from gladminds.core.constants import COUPON_STATUS
from django.db.models.aggregates import Sum
import logging
from gladminds.core.core_utils.utils import dictfetchall
from django.conf import settings
import csv
import StringIO
from gladminds.core.auth_helper import GmApps

AUDIT_ACTION = "SENT TO QUEUE"
logger = logging.getLogger("gladminds")
service_dict = {}

@transaction.commit_manually()
def get_customers_to_send_reminder(*args, **kwargs):
    from gladminds.sqs_tasks import send_reminder_message
    day = kwargs.get('reminder_day', None)
    brand= kwargs.get('brand', None)
    today_date = datetime.now().date()
    reminder_date = datetime.now().date()+timedelta(days=day)
    results = get_model("CouponData", brand).objects.select_for_update().filter(mark_expired_on__range=(today_date,
                                    reminder_date), last_reminder_date__isnull=True,
                                    status=1).select_related('vin', 'customer_phone_number__phone_number')
    for reminder in results:
        product = reminder.vin
        phone_number = product.customer_phone_number.phone_number
        usc = reminder.unique_service_coupon
        vin = product.vin
        expired_date = reminder.mark_expired_on.strftime('%d/%m/%Y')
        valid_kms = reminder.valid_kms
        message = templates.get_template('SEND_CUSTOMER_COUPON_REMINDER').format(usc=usc, vin=vin, expired_date=expired_date, valid_kms=valid_kms)
        send_reminder_message.delay(phone_number=phone_number, message=message)
        sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
        reminder.last_reminder_date = datetime.now()
        reminder.save()
        user = get_model("UserProfile", brand).objects.filter(phone_number=phone_number)
        notification = afterbuy_models.UserNotification(user=user[0],message=message, notification_date=datetime.now(),
                                                        notification_read=0)
        notification.save()
    transaction.commit()
    
@transaction.commit_manually()  
def get_customers_to_send_reminder_by_admin(*args, **kwargs):
    from gladminds.sqs_tasks import send_reminder_message
    today = datetime.now().date()
    brand= kwargs.get('brand', None)
    results = get_model("CouponData", brand).objects.filter(schedule_reminder_date__day=today.day, schedule_reminder_date__month=today.month, schedule_reminder_date__year=today.year, status=1).select_related('product_id', 'customer_phone_number')
    for reminder in results:
        product_obj = reminder.product
        phone_number = product_obj.customer_phone_number
        usc = reminder.unique_service_coupon
        vin = product_obj.product_id
        expired_date = reminder.mark_expired_on.strftime('%d/%m/%Y')
        valid_kms = reminder.valid_kms
        message = templates.get_template('SEND_CUSTOMER_COUPON_REMINDER').format(usc=usc, vin=vin, expired_date=expired_date, valid_kms=valid_kms)
        send_reminder_message.delay(phone_number=phone_number, message=message)
        sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
        reminder.last_reminder_date = datetime.now()
        reminder.schedule_reminder_date = None
        reminder.save()
    transaction.commit()


def expire_service_coupon(*args, **kwargs):
    today = timezone.now()
    brand= kwargs.get('brand', None)
    threat_coupons = get_model("CouponData", brand).objects.filter(mark_expired_on__lte=today.date()).exclude(Q(status=2) | Q(status=3) | Q(status=6))
    for coupon in threat_coupons:
        #If the coupon was initiated, it will expire if initiated more than 30days ago.
        if coupon.status == COUPON_STATUS['In Progress']:
            extended_date = coupon.extended_date.date()
            if extended_date < today.date():
                coupon.status = COUPON_STATUS['Expired']
                coupon.save()
        #If the coupon is unused and crossed the days limit, it will expire.
        else:
            coupon.status = COUPON_STATUS['Expired']
            coupon.save()

def mark_feeback_to_closed(*args, **kwargs):
    brand= kwargs.get('brand', None)
    feedback_closed_date = datetime.now()-timedelta(days=2)
    get_model("Feedback", brand).objects.filter(status = 'Resolved', resloved_date__lte = feedback_closed_date )\
                                        .update(status = 'Closed', closed_date = datetime.now())

def import_data_from_sap(*args, **kwargs):
    pass

def get_data_feed_log_detail(start_date=None, end_date=None, brand=None):
    start_date = start_date
    end_date = end_date
    feed_logs = get_model("DataFeedLog", brand).objects.filter(timestamp__range=(start_date, end_date))
    return feed_logs.values('feed_type','action').annotate(total_count=Sum('total_data_count'),
                                                                  total_success_data_count=Sum('success_data_count'),
                                                                  total_failed_data_count=Sum('failed_data_count'))

def get_feed_failure_log_detail(feed_type=None, brand=None):
    feed_logs = get_model("FeedFailureLog", brand).objects.filter(email_flag=False, feed_type=feed_type)
    feed_data = []
    for feed in feed_logs:
        data = {}
        data['feed_type'] = feed.feed_type
        data['reason'] = feed.reason
        data['created_date'] = feed.created_date
        feed_data.append(data)
    return { 'feed_data':feed_data , 'feed_logs':feed_logs}

def get_customer_details(brand=None):
    customer_details = get_model("CustomerUpdateHistory", brand).objects.filter(email_flag=False, temp_customer__dealer_asc_id__isnull=False)
    customer_data = []
    for customer in customer_details:
        if customer.new_value != customer.old_value:
            data = {}
            data['dealer_asc_id'] = customer.temp_customer.dealer_asc_id
            data['customer_id'] = customer.temp_customer.temp_customer_id
            data['customer_name'] = customer.temp_customer.new_customer_name
            data['new_number'] = customer.new_value
            data['old_number'] = customer.old_value
            data['modified_date'] = customer.modified_date
            customer_data.append(data)
    return {'customer_data' : customer_data, 'customer_details':customer_details}

def get_update_number_exceeds(brand=None):
    update_details = get_model("CustomerUpdateFailure", brand).objects.filter(email_flag=False, updated_by__isnull=False)
    update_data = []
    for update in update_details:
        if update.new_number != update.old_number:
            data = {}
            data['updated_by'] = update.updated_by
            data['customer_id'] = update.customer_id
            data['customer_name'] = update.customer_name
            data['new_number'] = update.new_number
            data['old_number'] = update.old_number
            data['modified_date'] = update.modified_date
            data['product_id'] = update.product_id.product_id
            update_data.append(data)
    return {'update_data' : update_data, 'update_details':update_details}

def get_vin_sync_feeds_detail(brand=None):
    feed_logs = get_model("VinSyncFeedLog", brand).objects.filter(email_flag=False)
    feed_data = []
    for feed in feed_logs:
        data = {}
        data['vin'] = feed.product_id
        data['dealer_asc_id'] = feed.dealer_asc_id
        data['status_code'] = feed.status_code
        data['ucn_count'] = feed.ucn_count
        feed_data.append(data)
    return {'feed_data':feed_data, 'feed_logs':feed_logs}

''' returns coupon details with policy descripencies'''
def get_discrepant_coupon_details(brand):
    try:
        service_type_obj = get_model("Constant", brand).objects.filter(constant_name__contains ='service')
        for service_type in service_type_obj:
            service_dict.update({service_type.constant_name:service_type.constant_value})

        query = "select p.product_id,  c.service_type, c.valid_days, c.valid_kms, c.created_date \
                from gm_coupondata as c \
                inner join gm_productdata as p on c.product_id = p.id where ( c.status not in (2,6) \
                and ( (c.service_type = 1 and (c.valid_kms!={0} or c.valid_days!={1})) \
                or ( c.service_type = 2 and (c.valid_kms!={2} or c.valid_days!={3})) \
                or ( c.service_type = 3 and (c.valid_kms!={4} or c.valid_days!={5})) \
                ));".format(service_dict['service_1_valid_kms'], service_dict['service_1_valid_days'], 
                        service_dict['service_2_valid_kms'], service_dict['service_2_valid_days'],
                        service_dict['service_3_valid_kms'], service_dict['service_3_valid_days'])
    
        discrepant_coupons = get_sql_data(query, brand)
        
        if len(discrepant_coupons) > 0:
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["VIN", "SERVICE TYPE", "VALID DAYS", "VALID KMS"])
            for coupon in discrepant_coupons:
                csvwriter.writerow([coupon['product_id'], coupon['service_type'], coupon['valid_days'], coupon['valid_kms']])
            update_coupon(brand)
            return csvfile
        return False
    except Exception as ex:
        logger.info("[Exception Policy discrepancy ]: {0}".format(ex))

def update_coupon(brand):
    update_days_kms = "update gm_coupondata c set c.valid_kms = (case when c.service_type=1 then {0} when \
                       c.service_type=2 then {1} when c.service_type=3 then {2} end),c.valid_days = ".format(service_dict['service_1_valid_kms'],
                                                                                                             service_dict['service_2_valid_kms'],
                                                                                                             service_dict['service_3_valid_kms'])
    
    valid_days = " (case when c.service_type=1 then {0} when c.service_type=2 then {1} when c.service_type=3 then {2} end)".format(service_dict['service_1_valid_days'],
                                                                                                    service_dict['service_2_valid_days'],
                                                                                                    service_dict['service_3_valid_days'])
    
    update_date = "update gm_coupondata c join gm_productdata p on c.product_id=p.id set "
    update_date_1 = "(select ADDDATE(p.purchase_date,"

    update_extended_date = update_date + " c.extended_date = " + update_date_1 + valid_days + ")) where c.status not in (2, 6)and p.purchase_date is not null;"
    update_expired_date = update_date + " c.mark_expired_on = " + update_date_1+ valid_days + ")) where c.status not in (2, 4, 6)and p.purchase_date is not null;"
    update_days_kms = update_days_kms + valid_days + " ,c.status=1 where c.status not in (2, 4, 5, 6);"
     
    get_sql_data(query=update_extended_date, brand=brand)
    get_sql_data(query=update_expired_date,  brand=brand)
    get_sql_data(query=update_days_kms,  brand=brand)
    logger.info('[Policy Discrepency]:Updated coupon data')
    
def get_sql_data(query, brand):
    conn = connections[brand]
    cursor = conn.cursor()
    cursor.execute(query)
    data = dictfetchall(cursor)
    conn.close()
    return data
    
    
def add_product(product, consumer_phone_number_mapping, phone_number, product_details, final_products):
    consumer_obj = consumer_phone_number_mapping[phone_number]
    product_brand =  get_model('Brand', GmApps.AFTERBUY).objects.get(name=GmApps.BAJAJ)
    try:
        product_type = get_model('ProductType', GmApps.AFTERBUY).objects.get(product_type=product.sku_code)
    except Exception as ObjectDoesNotExist:
        product_type = afterbuy_models.ProductType(product_type=product.sku_code,
                                                               brand=product_brand)
        product_type.save()
    final_products.append(get_model('UserProduct', GmApps.AFTERBUY)(consumer=consumer_obj, product_type=product_type,
                                                                    brand_product_id=product_details.brand_product_id))
    return final_products
