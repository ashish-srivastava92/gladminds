from models import logs
from datetime import datetime
from django.conf import settings

def audit_log(action='SENT', sender='+1 574-212-0423', reciever=None, message=None, status='success'):
    kwargs = {
                'action':action,
                'reciever': reciever,
                'sender':'sender',
                'message': message,
                'status':status
            }
    action_log = logs.AuditLog(date=datetime.now(), action=action, sender=sender, reciever=reciever, status=status, message=message)
    action_log.save()