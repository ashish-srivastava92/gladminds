from datetime import datetime
from django.db import models, transaction
from gladminds import utils, message_template as templates
from gladminds.models import common
from datetime import datetime, timedelta

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
        reminder.last_reminder_date = datetime.now()
        reminder.schedule_reminder_date = None
        reminder.save()
    transaction.commit()

def expire_service_coupon(*args, **kwargs):
    today = datetime.now()
    common.CouponData.objects.filter(mark_expired_on__lt = today.date()).update(status=3)

def import_data_from_sap(*args, **kwargs):
    pass