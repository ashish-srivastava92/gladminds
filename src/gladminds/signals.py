from gladminds.mail import send_email_to_assignee

def send_sms(sender, **kwargs):
    instance_object = kwargs['instance']
    if instance_object.assign_to:
        send_email_to_assignee(instance_object)
        