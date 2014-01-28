from gladminds.models import common
from django.conf import settings
import csv
from datetime import datetime , timedelta ,date
def export_data_csv():
    now=datetime.now()
    coupon_data = common.CouponData.objects.filter(status =2,closed_date__gte=now+timedelta(days=-1))
    file_name=datetime.now()
    file_location=settings.PROJECT_DIR+'/data/'+str(file_name)+'.csv'
    csv_file = csv.writer(open(file_location, 'w'))
    csv_file.writerow(["vin","unique_service_coupon","valid_days","valid_kms","service_type","sa_phone_number",
                       "status","closed_date","mark_expired_on","actual_service_date","actual_kms","last_reminder_date"
                       ,"schedule_reminder_date"])
    for coupon in coupon_data:
        csv_file.writerow([coupon.vin,coupon.unique_service_coupon,coupon.valid_days,coupon.valid_kms,coupon.service_type,coupon.sa_phone_number,
                       coupon.status,coupon.closed_date,coupon.mark_expired_on,coupon.actual_service_date,coupon.actual_kms,coupon.last_reminder_date
                       ,coupon.schedule_reminder_date])



