import StringIO
import csv
import smtplib
import logging
from django.core.mail.message import EmailMessage
from django.conf import settings
from django.template import Context, Template
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from gladminds.core.managers import audit_manager
from gladminds.core.auth_helper import GmApps
from gladminds.core.loaders.module_loader import get_model
from gladminds.bajaj.models import EmailLog

logger = logging.getLogger("gladminds")


def get_email_template(key):
    template_object = get_model('EmailTemplate').objects.filter(template_key=key).values()
    return template_object[0]

def get_mail_receiver(template_name, mail_detail):
    if  (settings.ENV not in settings.IGNORE_ENV):
            receivers = settings.template_name['receiver']
    else:
            receivers = []
            receivers.append(mail_detail['receiver'])
    return receivers

def send_email_with_file_attachment(sender, receiver, subject, body, filename, content, brand='bajaj'):
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        message = EmailMessage(subject, body, sender, receiver)
        message.attach(filename + yesterday.strftime("%d_%m_%Y") +'.csv', content.getvalue(), 'text/csv')
        message.send()
        audit_manager.email_log(subject," ", sender, receiver, brand=brand);
        return True
    except Exception as ex:
        logger.error('Exception while sending mail {0}'.format(ex))
        return False
    

def send_email(sender, receiver, subject, body, message=None,smtp_server=settings.MAIL_SERVER, title='GCP_Bajaj_FSC_Feeds'
               , brand='bajaj'):
    try:
        msg = MIMEText(body, 'html', _charset='utf-8')
        msg['Subject'] = subject
        if isinstance(receiver, list):
            msg['To'] = ", ".join(receiver)
        else:
            msg['To'] = receiver
        msg['From'] = title + "<%s>"% sender
        mail = smtplib.SMTP(smtp_server)
        mail.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
        mail.quit()
        audit_manager.email_log(subject, message, sender, receiver, brand=brand);
        return True
    except Exception as ex:
        logger.error('Exception while sending mail: {0}'.format(ex))
        return False


def send_email_activation(receiver_email, data=None, brand=None):
    file_stream = open(settings.EMAIL_DIR+'/activation_email.html')
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    context = Context(data)
    body = template.render(context)
    mail_detail = settings.EMAIL_ACTIVATION_MAIL
    send_email(sender=mail_detail['sender'],
               receiver=receiver_email,
               subject=mail_detail['subject'], body=body,
               smtp_server=settings.MAIL_SERVER, title='Support',
               brand=brand)


def send_recycle_mail(sender_id, data=None):
    file_stream = open(settings.EMAIL_DIR+'/recycle_email.html')
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    context = Context({'product_info': data})
    body = template.render(context)
    mail_detail = settings.RECYCLE_MAIL
    send_email(sender=mail_detail['sender'],
               receiver=mail_detail['receiver'],
               subject=mail_detail['subject'], body=body,
               smtp_server=settings.MAIL_SERVER, title='Recycle Product',
               brand=GmApps.AFTERBUY)


def feed_report(feed_data=None):
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        file_stream = open(settings.EMAIL_DIR+'/feed_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"feed_logs": feed_data, "yesterday": yesterday})
        body = template.render(context)
        mail_detail = settings.MAIL_DETAIL
        send_email(sender=mail_detail['sender'],
                   receiver=mail_detail['receiver'],
                   subject=mail_detail['subject'], body=body,
                   smtp_server=settings.MAIL_SERVER)

    except Exception as ex:
        logger.info("[Exception feed_report]: {0}".format(ex))


def customer_phone_number_update(customer_details=None):
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        mail_detail = get_email_template('CUSTOMER_PHONE_NUMBER_UPDATE')
        receivers = get_mail_receiver('CUSTOMER_PHONE_NUMBER_UPDATE', mail_detail)
        csvfile = StringIO.StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["DEALER/ASC ID", "CUSTOMER ID", "CUSTOMER NAME", "OLD NUMBER", "NEW NUMBER"])

        for customer in customer_details:
            csvwriter.writerow([customer['dealer_asc_id'], customer['customer_id'], customer['customer_name'],
                                customer['old_number'], customer['new_number']])
        
        send_email_with_file_attachment(mail_detail['sender'], receivers, mail_detail['subject'],
                                          mail_detail['body'] + yesterday.strftime("%d-%m-%Y"), 'customer_phone_number_update_',
                                          csvfile)
    except Exception as ex:
        logger.info("[Exception customer phone number update]: {0}".format(ex))


def send_vin_sync_feed_report(feed_data=None):
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        mail_detail = get_email_template('VIN_SYNC_FEED')
        receivers = get_mail_receiver('VIN_SYNC_FEED', mail_detail)
        csvfile = StringIO.StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["CHASSIS", "DEALER_ASC_ID", "STATUS_CODE"])
        for feed in feed_data:
            csvwriter.writerow([feed['vin'], feed['dealer_asc_id'], feed['status_code']])

        logger.info("Sending out feed_failure emails")
        send_email_with_file_attachment(mail_detail['sender'], receivers, mail_detail['subject'],
                                          mail_detail['body'] + yesterday.strftime("%d-%m-%Y"), 'vin_sync_feed_', csvfile)
    except Exception as ex:
        logger.info("[Exception feed_fail_report]: {0}".format(ex))


def feed_failure(feed_data=None):
    try:
        mail_detail = get_email_template('FEED_FAILURE')
        receivers = get_mail_receiver('FEED_FAILURE', mail_detail)
        csvfile = StringIO.StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Timestamp", "FeedType", "Reason"])
        feed_type = ''
        feed_log_time = ''
        for feed in feed_data:
            csvwriter.writerow([feed['created_date'], feed['feed_type'], feed['reason']])
            feed_type = feed['feed_type']
        try:
            feed_log_time = EmailLog.objects.filter(subject='Gladminds Failure Report - '+feed_type).order_by('-id')[0]
            feed_log_time = feed_log_time.created_date.strftime("%d_%m_%Y") 
        except:
            feed_log_time = datetime.now().strftime("%d_%m_%Y")

        logger.info("Sending out feed_failure emails")
        send_email_with_file_attachment(mail_detail['sender'], receivers, mail_detail['subject'] + feed_type,
                                          mail_detail['body'] + feed_log_time, 'feed_failure_', csvfile)
    except Exception as ex:
        logger.info("[Exception feed_fail_report]: {0}".format(ex))


def send_registration_failure(feed_data=None,
                              feed_type=None, brand=None):
    try:
        file_stream = open(settings.TEMPLATE_DIR +
                            '/portal/registration_failure_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"feed_type": feed_type,
                           "feed_logs": feed_data})
        body = template.render(context)

        mail_detail = settings.REGISTRATION_CONFIG[brand][feed_type][
                                                         'fail_mail_detail']
        logger.info(mail_detail)
        logger.info(settings.MAIL_SERVER)
        send_email(sender=mail_detail['sender'], receiver=mail_detail[
              'receiver'], subject=mail_detail['subject'], body=body,
                   smtp_server=settings.MAIL_SERVER)

    except Exception as ex:
        logger.info("[Exception feed_report]: {0}".format(ex))


def item_purchase_interest(data=None, receiver=None, subject=None):
    try:
        file_stream = open(
            settings.EMAIL_DIR + '/purchase_interest_mail.html')
        item = file_stream.read()
        template = Template(item)
        context = Context({"user": data})
        body = template.render(context)
        send_email(sender=data['email_id'], receiver=receiver,
                        subject=subject, body=body,
                        smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception item purchase report]: {0}".format(ex))


def warrenty_extend(data=None, receiver=None, subject=None):
    try:
        file_stream = open(
            settings.EMAIL_DIR + '/warrenty_extend_mail.html')
        item = file_stream.read()
        template = Template(item)
        context = Context({"user": data})
        body = template.render(context)
        send_email(sender=data['email_id'], receiver=receiver,
                        subject=subject, body=body,
                        smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception item warrenty extend]: {0}".format(ex))


def insurance_extend(data=None, receiver=None, subject=None):
    try:
        file_stream = open(
            settings.EMAIL_DIR + '/insurance_extend_mail.html')
        item = file_stream.read()
        template = Template(item)
        context = Context({"user": data})
        body = template.render(context)
        send_email(sender=data['email_id'], receiver=receiver,
                        subject=subject, body=body,
                        smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception item insurance extend]: {0}".format(ex))


def sent_password_reset_link(receiver=None, data=None, brand=None):
    try:
        file_stream = open(settings.EMAIL_DIR+'/password_reset_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context(data)
        body = template.render(context)
        mail_detail = settings.PASSWORD_RESET_MAIL
        send_email(sender = mail_detail['sender'], receiver = receiver, 
                   subject = mail_detail['subject'], body = body,
                   smtp_server = settings.MAIL_SERVER, title='Support',
                   brand = brand)
    except Exception as ex:
        logger.info("[Exception otp email]: {0}".format(ex))


def sent_otp_email(data=None, receiver=None, subject=None):
    try:
        date = datetime.now().date()
        file_stream = open(settings.EMAIL_DIR+'/otp_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"otp": data})
        body = template.render(context)
        mail_detail = settings.OTP_MAIL
        send_email(sender = mail_detail['sender'], receiver = receiver, 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception otp email]: {0}".format(ex))
    
def send_ucn_request_alert(data=None):
    try:
        file_stream = open(settings.EMAIL_DIR+'/ucn_request_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data})
        body = template.render(context)
        mail_detail = settings.UCN_RECOVERY_MAIL_DETAIL
        
        send_email(sender = mail_detail['sender'], receiver = mail_detail['receiver'], 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception ucn request email]: {0}".format(ex))
    
def send_feedback_received(data, receiver_email):
    try:
        file_stream = open(settings.EMAIL_DIR+'/base_email_template.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data['content']})
        body = template.render(context)
        send_email(sender = data['sender'], receiver = receiver_email, 
                   subject = data['newsubject'], body = body, message=data['content'],
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception feedback received email]: {0}".format(ex))

def send_due_date_exceeded(data, receiver_email):
    try:
        file_stream = open(settings.EMAIL_DIR+'/base_email_template.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data['content']})
        body = template.render(context)
        send_email(sender = data['sender'], receiver = receiver_email, 
                   subject = data['subject'], body = body, message=data['content'],
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception due date exceeded email]: {0}".format(ex))


def send_due_date_reminder(data, receiver_email):
    try:
        file_stream = open(settings.EMAIL_DIR+'/base_email_template.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data['content']})
        body = template.render(context)
        send_email(sender = data['sender'], receiver = receiver_email, 
                   subject = data['subject'], body = body, message=data['content'],
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception due date reminder email]: {0}".format(ex))
        
def send_servicedesk_feedback(data, reporter_email_id):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver= reporter_email_id, message=data['content'])
    except Exception as ex:
        logger.info("[Exception feedback initiator email]  {0}".format(ex))

def send_dealer_feedback(data, dealer_email):
    try:
        file_stream = open(settings.EMAIL_DIR+'/base_email_template.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data['content']})
        body = template.render(context)
        send_email(sender = data['sender'], receiver = dealer_email, 
                   subject = data['subject'], body = body, message=data['content'],
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception dealer feedback email]: {0}".format(ex))
        

def send_email_to_assignee(data, assignee_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                             data, receiver = assignee_email, message=data['content'])
    except Exception as ex:
        logger.info("[Exception feedback receiver email]  {0}".format(ex)) 
        
def send_email_to_initiator_after_issue_assigned(data, reporter_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver=reporter_email, message=data['content'])
    except Exception as ex:
        logger.info("[Exception feedback initiator after issue assigned email]  {0}".format(ex)) 

def send_email_to_dealer_after_issue_assigned(data, dealer_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver=dealer_email, message=data['content'])
    except Exception as ex:
        logger.info("[Exception feedback initiator after issue assigned email]  {0}".format(ex)) 

def send_email_to_initiator_after_issue_resolved(data, feedback_obj, host, reporter_email):
    try:
        context = Context({"content": data['content'],
                            "id":feedback_obj.id,
                            "url":host,
                            })
        send_template_email("initiator_feedback_resolved.html", context,
                            data, receiver=reporter_email, message=data['content'])
    except Exception as ex:
        logger.info("[Exception feedback initiator after issue resloved email]  {0}".format(ex))

def send_email_to_initiator_when_due_date_is_changed(data, reporter_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver=reporter_email, message=data['content'])
    except Exception as ex:
        logger.info("[Exception feedback initiator on change of due date]  {0}".format(ex)) 

        
def send_email_to_bajaj_after_issue_resolved(data):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context, data, message=data['content'])
    except Exception as ex:
        logger.info("[Exception fail to send mail to bajaj]  {0}".format(ex)) 

def send_email_to_manager_after_issue_resolved(data, manager_obj):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                             data, receiver = manager_obj.email_id, message=data['content'])
    except Exception as ex:
        logger.info("[Exception fail to send mail to manager]  {0}".format(ex))         
           
def send_template_email(template_name, context, mail_detail,receiver=None, message=None): 
    '''generic function use for send mail for any html template'''
    
    file_stream = open(settings.EMAIL_DIR+'/'+ template_name)
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    body = template.render(context)
    if receiver is None:
        receiver =  mail_detail['receiver']
    send_email(sender =  mail_detail['sender'], receiver = receiver, 
               subject = mail_detail['newsubject'], body = body, message=message,
               smtp_server = settings.MAIL_SERVER)
    logger.info("Mail sent successfully")
    #TODO We have to remove hard code receiver

def send_mail_when_vin_does_not_exist(data=None):
    try:
        file_stream = open(settings.TEMPLATE_DIR+'/portal/vin_does_not_exist.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data})
        body = template.render(context)
        mail_detail = settings.VIN_DOES_NOT_EXIST_DETAIL
        send_email(sender=mail_detail['sender'], receiver=mail_detail['receiver'],
                   subject=mail_detail['subject'], body=body,
                   smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception VIN not found email]: {0}".format(ex))


def send_asc_registration_mail(data=None):
    try:
        file_stream = open(settings.TEMPLATE_DIR+'/asc_username_password_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data})
        body = template.render(context)
        mail_detail = settings.REGISTER_ASC_MAIL_DETAIL

        send_email(sender = mail_detail['sender'], receiver = data['receiver'], 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception asc registration email]: {0}".format(ex))

def send_recovery_email_to_admin(file_obj, coupon_data):
    file_location = file_obj.file_location
    reason = file_obj.reason
    customer_id = file_obj.customer_id
    requester = str(file_obj.user.user.username)
    data = get_email_template('UCN_REQUEST_ALERT')['body'].format(requester,coupon_data.service_type,
                customer_id, coupon_data.actual_kms, reason, file_location)
    send_ucn_request_alert(data=data)
