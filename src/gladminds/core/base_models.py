from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from composite_field.base import CompositeField
from django.conf import settings
from django.utils.translation import gettext as _
from constance import config

from gladminds.core.managers import user_manager
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE, RATINGS,\
                            ROOT_CAUSE, SLA_PRIORITY, TIME_UNIT
from gladminds.core.model_helpers import PhoneField
from gladminds.afterbuy.managers.email_token_manager import EmailTokenManager
from gladminds.core.managers.mail import send_email_activation,\
    sent_password_reset_link
try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now





class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    phone_number = models.CharField(
                   max_length=15, blank=True, null=True)
    image_url = models.CharField(
                   max_length=200, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other'),
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              blank=True, null=True)

    class Meta:
        verbose_name_plural = "User Profile"
        abstract = True
        
    def __unicode__(self):
        return self.phone_number or 'None'


class Industry(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Industries"

    def __unicode__(self):
        return self.name


class Brand(BaseModel):
    name = models.CharField(max_length=250)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Brand Data"

    def __unicode__(self):
        return "Brand: "+self.name+" Industry: "+self.industry.name


class BrandProductCategory(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Brand Categories"


class OTPToken(BaseModel):
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "OTPs"

    def __unicode__(self):
        return self.email+" "+self.phone_number


class Dealer(BaseModel):
    dealer_id = models.CharField(
        max_length=25, blank=False, null=False, unique=True,
        help_text="Dealer Code must be unique")

    objects = user_manager.DealerManager()

    class Meta:
        abstract = True
        verbose_name_plural = "Dealer Data"

    def __unicode__(self):
        return self.dealer_id


class AuthorizedServiceCenter(BaseModel):
    asc_id = models.CharField(
        max_length=25, blank=False, null=False, unique=True,
        help_text="Dealer Code must be unique")

    class Meta:
        abstract = True
        verbose_name_plural = "Service Center Data"

    def __unicode__(self):
        return self.asc_id


class ServiceAdvisor(BaseModel):
    service_advisor_id = models.CharField(
        max_length=15, blank=False, unique=True, null=False)
    status = models.CharField(max_length=10, blank=False, null=False)

    objects = user_manager.ServiceAdvisorManager()

    class Meta:
        abstract = True
        verbose_name_plural = "Service Advisor Data"

    def __unicode__(self):
        return self.service_advisor_id

'''
ProductTypeData  is linked to Brand data
For 1 Brand there can be multiple Products
'''


class ProductType(BaseModel):
    product_type = models.CharField(max_length=255, unique=True, null=False)
    image_url = models.CharField(
                   max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Product Type"

    def __unicode__(self):
        return self.product_type

####################################################################

class ProductData(BaseModel):
    product_id = models.CharField(max_length=215, unique=True)
    customer_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)
    customer_phone_number = PhoneField(null=True, blank=True)
    customer_name = models.CharField(
        max_length=215, null=True, blank=True)
    customer_city = models.CharField(
        max_length=100, null=True, blank=True)
    customer_state = models.CharField(
        max_length=100, null=True, blank=True)
    customer_pincode = models.CharField(
        max_length=15, null=True, blank=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    veh_reg_no = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
        
    class Meta:
        abstract = True
        verbose_name_plural = "Product Data"

    def __unicode__(self):
        return self.product_id


STATUS_CHOICES = ((1, 'Unused'), (2, 'Closed'), (
    3, 'Expired'), (4, 'In Progress'), (
       5, 'Exceeds Limit'), (6, 'Closed Old Fsc'))

class CouponData(BaseModel):
    unique_service_coupon = models.CharField(
        max_length=215, unique=True, null=False)
    valid_days = models.IntegerField(max_length=10, null=False)
    valid_kms = models.IntegerField(max_length=10, null=False)
    service_type = models.IntegerField(max_length=10, null=False)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, db_index=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    mark_expired_on = models.DateTimeField(null=True, blank=True)
    actual_service_date = models.DateTimeField(null=True, blank=True)
    actual_kms = models.CharField(max_length=10, null=True, blank=True)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    schedule_reminder_date = models.DateTimeField(null=True, blank=True)
    extended_date = models.DateTimeField(null=True, blank=True)
    sent_to_sap = models.BooleanField(default=False)
    credit_date = models.DateTimeField(null=True, blank=True)
    credit_note = models.CharField(max_length=50, null=True, blank=True)
    special_case = models.BooleanField(default=False)

    class Meta:
        abstract = True
        verbose_name_plural = "Coupon Information"

    def __unicode__(self):
        return self.unique_service_coupon

class ServiceAdvisorCouponRelationship(BaseModel):
    
    class Meta:
        abstract = True
        verbose_name_plural = 'Service Advisor And Coupon Relationship'

class UCNRecovery(BaseModel):
    reason = models.TextField(null=False)
    customer_id = models.CharField(max_length=215, null=True, blank=True)
    file_location = models.CharField(max_length=215, null=True, blank=True)
    unique_service_coupon = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "UCN recovery logs"
        
class OldFscData(BaseModel):
    unique_service_coupon = models.CharField(
        max_length=215, null=True)
    valid_days = models.IntegerField(max_length=10, null=True)
    valid_kms = models.IntegerField(max_length=10, null=True)
    service_type = models.IntegerField(max_length=10, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, db_index=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    mark_expired_on = models.DateTimeField(null=True, blank=True)
    actual_service_date = models.DateTimeField(null=True, blank=True)
    actual_kms = models.CharField(max_length=10, null=True, blank=True)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    schedule_reminder_date = models.DateTimeField(null=True, blank=True)
    extended_date = models.DateTimeField(null=True, blank=True)
    sent_to_sap = models.BooleanField(default=False)
    credit_date = models.DateTimeField(null=True, blank=True)
    credit_note = models.CharField(max_length=50, null=True, blank=True)
    special_case = models.BooleanField(default=False)
    missing_field = models.CharField(max_length=50, null=True, blank=True)
    missing_value = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True
        app_label = "gladminds"
        verbose_name_plural = "Old Coupon Information"

##################################################################
####################Message Template DB Storage###################


class MessageTemplate(BaseModel):
    template_key = models.CharField(max_length=255, unique=True, null=False)
    template = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Message Template"

##################################################################
####################Message Template DB Storage###################


class EmailTemplate(BaseModel):
    template_key = models.CharField(max_length=255, unique=True, null=False,\
                                     blank=False)
    sender = models.CharField(max_length=512, null=False)
    receiver = models.CharField(max_length=512, null=False)
    subject = models.CharField(max_length=512, null=False)
    body = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Email Template"

########################## TempRegistration #########################

class ASCTempRegistration(BaseModel):
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False,
                                                         unique=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.now)
    dealer_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "ASC Save Form"

class SATempRegistration(BaseModel):
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "SA Save Form"
    

class CustomerTempRegistration(BaseModel):
    new_customer_name = models.CharField(max_length=50, null=True, blank=True)
    new_number = models.CharField(max_length=15)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    temp_customer_id = models.CharField(max_length=50, null=False, blank=False, unique=True)
    sent_to_sap = models.BooleanField(default=False)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    tagged_sap_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)

    objects = user_manager.CustomerTempRegistrationManager()

    class Meta:
        abstract = True
        verbose_name_plural = "Customer temporary info"

    def __unicode__(self):
        return self.new_customer_name

#############################################################


class SparesData(BaseModel):
    spare_name = models.CharField(max_length=50, null=True, blank=True)
    spare_contact = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "spares data"


class EmailToken(models.Model):
    ACTIVATED = u"ALREADY_ACTIVATED"
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = EmailTokenManager()

    class Meta:
        abstract = True
        verbose_name_plural = 'email_tokens'

        def __unicode__(self):
            return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        import datetime
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        Key expiration is determined by a two-step process:
        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.user.date_joined + expiration_date <= datetime_now())
    activation_key_expired.boolean = True

    def send_activation_email(self, reciever_email, site, trigger_mail):
        """
        Send an activation email to the user associated with this
        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'base_url':settings.DOMAIN_BASE_URL}
        if trigger_mail == 'forgot-password':
            ctx_dict = {'activation_key': self.activation_key,
                    'link': config.AFTERBUY_FORGOT_PASSWORD_URL}
            sent_password_reset_link(reciever_email, ctx_dict)
        else:
            send_email_activation(reciever_email, ctx_dict)

class UserPreference(BaseModel):
    """
    This model is used for storing user preferences
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    class Meta:
        abstract = True
        verbose_name_plural = "User Preferences"


class BrandPreference(UserPreference):

    class Meta:
        abstract = True
        verbose_name_plural = "Brand Preferences"


class SMSLog(BaseModel):
    action = models.CharField(max_length=250)
    message = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=15)
    receiver = models.CharField(max_length=15)
    status = models.CharField(max_length=20)

    class Meta:
        abstract = True
        verbose_name_plural = "SMS Log"

class EmailLog(BaseModel):
    subject = models.CharField(max_length=250, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=100, null=True, blank=True)
    receiver = models.TextField()
    cc = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Email Log"

class DataFeedLog(models.Model):
    data_feed_id = models.AutoField(primary_key=True)
    feed_type = models.CharField(max_length=50, null=False)
    total_data_count = models.IntegerField(null=False)
    failed_data_count = models.IntegerField(null=False)
    success_data_count = models.IntegerField(null=False)
    action = models.CharField(max_length=50, null=False)
    status = models.BooleanField(null=False)
    timestamp = models.DateTimeField(default=datetime.now)
    remarks = models.CharField(max_length=2048, null=True, blank=True)
    file_location = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Feed Log"


class AuditLog(BaseModel):
    device = models.CharField(max_length=250, null=True, blank=True)
    user_agent = models.CharField(max_length=250, null=True, blank=True)
    urls = models.CharField(max_length=250)
    access_token = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Audit log"

class ServiceDeskUser(BaseModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Service Desk Users"


class Activity(BaseModel):
    action = models.TextField(null=True, blank=True)
    original_value = models.CharField(max_length=512, null=True, blank=True)
    new_value = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Activity info"


class Feedback(BaseModel):
    summary = models.CharField(max_length=512, null=True, blank=True)
    description = models.CharField(max_length=512, null=True, blank=False)
    status = models.CharField(max_length=12, choices=FEEDBACK_STATUS)
    priority = models.CharField(max_length=12, choices=PRIORITY, default='Low')
    type = models.CharField(max_length=20, choices=FEEDBACK_TYPE)
    closed_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    pending_from = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    wait_time = models.FloatField(max_length=20, null=True, blank=True, default = '0.0')
    remarks = models.CharField(max_length=512, null=True, blank=True)
    ratings = models.CharField(max_length=20, choices=RATINGS)
    root_cause = models.CharField(max_length=20, choices=ROOT_CAUSE)
    resolution = models.CharField(max_length=512, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    assign_to_reporter = models.BooleanField(default=False)
    assignee_created_date = models.DateTimeField(null=True, blank=True)
    reminder_date = models.DateTimeField(null=True, blank=True)
    reminder_flag = models.BooleanField(default=False)
    resolution_flag = models.BooleanField(default=False)

    class Meta:
        abstract = True
        verbose_name_plural = "Feedback info"


class Comment(BaseModel):
    user = models.CharField(max_length=20, null=False, blank=False)
    comment = models.CharField(max_length=100, null=True, blank=True)
    file_location = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Comment info"

class FeedbackEvent(BaseModel):
    class Meta:
        abstract = True
        verbose_name_plural = "Feedback Event info"

    
class Duration(CompositeField):
    time = models.PositiveIntegerField()
    unit = models.CharField(max_length=12, choices=TIME_UNIT, verbose_name = 'unit')

class SLA(models.Model):
    priority = models.CharField(max_length=12, choices=SLA_PRIORITY, unique=True)
    response = Duration()
    reminder = Duration()
    resolution = Duration()
        
    def get_time_in_seconds(self, time , unit):
        if unit == 'days':
            total_time = time * 86400
        elif unit == 'hrs':
            total_time = time * 3600
        else:
            total_time = time * 60
        return total_time
    
    def clean(self, *args, **kwargs):
        response_time = self.get_time_in_seconds(self.response_time, self.response_unit)
        resolution_time = self.get_time_in_seconds(self.resolution_time, self.resolution_unit)
        reminder_time = self.get_time_in_seconds(self.reminder_time, self.reminder_unit)
        
        if reminder_time > response_time and resolution_time > reminder_time:
            super(SLA, self).clean(*args, **kwargs)
        else:
            raise ValidationError("Ensure that Reminder time is greater than Response time and Resolution time is greater than Reminder time")
            
    
    class Meta:
        abstract = True
        verbose_name_plural = "SLA info"
