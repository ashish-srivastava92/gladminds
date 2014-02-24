from django.conf import settings
from django.template import Context, Template

import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging

logger = logging.getLogger("gladminds")

def send_email(sender, receiver, subject, body, smtp_server):
    msg = MIMEText(body, 'html', _charset='utf-8')
    msg['Subject'] = subject
    msg['To'] = receiver
    msg['From'] = "Gladminds<%s>" % sender
    mail = smtplib.SMTP(smtp_server)
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()

def feed_report(feed_data = None):
    from gladminds import mail
    try:
        file_stream = open(settings.TEMPLATE_DIR+'/feed_report.html')
        feed_temp = file_stream.read()
        template = Template(feed_temp)
        context = Context({"feed_logs": feed_data})
        body = template.render(context)
        mail_detail = settings.MAIL_DETAIL
        mail.send_email(sender = mail_detail['sender'], receiver = mail_detail['reciever'], 
                   subject = mail_detail['subject'], body = body, 
                   smtp_server = settings.MAIL_SERVER)
    except Exception as ex:
        logger.info("[Exception feed_report]: {0}".format(ex))
        
