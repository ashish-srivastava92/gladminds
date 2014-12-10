from django.conf import settings
from django.template import Context, Template

import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging
from gladminds.core.managers import audit_manager
from gladminds.core.utils import get_email_template

logger = logging.getLogger("gladminds")


def send_email(sender, receiver, subject, body, smtp_server=settings.MAIL_SERVER, title='GCP_Bajaj_FSC_Feeds'):
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
        audit_manager.email_log(subject, body, sender, receiver);
        return True
    except Exception as ex:
        logger.error('Exception while sending mail: {0}'.format(ex))
        return False


def send_email_activation(receiver_email, data=None):
    file_stream = open(settings.EMAIL_DIR+'/activation_email.html')
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    context = Context(data)
    body = template.render(context)
    mail_detail = settings.EMAIL_ACTIVATION_MAIL
    send_email(sender=mail_detail['sender'],
               receiver=receiver_email,
               subject=mail_detail['subject'], body=body,
               smtp_server=settings.MAIL_SERVER, title='Support')


def send_recycle_mail(sender_id, data=None):
    file_stream = open(settings.EMAIL_DIR+'/recycle_email.html')
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    context = Context(data)
    body = template.render(context)
    mail_detail = settings.RECYCLE_MAIL
    send_email(sender=sender_id,
               receiver=mail_detail['receiver'],
               subject=mail_detail['subject'], body=body,
               smtp_server=settings.MAIL_SERVER, title='Recycle Product')



def feed_report(feed_data = None):
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


def feed_failure_report(remarks = None, feed_type=None):
    try:
        file_stream = open(settings.EMAIL_DIR+'/feed_failure_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"remarks": remarks, "feed_type": feed_type})
        body = template.render(context)
        mail_detail = settings.FEED_FAILURE_MAIL_DETAIL
        send_email(sender=mail_detail['sender'],
                   receiver=mail_detail['receiver'],
                   subject=mail_detail['subject'], body=body,
                   smtp_server=settings.MAIL_SERVER)

    except Exception as ex:
        logger.info("[Exception feed_failure_report]: {0}".format(ex))


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


def sent_password_reset_link(receiver=None, data=None):
    try:
        file_stream = open(settings.EMAIL_DIR+'/password_reset_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context(data)
        body = template.render(context)
        mail_detail = settings.PASSWORD_RESET_MAIL
        send_email(sender = mail_detail['sender'], receiver = receiver, 
                   subject = mail_detail['subject'], body = body,
                   smtp_server = settings.MAIL_SERVER, title='Support')
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
                   subject = data['subject'], body = body, 
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
                   subject = data['subject'], body = body, 
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
                   subject = data['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception due date reminder email]: {0}".format(ex))
        
def send_servicedesk_feedback(data, reporter_email_id):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver= reporter_email_id)
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
                   subject = data['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception dealer feedback email]: {0}".format(ex))
        

def send_email_to_assignee(data, assignee_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                             data, receiver = assignee_email)
    except Exception as ex:
        logger.info("[Exception feedback receiver email]  {0}".format(ex)) 
        
def send_email_to_initiator_after_issue_assigned(data, reporter_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver=reporter_email)
    except Exception as ex:
        logger.info("[Exception feedback initiator after issue assigned email]  {0}".format(ex)) 

def send_email_to_initiator_after_issue_resolved(data, feedback_obj, host, reporter_email):
    try:
        context = Context({"content": data['content'],
                            "id":feedback_obj.id,
                            "url":host,
                            })
        send_template_email("initiator_feedback_resolved.html", context,
                            data, receiver=reporter_email)
    except Exception as ex:
        logger.info("[Exception feedback initiator after issue resloved email]  {0}".format(ex))

def send_email_to_initiator_when_due_date_is_changed(data, reporter_email):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                            data, receiver=reporter_email)
    except Exception as ex:
        logger.info("[Exception feedback initiator on change of due date]  {0}".format(ex)) 

        
def send_email_to_bajaj_after_issue_resolved(data):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context, data)
    except Exception as ex:
        logger.info("[Exception fail to send mail to bajaj]  {0}".format(ex)) 

def send_email_to_manager_after_issue_resolved(data, manager_obj):
    try:
        context = Context({"content": data['content']})
        send_template_email("base_email_template.html", context,
                             data, receiver = manager_obj.email_id)
    except Exception as ex:
        logger.info("[Exception fail to send mail to manager]  {0}".format(ex))         
           
def send_template_email(template_name, context, mail_detail,receiver=None): 
    '''generic function use for send mail for any html template'''
    
    file_stream = open(settings.EMAIL_DIR+'/'+ template_name)
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    body = template.render(context)
    if receiver is None:
        receiver =  mail_detail['receiver']
    send_email(sender =  mail_detail['sender'], receiver = receiver, 
               subject = mail_detail['newsubject'], body = body, 
               smtp_server = settings.MAIL_SERVER)
    logger.info("Mail sent successfully")
    #TODO We have to remove hard code receiver

def send_mail_when_vin_does_not_exist(data=None):
    try:
        file_stream = open(settings.TEMPLATE_DIR+'/vin_does_not_exist.html')
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
