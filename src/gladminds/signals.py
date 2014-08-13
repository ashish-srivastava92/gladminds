from gladminds.mail import send_email_to_assignee, \
     send_email_to_initiator_after_issue_assigned, \
     send_email_to_initiator_after_issue_resolved
from gladminds import  message_template as templates
from gladminds.utils2 import get_task_queue , send_sms_servicedesk
from gladminds.audit import audit_log
from django.conf import settings
from gladminds.mail import send_email_to_assignee, send_status_mail_to_assignee

# from gladminds.sqs_tasks import send_registration_detail, send_service_detail, \
#     send_coupon_detail_customer, send_coupon

_all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'
angular_format = lambda x: x.replace('{', '<').replace('}', '>')


def send_sms(sender, **kwargs):
    instance_object = kwargs['instance']
    # Reporter and assinge phone get here
        
    if instance_object.assign_to:
        send_email_to_assignee(instance_object)
        send_email_to_initiator_after_issue_assigned(instance_object)
        template = templates.get_template('INITIATOR_FEEDBACK_DETAILS')
        msg_list = template.format(instance_object.type, instance_object.assign_to, instance_object.priority) 
        print msg_list
        if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add("send_sms_servicedesk", {"phone_number":instance_object.reporter.phone_number, "message": message})
        else:
            send_sms_servicedesk.delay(phone_number=instance_object.reporter.phone_number, message=message)
        audit_log(reciever=instance_object.reporter.phone_number, action=AUDIT_ACTION, message=message)
        return {'status': True, 'message': message}
     
    if instance_object.status == 'Resolved' :
       send_email_to_initiator_after_issue_resolved(instance_object)
       try:
         message = templates.get_template('INITIATOR_FEEDBACK_STATUS')
         print "sss", message
       except Exception as ex:
            message = templates.get_template('INITIATOR_FEEDBACK_STATUS')
       if settings.ENABLE_AMAZON_SQS:
                 task_queue = get_task_queue()
                 task_queue.add("send_sms_servicedesk", {"phone_number":instance_object.reporter.phone_number, "message": message})
       else:
             send_sms_servicedesk.delay(phone_number=instance_object.reporter.phone_number, message=message)
       audit_log(reciever=instance_object.reporter.phone_number, action=AUDIT_ACTION, message=message)
       return {'status': True, 'message': message}
        
    if instance_object.status=='Resolved':
            send_status_mail_to_assignee(instance_object)
