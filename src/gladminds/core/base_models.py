from datetime import datetime

from django.db import models
from django.conf import settings

from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    USER_DESIGNATION, RATINGS
from gladminds.core.managers import user_manager


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
        abstract = True

class Industry(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Industries"

class Brand(BaseModel):
    brand_id = models.CharField(
        max_length=50, null=False, unique=True, help_text="Brand Id must be unique")
    name = models.CharField(max_length=250, null=False)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Brand Data"

    def __unicode__(self):
        return self.brand_id

    def image_tag(self):
        if self.brand_name == 'Bajaj':
            url = settings.STATIC_URL + 'img/bajaj.jpg'
            return u'<img src= ' + url + ' style="max-width: 37%;max-height: 15%" />'
        elif self.brand_name == 'Honda':
            url = settings.STATIC_URL + 'img/honda.jpg'
            return u'<img src= ' + url + ' style="max-width: 37%;max-height: 15%" />'
        else:
            url = settings.STATIC_URL + 'img/noimage.jpg'
            return u'<img src= ' + url + ' style="max-width: 37%;max-height: 15%" />'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

class OTPToken(BaseModel):
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "OTPs"

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
        return self.dealer_id


class ServiceAdvisor(BaseModel):
    service_advisor_id = models.CharField(
        max_length=15, blank=False, unique=True, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    phone_number = models.CharField(
        max_length=15, blank=False, null=False)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "Service Advisor Data"

    def __unicode__(self):
        return self.phone_number

'''
ProductTypeData  is linked to Brand data
For 1 Brand there can be multiple Products
'''

class ProductType(BaseModel):
    product_type_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, null=False)
    product_type = models.CharField(max_length=255, unique=True, null=False)
    image_url = models.CharField(
                   max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    warranty_email = models.EmailField(max_length=215, null=True, blank=True)
    warranty_phone = models.CharField(
        max_length=15, blank=False, null=False)

    class Meta:
        abstract= True
        verbose_name_plural = "Product Type"

    def __unicode__(self):
        return self.product_type

####################################################################

class ProductData(BaseModel):
    product_id = models.CharField(max_length=215, unique=True)
    customer_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)
    purchase_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    veh_reg_no = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
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
    order = models.PositiveIntegerField(default=0)
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
    request_date = models.DateTimeField(default=datetime.now())
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
    order = models.PositiveIntegerField(default=0)
    extended_date = models.DateTimeField(null=True, blank=True)
    sent_to_sap = models.BooleanField(default=False)
    credit_date = models.DateTimeField(null=True, blank=True)
    credit_note = models.CharField(max_length=50, null=True, blank=True)
    special_case = models.BooleanField(default=False)

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
    reciever = models.CharField(max_length=512, null=False)
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
    
#########################################################################################

"""
Monkey-patch the Site object to include folder for template
"""

class UserPreferences(BaseModel):
    """
    This model is used for storing user preferences
    """
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def unicode(self):
        return self.user_profile

    class Meta:
        abstract = True
        verbose_name_plural = "User Preferences"
        
        
class SMSLog(BaseModel):
    action = models.CharField(max_length=250)
    message = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=15)
    reciever = models.CharField(max_length=15)

    class Meta:
        abstract = True
        verbose_name_plural = "SMS Log"

class EmailLog(BaseModel):
    subject = models.CharField(max_length=250, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=100, null=True, blank=True)
    reciever = models.TextField()
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


class Feedback(BaseModel):
    reporter = models.CharField(max_length=15)
    reporter_email_id = models.CharField(max_length=50, null=True, blank= True)
    message = models.CharField(max_length=512, null=True, blank=False)
    status = models.CharField(max_length=12, choices=FEEDBACK_STATUS)
    priority = models.CharField(max_length=12, choices=PRIORITY)
    type = models.CharField(max_length=12, choices=FEEDBACK_TYPE)
    subject = models.CharField(max_length=512, null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    pending_from = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    wait_time = models.FloatField(max_length=20, null=True, blank=True, default = '0.0')
    remarks = models.CharField(max_length=512, null=True, blank=True)
    ratings = models.CharField(max_length=12, choices=RATINGS)
    root_cause = models.CharField(max_length=512, null=True, blank=True)
    resolution = models.CharField(max_length=512, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "aftersell feedback info"


class Comments(BaseModel):
    user = models.CharField(max_length=20, null=False, blank=False)
    comments_str = models.CharField(max_length=100, null=True, blank=True)
    isDeleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        verbose_name_plural = "aftersell comment info"
