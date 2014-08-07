from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from gladminds.signals import send_sms

##########################################################################
########################## ASC Save Form #########################
ASC_STATUS_CHOICES = ((1, 'In Progress'), (2, 'Failed'))


FEEDBACK_STATUS = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Resolved', 'Resolved'),
        ('Progress', 'Progress'),
    )
PRIORITY = (
        ('Low', 'Low'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Urgent', 'Urgent'),
    )
FEEDBACK_TYPE = (
        ('Problem', 'Problem'),
        ('Question', 'Question'),
        ('Feature', 'Feature'),
        ('Request', 'Request'),
        ('Suggestion', 'Suggestion'),
    )


class ASCSaveForm(models.Model):
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False,
                                                         unique=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.SmallIntegerField(choices=ASC_STATUS_CHOICES, default=1)
    timestamp = models.DateTimeField(default=datetime.now)
    dealer_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "ASC Save Form"


class UCNRecovery(models.Model):
    reason = models.TextField(null=False)
    user = models.ForeignKey(User)
    sap_customer_id = models.CharField(max_length=215, null=True, blank=True)
    file_location = models.CharField(max_length=215, null=True, blank=True)
    request_date = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "UCN recovery logs"

###################################################################

######################DEALER-SA MODELS#############################


class RegisteredDealer(models.Model):
    dealer_id = models.CharField(
        max_length=25, blank=False, null=False, unique=True, help_text="Dealer Code must be unique")
    address = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "Dealer Data"

    def __unicode__(self):
        return self.dealer_id


class ServiceAdvisor(models.Model):
    service_advisor_id = models.CharField(
        max_length=15, blank=False, unique=True, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    phone_number = models.CharField(
        max_length=15, blank=False, null=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "Service Advisor Data"

    def __unicode__(self):
        return self.phone_number


##################################################################
#############Service Advisor and Registered Relationship MODEL####


class ServiceAdvisorDealerRelationship(models.Model):
    dealer_id = models.ForeignKey(RegisteredDealer, null=False)
    service_advisor_id = models.ForeignKey(ServiceAdvisor, null=False)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "Service Advisor And Dealer Relationship"


class RegisteredASC(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    asc_name = models.CharField(max_length=215)
    email_id = models.EmailField(max_length=215, null=True, blank=True)
    registration_date = models.DateTimeField(default=datetime.now())
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    img_url = models.FileField(upload_to="users", blank=True)
    isActive = models.BooleanField(default=True)
    asc_id = models.CharField(
        max_length=20, blank=False, unique=True, null=False)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "Registered ASC Form"
        
    
class Feedback(models.Model):
    reporter = models.ForeignKey('aftersell.ServiceAdvisor', null=False)
    assign_to = models.ForeignKey(User, null=True, blank= True)
    message = models.CharField(max_length=512, null=True, blank=False)
    status = models.CharField(max_length=12, choices=FEEDBACK_STATUS)
    priority = models.CharField(max_length=12, choices=PRIORITY)
    type = models.CharField(max_length=12, choices=FEEDBACK_TYPE)
    subject = models.CharField(max_length=512, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank= False)
    modified_date = models.DateTimeField(null=True, blank= True)
    
    class Meta:
        app_label = "aftersell"
        verbose_name_plural = "aftersell feedback info"
post_save.connect(send_sms,sender=Feedback)       
        