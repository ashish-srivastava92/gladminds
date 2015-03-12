from celery import shared_task
from django.conf import settings
from datetime import datetime, timedelta
import operator

from gladminds.bajaj import models as models
from gladminds.core import utils, export_file
from gladminds.core.managers.audit_manager import sms_log, feed_log
from gladminds.core.managers.sms_client_manager import load_gateway, MessageSentFailed
from gladminds.core.managers import mail
from gladminds.core.cron_jobs import taskmanager
from gladminds.bajaj.services.coupons import import_feed, export_feed
from gladminds.bajaj.services.loyalty import export_feed as loyalty_export
from gladminds.core.services import  message_template as templates

import pytz
import logging
from gladminds.core.managers.mail import send_due_date_exceeded,\
    send_due_date_reminder, send_email_to_asc_customer_support
from django.contrib.auth.models import User
from gladminds.core.constants import DATE_FORMAT, FEED_TYPES
from gladminds.core.cron_jobs.queue_utils import get_task_queue,\
    send_job_to_queue
from gladminds.core.core_utils.date_utils import convert_utc_to_local_time
from gladminds.core.cron_jobs.update_fact_tables import update_coupon_history_table
from gladminds.core.managers.mail import get_email_template,send_email_to_redeem_escaltion_group,\
    send_email_to_welcomekit_escaltion_group
from gladminds.core.auth_helper import Roles
from django.db.models import Q
import textwrap


logger = logging.getLogger("gladminds")
__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'

def set_gateway(**kwargs):
    sms_client = kwargs.get('sms_client', None)
    logger.info('sms_client is {0}'.format(sms_client))
    sms_client_gateway = load_gateway(sms_client)
    response_data = sms_client_gateway.send_stateless(**kwargs)

@shared_task
def send_registration_detail(*args, **kwargs):
    """
    send sms to customer on customer registration
    """
    status = "success"
    brand= kwargs.get('brand', None)
    logger.info("message addded")
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_registration_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

def customer_detail_recovery(*args, **kwargs):
    """
    send customer details recovery by sms 
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        customer_detail_recovery.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_service_detail(*args, **kwargs):
    """
    send customer valid service detail
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_service_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_coupon_validity_detail(*args, **kwargs):
    """
    send sms to service advisor, whether the coupon is valid or not 
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon_validity_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_coupon_detail_customer(*args, **kwargs):
    """
    send sms to customer when SA send 
     query, whether the coupon is valid or not 
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
        logger.info('[send_coupon_detail_customer]: SENT MESSAGE')
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon_detail_customer.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        logger.info('[send_coupon_detail_customer]: SENT MESSAGE FINALLY')
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_servicedesk_feedback_detail(*args, **kwargs):
    """
    send sms in service desk 
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_servicedesk_feedback_detail.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_reminder_message(*args, **kwargs):
    """
    send reminder sms to customer
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_reminder_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_customer_phone_number_update_message(*args, **kwargs):
    """
    send customer phone number update sms
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_reminder_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_coupon_close_message(*args, **kwargs):
    """
    send coupon close message
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon_close_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_loyalty_escalation_message(*args, **kwargs):
    """
    sends escalation message related to loyalty
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_reminder_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_dfsc_customer_support(*args, **kwargs):
    """
    sends customer support phone number 
    """
    status = "success"
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_reminder_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(status=status, receiver=phone_number, message=message)

@shared_task
def send_otp(*args, **kwargs):
    """ Send OTP """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        brand = kwargs.get('brand', 'bajaj')
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_otp.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)


@shared_task
def send_coupon(*args, **kwargs):
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_coupon.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_close_sms_customer(*args, **kwargs):
    """
    send coupon close message to customer
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_close_sms_customer.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)


@shared_task
def send_brand_sms_customer(*args, **kwargs):
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_brand_sms_customer.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_invalid_keyword_message(*args, **kwargs):
    """
    send Invalid Keyword message
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_invalid_keyword_message.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand, status=status, receiver=phone_number, message=message)

@shared_task
def send_on_product_purchase(*args, **kwargs):
    """
    send on customer product purchase
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_on_product_purchase.retry(
            exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)
        

@shared_task
def send_point(*args, **kwargs):
    """
    send on loyalty points to member
    """    
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        logger.info("request for sending sms received {0} message {1}".format(phone_number, message))
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        logger.error("[Eception:send_point]:{0}".format(ex))
        send_point.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_loyalty_sms(*args, **kwargs):
    """
    Send loyalty sms
    """
    status = "success"
    brand= kwargs.get('brand', None)
    try:
        phone_number = kwargs.get('phone_number', None)
        message = kwargs.get('message', None)
        brand = kwargs.get('brand', 'bajaj')
        set_gateway(**kwargs)
    except (Exception, MessageSentFailed) as ex:
        status = "failed"
        send_loyalty_sms.retry(exc=ex, countdown=10, kwargs=kwargs, max_retries=5)
    finally:
        sms_log(brand,status=status, receiver=phone_number, message=message)

@shared_task
def send_reminder(*args, **kwargs):
    """
    send reminder sms to customer 
    """
    taskmanager.get_customers_to_send_reminder(*args, **kwargs)

@shared_task
def send_schedule_reminder(*args, **kwargs):
    """
    send scheduler reminder sms setup by admin
    """
    taskmanager.get_customers_to_send_reminder_by_admin(*args, **kwargs)

@shared_task
def expire_service_coupon(*args, **kwargs):
    """
    set the is_expire=True for all those coupon which expire till current date time
    """
    taskmanager.expire_service_coupon(*args, **kwargs)

@shared_task
def mark_feeback_to_closed(*args, **kwargs):
    """
    mark feedbacks resolved 2 days back as closed 
    """
    taskmanager.mark_feeback_to_closed(*args, **kwargs)

@shared_task
def import_data(*args, **kwargs):
    """
    import data from SAP to Gladminds Database
    """
    import_feed.load_feed()

@shared_task
def export_close_coupon_data(*args, **kwargs):
    '''
    export close coupon data into csv file
    '''
    export_file.export_data_csv()


@shared_task
def export_coupon_redeem_to_sap(*args, **kwargs):
    '''
    send coupon redeemed in a day
    '''
    coupon_redeem = export_feed.ExportCouponRedeemFeed(username=settings.SAP_CRM_DETAIL[
                   'username'], password=settings.SAP_CRM_DETAIL['password'],
                  wsdl_url=settings.COUPON_WSDL_URL, feed_type='Coupon Redeem Feed')
    feed_export_data = coupon_redeem.export_data()
    if len(feed_export_data[0]) > 0:
        coupon_redeem.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("[export_coupon_redeem_to_sap]: No Coupon closed during last day")

@shared_task
def send_report_mail_for_feed(*args, **kwargs):
    '''
    send report email for data feed
    '''
    day = kwargs['day_duration']
    today = datetime.now().date()
    start_date = today - timedelta(days=day)
    feed_data = taskmanager.get_data_feed_log_detail(
        start_date=start_date, end_date=today)
    mail.feed_report(feed_data=feed_data)

@shared_task
def send_mail_for_feed_failure(*args, **kwargs):
    '''
    send feed failure email
    '''
    for feed_type in FEED_TYPES:
        feed_data = taskmanager.get_feed_failure_log_detail(type=feed_type)
        if feed_data['feed_data']:
            mail.feed_failure(feed_data=feed_data['feed_data'])
            feed_data['feed_logs'].update(email_flag=True)

@shared_task
def send_vin_sync_feed_details(*args, **kwargs):
    ''' send vin sync feeds'''
    feed_data = taskmanager.get_vin_sync_feeds_detail()
    if feed_data['feed_data']:
        mail.send_vin_sync_feed_report(feed_data=feed_data['feed_data'])
        feed_data['feed_logs'].update(email_flag=True)

@shared_task
def send_mail_for_customer_phone_number_update(*args, **kwargs):
    '''
    send customer phone number update email
    '''
    customer_details = taskmanager.get_customer_details()
    if customer_details['customer_data']:
        mail.customer_phone_number_update(customer_details=customer_details['customer_data'])
        customer_details['customer_details'].update(email_flag=True)

@shared_task
def send_mail_customer_phone_number_update_exceeds(*args, **kwargs):
    '''
    send email to asm when customer number update exceeds
    '''
    update_details = taskmanager.get_update_number_exceeds()
    if update_details['update_data']:
        mail.send_phone_number_update_count_exceeded(update_details=update_details['update_data'])
        update_details['update_details'].update(email_flag=True) 

@shared_task
def send_mail_for_policy_discrepency(*args, **kwargs):
    ''' send mail for policy_discrepency'''
    discrepant_coupons = taskmanager.get_discrepant_coupon_details()
    mail.discrepant_coupon_update(discrepant_coupons=discrepant_coupons)


@shared_task
def export_asc_registeration_to_sap(*args, **kwargs):
    '''
    send ASC Registration to BAJAJ
    '''
    phone_number = kwargs['phone_number']
    brand = kwargs['brand']
    feed_type = "ASC Registration Feed"

    status = "success"
    try:
        export_obj = export_feed.ExportASCRegistrationFeed(
               username=settings.SAP_CRM_DETAIL['username'], password=settings
               .SAP_CRM_DETAIL['password'], wsdl_url=settings.ASC_WSDL_URL)
        feed_export_data = export_obj.export_data(phone_number)
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
        feed_log(brand=settings.BRAND, feed_type="ASC Registration Feed", total_data_count=1,
         failed_data_count=total_failed, success_data_count=1 - total_failed,
                 action='Sent', status=export_status)

@shared_task
def delete_unused_otp(*args, **kwargs):
    '''
    Delete the all the generated otp by end of day.
    '''
    models.OTPToken.objects.all().delete()

@shared_task
def export_customer_reg_to_sap(*args, **kwargs):
    '''
    send info of registered customer
    '''
    customer_registered = export_feed.ExportCustomerRegistrationFeed(username=settings.SAP_CRM_DETAIL[
                   'username'], password=settings.SAP_CRM_DETAIL['password'],
                  wsdl_url=settings.CUSTOMER_REGISTRATION_WSDL_URL, feed_type='Customer Registration Feed')
    feed_export_data = customer_registered.export_data()
    if len(feed_export_data[0]) > 0:
        customer_registered.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("[export_customer_reg_to_sap]: No Customer registered since last feed")

@shared_task
def update_coupon_history_data(*args, **kwargs):
    update_coupon_history_table()
#     try:
#         logger.info("updating_coupon_history_data")
#         update_coupon_history_table()
#     except Exception as ex:
#         logger.info("update_coupon_history_data: {0}".format(ex))

def send_sms(template_name, phone_number, feedback_obj, comment_obj=None):
    created_date = convert_utc_to_local_time(feedback_obj.created_date, True)
    try:
        assignee = feedback_obj.assignee.user_profile.user.username
    except:
        assignee = ""
    try:
        due_date = feedback_obj.due_date.strftime(DATE_FORMAT)
    except:
        due_date = ""
    reporter = None
    try:
        if feedback_obj.reporter:
            reporter = feedback_obj.reporter.user_profile
        message = templates.get_template(template_name).format(type=feedback_obj.type,
                                                               reporter=reporter,
                                                               message=feedback_obj.description,
                                                               created_date=created_date,
                                                               assign_to=assignee,
                                                               priority=feedback_obj.priority,
                                                               due_date = due_date, id=feedback_obj.id)
        if comment_obj and template_name == 'SEND_MSG_TO_ASSIGNEE':
            message = message + 'Note :' + comment_obj.comment
    except Exception as ex:
        logger.info("send_sms: {0}".format(ex))
        message = templates.get_template('SEND_INVALID_MESSAGE')
    finally:
        logger.info("Send complain message received successfully with %s" % message)
        phone_number = utils.get_phone_number_format(phone_number)
        sms_log(settings.BRAND,receiver=phone_number, action=AUDIT_ACTION, message=message)
        send_job_to_queue(send_servicedesk_feedback_detail, {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
    return {'status': True, 'message': message}


def send_reminders_for_servicedesk(*args, **kwargs):
    manager_obj = User.objects.get(groups__name='sdm')
    time = datetime.now()
    '''
    send mail when reminder_date is less than current date or when due date is less than current date
    '''
    feedback_obj = models.Feedback.objects.filter(reminder_date__lte=time, reminder_flag=False) or models.Feedback.objects.filter(due_date__lte=time,resolution_flag=False)
    for feedback in feedback_obj:
        if not feedback.reminder_flag:
            context = utils.create_context('DUE_DATE_EXCEEDED_MAIL_TO_AGENT', feedback)
            send_due_date_reminder(context, feedback.assignee.user_profile.user.email)
            context = utils.create_context('DUE_DATE_REMINDER_MAIL_TO_MANAGER', feedback)
            send_due_date_reminder(context, manager_obj.email)
            feedback.reminder_flag = False
 
        if not feedback.resolution_flag:
            context = utils.create_context('DUE_DATE_EXCEEDED_MAIL_TO_MANAGER', feedback)
            escalation_list = models.UserProfile.objects.filter(user__groups__name=Roles.SDESCALATION)
            escalation_list_detail = utils.get_escalation_mailing_list(escalation_list)
            send_due_date_exceeded(context, escalation_list_detail['mail'])
            for phone_number in escalation_list_detail['sms']: 
                send_sms('DUE_DATE_EXCEEDED_ESCALATION', phone_number, feedback)
            feedback.resolution_flag = False
        feedback.save()

@shared_task
def export_member_temp_id_to_sap(*args, **kwargs):
    '''
    send info of registered Mechanic
    '''
    member_registered = loyalty_export.ExportMemberTempFeed(username=settings.SAP_CRM_DETAIL[
                   'username'], password=settings.SAP_CRM_DETAIL['password'],
                  wsdl_url=settings.MEMBER_SYNC_WSDL_URL, feed_type='Mechanic Registration Feed')
    feed_export_data = member_registered.export_data()
    if len(feed_export_data[0]) > 0:
        member_registered.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("[export_member_temp_id_to_sap]: No member registered since last feed")

@shared_task
def export_purchase_feed_sync_to_sap(*args, **kwargs):
    '''
    send info of purchase feed failed due to no matching VIN in GM
    '''
    purchase_feed_sync = export_feed.ExportPurchaseSynFeed(username=settings.SAP_CRM_DETAIL[
                           'username'], password=settings.SAP_CRM_DETAIL['password'],
                          wsdl_url=settings.PURCHASE_SYNC_WSDL_URL, feed_type='Purchase Sync Feed')
    feed_export_data = purchase_feed_sync.export_data()
    if len(feed_export_data[0]) > 0:
        purchase_feed_sync.export(items=feed_export_data[0], item_batch=feed_export_data[
                         1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("[export_purchase_feed_sync_to_sap]: No Purchase Feed failed since last feed")

def welcome_kit_due_date_escalation(*args, **kwargs):
    time = datetime.now()
    '''
    send mail when due date is less than current date for welcome kit request
    '''
    args=[Q(due_date__lte=time), Q(resolution_flag=False),~Q(status='Shipped')]
    welcome_kit_obj = models.WelcomeKit.objects.filter(reduce(operator.and_, args))
    for welcome_kit in welcome_kit_obj:
        data = get_email_template('WELCOME_KIT_DUE_DATE_EXCEED_MAIL_TO_MANAGER')
        data['newsubject'] = data['subject'].format(id = welcome_kit.transaction_id)
        data['content'] = data['body'].format(transaction_id=welcome_kit.transaction_id, 
                                      due_date=welcome_kit.due_date, status=welcome_kit.status )
        escalation_list = models.UserProfile.objects.filter(user__groups__name=Roles.WELCOMEKITESCALATION)
        escalation_list_detail = utils.get_escalation_mailing_list(escalation_list)
        send_email_to_welcomekit_escaltion_group(data, escalation_list_detail)

        message = templates.get_template('LOYALTY_DUE_DATE_EXCEED_ESCALATION').format(transaction_id=welcome_kit.transaction_id,
                                                                                      status=welcome_kit.status)    
        for phone_number in escalation_list_detail['sms']: 
            phone_number = utils.get_phone_number_format(phone_number)
            sms_log(settings.BRAND,receiver=phone_number, action=AUDIT_ACTION, message=message)
            send_job_to_queue(send_loyalty_escalation_message,
                               {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
        welcome_kit.resolution_flag = True
        welcome_kit.save()

def redemption_request_due_date_escalation(*args, **kwargs):
    time = datetime.now()
    '''
    send mail when due date is less than current date for redemption request
    '''
    args=[Q(due_date__lte=time), Q(resolution_flag=False),~Q(status='Delivered')]
    redemption_request_obj = models.RedemptionRequest.objects.filter(reduce(operator.and_, args))
    for redemption_request in redemption_request_obj:
        data = get_email_template('REDEMPTION_REQUEST_DUE_DATE_EXCEED_MAIL_TO_MANAGER')
        data['newsubject'] = data['subject'].format(id = redemption_request.transaction_id)
        data['content'] = data['body'].format(transaction_id=redemption_request.transaction_id,
                                                                  status=redemption_request.status)
        escalation_list = models.UserProfile.objects.filter(user__groups__name=Roles.REDEEMESCALATION)
        escalation_list_detail = utils.get_escalation_mailing_list(escalation_list)
        send_email_to_redeem_escaltion_group(data, escalation_list_detail)
        
        message = templates.get_template('LOYALTY_DUE_DATE_EXCEED_ESCALATION').format(transaction_id=redemption_request.transaction_id,
                                                                                      status=redemption_request.status)    
        for phone_number in escalation_list_detail['sms']: 
            phone_number = utils.get_phone_number_format(phone_number)
            sms_log(brand=settings.BRAND,receiver=phone_number, action=AUDIT_ACTION, message=message)
            send_job_to_queue(send_loyalty_escalation_message,
                               {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
        redemption_request.resolution_flag = True
        redemption_request.save()

def customer_support_helper(obj_list, data, message):   
    for obj in obj_list:
        try:
            phone = obj.user.phone_number
            send_email_to_asc_customer_support(data, obj.user.user.email)
            sms_log(receiver = phone, action=AUDIT_ACTION, message=message)
            send_job_to_queue(send_dfsc_customer_support,
                                   {"phone_number":phone, "message":message, "sms_client":settings.SMS_CLIENT})
        except Exception as ex:
            logger.info("[Exception fail to send SMS to ASCs/Dealers on Customer Support]  {0}".format(ex))
            
def dfsc_customer_support(*args, **kwargs):    
    asc_obj = models.AuthorizedServiceCenter.objects.filter(user__state='MAH').select_related('user, user__user')
    dealer_obj = models.Dealer.objects.filter(user__state='MAH').select_related('user, user__user')
    
    data = get_email_template('CUSTOMER_SUPPORT_FOR_DFSC')
    data['newsubject'] = data['subject']
    data['content'] = data['body']
    message = templates.get_template('CUSTOMER_SUPPORT_FOR_DFSC')
    
    customer_support_helper(asc_obj, data, message)
    customer_support_helper(dealer_obj, data, message)    
    
@shared_task
def export_member_accumulation_to_sap(*args, **kwargs):
    '''
    send info of accumulation requests
    '''
    accumulation_requests = loyalty_export.ExportAccumulationFeed(username=settings.SAP_CRM_DETAIL[
                   'username'], password=settings.SAP_CRM_DETAIL['password'],
                  wsdl_url=settings.ACCUMULATION_SYNC_WSDL_URL, feed_type='Accumulation Request Feed')
    feed_export_data = accumulation_requests.export_data()
    if len(feed_export_data[0]) > 0:
        accumulation_requests.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2], query_set=feed_export_data[3])
    else:
        logger.info("[export_member_accumulation_to_sap]: No accumulation request since last feed")
        
@shared_task
def export_member_redemption_to_sap(*args, **kwargs):
    '''
    send info of redemption requests
    '''
    redemption_requests = loyalty_export.ExportRedemptionFeed(username=settings.SAP_CRM_DETAIL[
                   'username'], password=settings.SAP_CRM_DETAIL['password'],
                  wsdl_url=settings.REDEMPTION_SYNC_WSDL_URL, feed_type='Redemption Request Feed')
    feed_export_data = redemption_requests.export_data()
    if len(feed_export_data[0]) > 0:
        redemption_requests.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2], query_set=feed_export_data[3])
    else:
        logger.info("[export_member_redemption_to_sap]: No redemption request since last feed")
        
@shared_task
def export_distributor_to_sap(*args, **kwargs):
    '''
    send info of redemption requests
    '''
    distributors = loyalty_export.ExportDistributorFeed(username=settings.SAP_CRM_DETAIL[
                   'username'], password=settings.SAP_CRM_DETAIL['password'],
                  wsdl_url=settings.DISTRIBUTOR_SYNC_WSDL_URL, feed_type='Distributor Registration Feed')
    feed_export_data = distributors.export_data()
    if len(feed_export_data[0]) > 0:
        distributors.export(items=feed_export_data[0], item_batch=feed_export_data[
                             1], total_failed_on_feed=feed_export_data[2])
    else:
        logger.info("[export_distributor_to_sap]: No distributor registered since last feed")
 
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
              
              "mark_feeback_to_closed" : mark_feeback_to_closed,
              
              "customer_detail_recovery": customer_detail_recovery,
              
              "send_point": send_point,
              
              "send_loyalty_sms": send_loyalty_sms,
              
              "send_reminders_for_servicedesk": send_reminders_for_servicedesk,
              
              "send_mail_for_feed_failure" : send_mail_for_feed_failure,
              
              "send_servicedesk_feedback_detail" : send_servicedesk_feedback_detail,
              
              "send_customer_phone_number_update_message" : send_customer_phone_number_update_message,
              
              "send_mail_customer_phone_number_update_exceeds" : send_mail_customer_phone_number_update_exceeds,
              
              "send_vin_sync_feed_details" : send_vin_sync_feed_details,

              "update_coupon_history": update_coupon_history_data, 
              
              "redemption_request_due_date_escalation":redemption_request_due_date_escalation,
              
              "export_member_temp_id_to_sap": export_member_temp_id_to_sap,

              "export_purchase_feed_sync_to_sap": export_purchase_feed_sync_to_sap,

              "welcome_kit_due_date_escalation":welcome_kit_due_date_escalation,
              
              "send_mail_for_customer_phone_number_update" : send_mail_for_customer_phone_number_update,
              
              "send_mail_for_policy_discrepency": send_mail_for_policy_discrepency,
              
              "export_member_accumulation_to_sap": export_member_accumulation_to_sap,
              
              "export_member_redemption_to_sap": export_member_redemption_to_sap,
              
              "export_distributor_to_sap": export_distributor_to_sap,
              
              "dfsc_customer_support": dfsc_customer_support
              }
