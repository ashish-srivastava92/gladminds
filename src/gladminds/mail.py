from django.conf import settings
from django.template import Context, Template

import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("gladminds")


def send_email(sender, receiver, subject, body, smtp_server=settings.MAIL_SERVER):
    msg = MIMEText(body, 'html', _charset='utf-8')
#   subject = 'Subject: {0}\n'.format(subject)
#   header = "To:{0}\nFrom:{1}\n{2}".format(", ".join(receiver),sender, subject)
#   msg = "{0}\n{1}\n\n ".format(header, msg)
    msg['Subject'] = subject
    msg['To'] = ", ".join(receiver)
    msg['From'] = "GCP_Bajaj_FSC_Feeds<%s>" % sender
    mail = smtplib.SMTP(smtp_server)
    mail.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
    mail.quit()


def feed_report(feed_data = None):
    from gladminds import mail
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        file_stream = open(settings.EMAIL_DIR+'/feed_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"feed_logs": feed_data, "yesterday": yesterday})
        body = template.render(context)
        mail_detail = settings.MAIL_DETAIL
        mail.send_email(sender=mail_detail['sender'],
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
    from gladminds import mail
    try:
        file_stream = open(
            settings.EMAIL_DIR + '/purchase_interest_mail.html')
        item = file_stream.read()
        template = Template(item)
        context = Context({"user": data})
        body = template.render(context)
        mail.send_email(sender=data['email_id'], receiver=receiver,
                        subject=subject, body=body,
                        smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception item purchase report]: {0}".format(ex))


def warrenty_extend(data=None, receiver=None, subject=None):
    from gladminds import mail
    try:
        file_stream = open(
            settings.EMAIL_DIR + '/warrenty_extend_mail.html')
        item = file_stream.read()
        template = Template(item)
        context = Context({"user": data})
        body = template.render(context)
        mail.send_email(sender=data['email_id'], receiver=receiver,
                        subject=subject, body=body,
                        smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception item warrenty extend]: {0}".format(ex))


def insurance_extend(data=None, receiver=None, subject=None):
    from gladminds import mail
    try:
        file_stream = open(
            settings.EMAIL_DIR + '/insurance_extend_mail.html')
        item = file_stream.read()
        template = Template(item)
        context = Context({"user": data})
        body = template.render(context)
        mail.send_email(sender=data['email_id'], receiver=receiver,
                        subject=subject, body=body,
                        smtp_server=settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception item insurance extend]: {0}".format(ex))
        

def sent_otp_email(data=None, receiver=None, subject=None):
    from gladminds import mail
    try:
        date = datetime.now().date()
        file_stream = open(settings.EMAIL_DIR+'/otp_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"otp": data})
        body = template.render(context)
        mail_detail = settings.OTP_MAIL
        
        mail.send_email(sender = mail_detail['sender'], receiver = receiver, 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception otp email]: {0}".format(ex))
    
def send_ucn_request_alert(data=None):
    from gladminds import mail
    try:
        file_stream = open(settings.EMAIL_DIR+'/ucn_request_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data})
        body = template.render(context)
        mail_detail = settings.UCN_RECOVERY_MAIL_DETAIL
        
        mail.send_email(sender = mail_detail['sender'], receiver = mail_detail['receiver'], 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception ucn request email]: {0}".format(ex))
    
def send_feedback_received(data=None):
    from gladminds import mail
    try:
        file_stream = open(settings.EMAIL_DIR+'/feedback_received_mail.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({'message': data.message,
                           'reporter': data.reporter,
                           'created_date': data.created_date})
        body = template.render(context)
        mail_detail = settings.FEDBACK_MAIL_DETAIL
        mail.send_email(sender = mail_detail['sender'], receiver = mail_detail['receiver'], 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception ucn request email]: {0}".format(ex))
        
def send_servicedesk_feedback(feedback_details=None):
    try:
        context = Context({'type': feedback_details.type})
        mail_detail = settings.SERVICEDESK_FEEDBACK_MAIL_DETAIL
        send_template_email("servicedesk_feedback_inititator.html", context, 
                            "Exception feedback receiver email", mail_detail, 
                            receiver="srv.sngh@gmail.com")
    except Exception as ex:
        logger.info("[Exception feedback receiver email]  {0}".format(ex))
    
def send_template_email(template_name,context,exceptionstring, mail_detail,receiver=None): 
    '''generic function use for send mail for any html template'''
    
    file_stream = open(settings.EMAIL_DIR+'/'+ template_name)
    feed_temp = file_stream.read()
    template = Template(feed_temp)
    body = template.render(context)
    #TODO We have to remove hard code receiver
    if receiver is None:
        receiver = mail_detail['receiver']
    
    send_email(sender = mail_detail['sender'], receiver = receiver, 
               subject = mail_detail['subject'], body = body, 
               smtp_server = settings.MAIL_SERVER)
    logger.info("Mail sent successfully")
       
            
              
