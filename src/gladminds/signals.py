from gladminds.mail import send_email_to_assignee, send_status_mail_to_assignee


def send_sms(sender, **kwargs):
    instance_object = kwargs['instance']
    if instance_object.assign_to:
        send_email_to_assignee(instance_object)
        phone_number = instance_object.assign_to.phone_number
        print phone_number        
    if instance_object.status=='Resolved':
            send_status_mail_to_assignee(instance_object)


