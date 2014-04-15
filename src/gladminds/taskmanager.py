from django.db import models, transaction
from gladminds import audit, utils, message_template as templates
from gladminds.models import common, logs
from datetime import datetime, timedelta
from gladminds.models.common import CouponData
from django.utils import timezone

AUDIT_ACTION = "SENT TO QUEUE"

@transaction.commit_manually()
def get_customers_to_send_reminder(*args, **kwargs):
    from gladminds.tasks import send_reminder_message
    day = kwargs.get('reminder_day', None)
    today_date = datetime.now().date()
    reminder_date = datetime.now().date()+timedelta(days=day)
    results = common.CouponData.objects.select_for_update().filter(mark_expired_on__range=(today_date, reminder_date), last_reminder_date__isnull=True, status=1).select_related('vin','customer_phone_number__phone_number')
    for reminder in results:
        product = reminder.vin
        phone_number = product.customer_phone_number.phone_number
        usc = reminder.unique_service_coupon
        vin = product.vin
        expired_date = reminder.mark_expired_on.strftime('%d/%m/%Y')
        valid_kms = reminder.valid_kms
        message = templates.get_template('SEND_CUSTOMER_COUPON_REMINDER').format(usc = usc, vin = vin, expired_date = expired_date, valid_kms = valid_kms)
        send_reminder_message.delay(phone_number = phone_number, message = message)
        audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        reminder.last_reminder_date = datetime.now()
        reminder.save()
    transaction.commit()
    
@transaction.commit_manually()  
def get_customers_to_send_reminder_by_admin(*args, **kwargs):
    from gladminds.tasks import send_reminder_message
    today=datetime.now().date()
    results=common.CouponData.objects.select_for_update().filter(schedule_reminder_date__day=today.day, schedule_reminder_date__month=today.month, schedule_reminder_date__year=today.year, status=1).select_related('vin','customer_phone_number__phone_number')
    for reminder in results:
        product = reminder.vin
        phone_number = product.customer_phone_number.phone_number
        usc = reminder.unique_service_coupon
        vin = product.vin
        expired_date = reminder.mark_expired_on.strftime('%d/%m/%Y')
        valid_kms = reminder.valid_kms
        message = templates.get_template('SEND_CUSTOMER_COUPON_REMINDER').format(usc = usc, vin = vin, expired_date = expired_date, valid_kms = valid_kms)
        send_reminder_message.delay(phone_number = phone_number, message = message)
        audit.audit_log(reciever=phone_number, action=AUDIT_ACTION, message=message)
        reminder.last_reminder_date = datetime.now()
        reminder.schedule_reminder_date = None
        reminder.save()
    transaction.commit()

def expire_service_coupon(*args, **kwargs):
    today = timezone.now()
    threat_coupons = CouponData.objects.filter(mark_expired_on__lt = today.date())
    for coupon in threat_coupons:
        #If the coupon was initiated, it will expire if initiated more than 30days ago.
        if coupon.status == 4:
            print coupon.unique_service_coupon, coupon.actual_service_date, "==========#######"
            extended_date = coupon.actual_service_date + timedelta(days=30)
            if extended_date < today:
                coupon.status = 3
                coupon.save()
        #If the coupon is unused and crossed the days limit, it will expire.
        else:
            print coupon.unique_service_coupon, coupon.actual_service_date, "==================="
            coupon.status = 3
            coupon.save()

def import_data_from_sap(*args, **kwargs):
    pass

def get_data_feed_log_detail(start_date = None, end_date = None):
    start_date = start_date
    end_date = end_date
    feed_logs = logs.DataFeedLog.objects.filter(timestamp__range = (start_date, end_date))
    feed_data = []
    for feed in feed_logs:
        data = {}
        data['feed_type'] = feed.feed_type
        data['total_feed_count'] = feed.total_data_count
        data['total_failed_count'] = feed.failed_data_count
        data['total_success_count'] = feed.success_data_count
        data['timestamp'] = feed.timestamp
        data['action'] = feed.action
        feed_data.append(data)
    return feed_data
    
    
    
    