from __future__ import absolute_import
from celery import shared_task
from django.conf import settings
from datetime import datetime, timedelta
import logging

from gladminds.bajaj import models as common
from gladminds.core import utils, export_file
from gladminds.core.managers.audit_manager import audit_log, feed_log
from gladminds.core.managers.sms_client_manager import load_gateway, MessageSentFailed
from gladminds.core.managers import mail
from gladminds.core.cron_jobs import taskmanager
from gladminds.bajaj.feeds import feed, export_feed
from gladminds.bajaj.services import  message_template as templates


logger = logging.getLogger("gladminds")
__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'
sms_client = load_gateway()


"""
This task send sms to customer on customer registration
"""


@shared_task
def send_registration_detail(*args, **kwargs):
    status = "success"
    logger.info("message addded")
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_registration_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This task send customer valid service detail
"""


@shared_task
def send_service_detail(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        response_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_service_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This job send sms to service advisor, whether the coupon is valid or not 
"""


@shared_task
def send_coupon_validity_detail(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon_validity_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This job send sms to customer when SA send 
 query, whether the coupon is valid or not 
"""


@shared_task
def send_coupon_detail_customer(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon_detail_customer.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This job send reminder sms to customer
"""


@shared_task
def send_reminder_message(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_reminder_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This job send coupon close message
"""


@shared_task
def send_coupon_close_message(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon_close_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)


"""
Send OTP
"""
@shared_task
def send_otp(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_otp.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status = status, reciever=phone_number, message=message)


@shared_task
def send_coupon(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This job send coupon close message to customer
"""

def send_sms(template_name, phone_number, feedback_obj, comment_obj=None):
    try:
        message = templates.get_template(template_name).format(type=feedback_obj.type,
                                          reporter=feedback_obj.reporter, message=feedback_obj.message,
                                          created_date=feedback_obj.created_date,
                                          assign_to=feedback_obj.assign_to,
                                          priority=feedback_obj.priority)
        if comment_obj and template_name == 'SEND_MSG_TO_ASSIGNEE':
            message = message + 'Note :' + comment_obj.comments
    except Exception as ex:
           message = templates.get_template('SEND_INVALID_MESSAGE')
    finally:
        logger.info("Send complain message received successfully with %s" % message)
        phone_number = utils.get_phone_number_format(phone_number)
        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("send_coupon", {"phone_number":phone_number, "message": message})
        else:
           send_coupon.delay(phone_number=phone_number, message=message)
    audit_log(reciever = phone_number, action=AUDIT_ACTION, message=message)
    return {'status': True, 'message': message}

@shared_task
def send_close_sms_customer(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_close_sms_customer.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)


@shared_task
def send_brand_sms_customer(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_brand_sms_customer.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
This task send Invalid Keyword message
"""


@shared_task
def send_invalid_keyword_message(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_invalid_keyword_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)


"""
This job send on customer product purchase
"""


@shared_task
def send_on_product_purchase(*args, **kwargs):
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        respone_data = sms_client.send_stateless(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_on_product_purchase.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        audit_log(status=status, reciever=phone_number, message=message)

"""
Crontab to send reminder sms to customer 
"""


@shared_task
def send_reminder(*args, **kwargs):
    taskmanager.get_customers_to_send_reminder(*args, **kwargs)

"""
Crontab to send scheduler reminder sms setup by admin
"""


@shared_task
def send_schedule_reminder(*args, **kwargs):
    taskmanager.get_customers_to_send_reminder_by_admin(*args, **kwargs)


"""
Crontab to set the is_expire=True for all those coupon which expire till current date time
"""


@shared_task
def expire_service_coupon(*args, **kwargs):
    taskmanager.expire_service_coupon(*args, **kwargs)

"""
Crontab to import data from SAP to Gladminds Database
"""


@shared_task
def mark_feeback_to_closed(*args, **kwargs):
    taskmanager.mark_feeback_to_closed(*args, **kwargs)

"""
Crontab to import data from SAP to Gladminds Database
"""

@shared_task
def import_data(*args, **kwargs):
    feed.load_feed()


'''
Cronjob to export close coupon data into csv file
'''


@shared_task
def export_close_coupon_data(*args, **kwargs):
    export_file.export_data_csv()


@shared_task
def export_coupon_redeem_to_sap(*args, **kwargs):
#     today = datetime.now().date()
    today = datetime.now()
    start_date = today - timedelta(days=1)
    end_date = today
    redeem_obj = feed.CouponRedeemFeedToSAP()
    feed_export_data = redeem_obj.export_data(
        start_date=start_date, end_date=end_date)
    if len(feed_export_data[0]) > 0:
        coupon_redeem = exportfeed.ExportCouponRedeemFeed(username=settings.SAP_CRM_DETAIL[
                       'username'], password=settings.SAP_CRM_DETAIL['password'],
                      wsdl_url=settings.COUPON_WSDL_URL, feed_type='Coupon Redeem Feed')
        coupon_redeem.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("tasks.py: No Coupon closed during last day")

'''
Cron Job to send report email for data feed
'''


@shared_task
def send_report_mail_for_feed(*args, **kwargs):
    day = kwargs['day_duration']
    today = datetime.now().date()
    start_date = today - timedelta(days=day)
    end_date = today + timedelta(days=1)
    feed_data = taskmanager.get_data_feed_log_detail(
        start_date=start_date, end_date=end_date)
    mail.feed_report(feed_data=feed_data)

'''
Cron Job to send ASC Registeration to BAJAJ
'''


@shared_task
def export_asc_registeration_to_sap(*args, **kwargs):
    phone_number = kwargs['phone_number']
    brand = kwargs['brand']
    feed_type = "ASC Registration Feed"

    status = "success"
    try:
        asc_registeration_data = feed.ASCRegistrationToSAP()
        feed_export_data = asc_registeration_data.export_data(phone_number)
        export_obj = exportfeed.ExportCouponRedeemFeed(
               username=settings.SAP_CRM_DETAIL['username'], password=settings
               .SAP_CRM_DETAIL['password'], wsdl_url=settings.ASC_WSDL_URL)
        export_obj.export(items=feed_export_data['item'],
                          item_batch=feed_export_data['item_batch'])
    except Exception as ex:
        status = "failed"
        config = settings.REGISTRATION_CONFIG[
                                         brand][feed_type]
        export_asc_registeration_to_sap.retry(
            exc=ex, countdown=config["retry_time"], kwargs=kwargs,
            max_retries=config["num_of_retry"])
    finally:
        export_status = False if status == "failed" else True
        total_failed = 1 if status == "failed" else 0
        if status == "failed":
            feed_data = 'ASC Registration for this %s is failing' % phone_number
            mail.send_registration_failure(feed_data=feed_data,
                               feed_type="ASC Registration Feed", brand=brand)
        feed_log(feed_type="ASC Registration Feed", total_data_count=1,
         failed_data_count=total_failed, success_data_count=1 - total_failed,
                 action='Sent', status=export_status)

'''
Delete the all the generated otp by end of day.
'''
@shared_task
def delete_unused_otp(*args, **kwargs):
    common.OTPToken.objects.all().delete()

'''
Cron Job to send report email for data feed
'''
@shared_task
def send_report_mail_for_feed_failure(*args, **kwargs):
    remarks = kwargs['remarks']
    feed_type = kwargs['feed_type']
    mail.feed_failure_report(remarks = remarks, feed_type=feed_type)
    
'''
Cron Job to send info of registered customer
'''

@shared_task
def export_customer_reg_to_sap(*args, **kwargs):
    redeem_obj = feed.CustomerRegistationFeedToSAP()
    feed_export_data = redeem_obj.export_data()
    if len(feed_export_data[0]) > 0:
        customer_registered = exportfeed.ExportCustomerRegistrationFeed(username=settings.SAP_CRM_DETAIL[
                       'username'], password=settings.SAP_CRM_DETAIL['password'],
                      wsdl_url=settings.CUSTOMER_REGISTRATION_WSDL_URL, feed_type='Customer Registration Feed')
        customer_registered.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("tasks.py: No Customer registered since last feed")

    
_tasks_map = {"send_registration_detail": send_registration_detail,

              "send_service_detail": send_service_detail,

              "send_coupon_validity_detail": send_coupon_validity_detail,

              "send_coupon_detail_customer": send_coupon_detail_customer,

              "send_reminder_message": send_reminder_message,

              "send_coupon_close_message": send_coupon_close_message,

              "send_coupon": send_coupon,

              "send_close_sms_customer": send_close_sms_customer,

              "send_brand_sms_customer": send_brand_sms_customer,

              "send_on_product_purchase": send_on_product_purchase,

              "send_reminder": send_reminder,

              "send_schedule_reminder": send_schedule_reminder,

              "expire_service_coupon": expire_service_coupon,

              "import_data": import_data,

              "export_close_coupon_data": export_close_coupon_data,

              "export_coupon_redeem_to_sap": export_coupon_redeem_to_sap,

              "send_report_mail_for_feed": send_report_mail_for_feed,
              
              "send_otp": send_otp,
              
              "delete_unused_otp" : delete_unused_otp,
              
              "send_invalid_keyword_message" : send_invalid_keyword_message,
              
              "export_customer_reg_to_sap" : export_customer_reg_to_sap,
              
              "mark_feeback_to_closed" : mark_feeback_to_closed

              }
