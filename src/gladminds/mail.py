from django.conf import settings
from django.template import Context, Template

import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("gladminds")


def send_email(sender, receiver, subject, body, smtp_server=settings.MAIL_SERVER):
    msg = MIMEText(body, 'html', _charset='utf-8')
    msg['Subject'] = subject
    msg['To'] = receiver
    msg['From'] = sender
    mail = smtplib.SMTP(smtp_server)
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()


def feed_report(feed_data = None):
    from gladminds import mail
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        file_stream = open(settings.TEMPLATE_DIR+'/feed_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"feed_logs": feed_data, "yesterday": yesterday})
        body = template.render(context)
        mail_detail = settings.MAIL_DETAIL
        mail.send_email(sender=mail_detail['sender'],
                   receiver=mail_detail['reciever'],
                   subject=mail_detail['subject'], body=body,
                   smtp_server=settings.MAIL_SERVER)

    except Exception as ex:
        logger.info("[Exception feed_report]: {0}".format(ex))


def feed_report_failure(remarks = None, feed_type=None):
    try:
        yesterday = datetime.now().date() - timedelta(days=1)
        file_stream = open(settings.TEMPLATE_DIR+'/feed_failure_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"remarks": remarks, "feed_type": feed_type})
        body = template.render(context)
        mail_detail = settings.MAIL_DETAIL
        send_email(sender=mail_detail['sender'],
                   receiver=mail_detail['reciever'],
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
            settings.TEMPLATE_DIR + '/purchase_interest_mail.html')
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
            settings.TEMPLATE_DIR + '/warrenty_extend_mail.html')
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
            settings.TEMPLATE_DIR + '/insurance_extend_mail.html')
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
        file_stream = open(settings.TEMPLATE_DIR+'/otp_email.html')
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
        date = datetime.now().date()
        file_stream = open(settings.TEMPLATE_DIR+'/ucn_request_email.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"content": data})
        body = template.render(context)
        mail_detail = settings.UCN_RECOVERY_MAIL
        
        mail.send_email(sender = mail_detail['sender'], receiver = mail_detail['reciever'], 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception ucn request email]: {0}".format(ex))
    

