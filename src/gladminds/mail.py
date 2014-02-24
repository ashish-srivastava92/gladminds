import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def send_email(sender, receiver, subject, body, smtp_server):
    msg = MIMEText(body, 'html', _charset='utf-8')
    msg['Subject'] = subject
    msg['To'] = receiver
    msg['From'] = "Gladminds<%s>" % sender
    mail = smtplib.SMTP(smtp_server)
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()
    