from gladminds.mail import send_email_to_assignee

def send_sms(sender, **kwargs):
    instance_object = kwargs['instance']
    send_email_to_assignee(instance_object)
