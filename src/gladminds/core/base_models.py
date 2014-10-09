from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from gladminds.gm.models import UserProfile, GladMindUsers
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    USER_DESIGNATION, RATINGS
    

##########################################################################
########################## ASC Save Form #########################
ASC_STATUS_CHOICES = ((1, 'In Progress'), (2, 'Failed'))

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
        abstract = True
        verbose_name_plural = "ASC Save Form"


class UCNRecovery(models.Model):
    reason = models.TextField(null=False)
    sap_customer_id = models.CharField(max_length=215, null=True, blank=True)
    file_location = models.CharField(max_length=215, null=True, blank=True)
    request_date = models.DateTimeField(default=datetime.now())

    class Meta:
        abstract = True
        verbose_name_plural = "UCN recovery logs"

###################################################################

######################DEALER-SA MODELS#############################


class RegisteredDealer(models.Model):
    dealer_id = models.CharField(
        max_length=25, blank=False, null=False, unique=True, help_text="Dealer Code must be unique")
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, default='dealer', blank=False)
    dependent_on = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        abstract = True
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
        abstract = True
        verbose_name_plural = "Service Advisor Data"

    def __unicode__(self):
        return self.phone_number


##################################################################
#############Service Advisor and Registered Relationship MODEL####


class ServiceAdvisorDealerRelationship(models.Model):
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "Service Advisor And Dealer Relationship"


#     NOT IN USE CHECK AND UNCOMMENT IT

# class RegisteredASC(models.Model):
#     user = models.OneToOneField(UserProfile, null=True, blank=True)
#     phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
#     asc_name = models.CharField(max_length=215)
#     email_id = models.EmailField(max_length=215, null=True, blank=True)
#     registration_date = models.DateTimeField(default=datetime.now())
#     address = models.CharField(max_length=255, null=True, blank=True)
#     city = models.CharField(max_length=255, null=True, blank=True)
#     country = models.CharField(max_length=255, null=True, blank=True)
#     state = models.CharField(max_length=255, null=True, blank=True)
#     img_url = models.FileField(upload_to="users", blank=True)
#     isActive = models.BooleanField(default=True)
#     asc_id = models.CharField(
#         max_length=20, blank=False, unique=True, null=False)
#     dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)
# 
#     class Meta:
#         abstract = True
#         verbose_name_plural = "Registered ASC Form"


class ServiceDeskUser(models.Model):
    email_id = models.EmailField(max_length=215, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    designation = models.CharField(max_length=10, choices = USER_DESIGNATION)
    
    class Meta:
        abstract = True
        verbose_name_plural = "service desk users"
    
    def __unicode__(self):
        return self.phone_number        

class Feedback(models.Model):
    reporter = models.CharField(max_length=15)
    reporter_email_id = models.CharField(max_length=50, null=True, blank= True)
    message = models.CharField(max_length=512, null=True, blank=False)
    status = models.CharField(max_length=12, choices=FEEDBACK_STATUS)
    priority = models.CharField(max_length=12, choices=PRIORITY)
    type = models.CharField(max_length=12, choices=FEEDBACK_TYPE)
    subject = models.CharField(max_length=512, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank= False)
    modified_date = models.DateTimeField(null=True, blank= True,auto_now=True)
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


class Comments(models.Model):
    user = models.CharField(max_length=20, null=False, blank=False)
    comments_str = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(null=False, blank=False)
    modified_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    isDeleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        verbose_name_plural = "aftersell comment info"    
    


########################### Models Taken from Gladminds Common ##################

class UploadProductCSV(models.Model):
    file_location = settings.PROJECT_DIR + '/data/'
    upload_brand_feed = models.FileField(upload_to=file_location, blank=True)
    upload_dealer_feed = models.FileField(upload_to=file_location, blank=True)
    upload_product_dispatch_feed = models.FileField(
        upload_to=file_location, blank=True)
    upload_product_purchase_feed = models.FileField(
        upload_to=file_location, blank=True)
    upload_coupon_redeem_feed = models.FileField(
        upload_to=file_location, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Upload Product Data"
        
class BrandData(models.Model):
    pk_brand_id = models.AutoField(primary_key=True)
    brand_id = models.CharField(
        max_length=50, null=False, unique=True, help_text="Brand Id must be unique")
    brand_name = models.CharField(max_length=250, null=False)
    brand_image_loc = models.FileField(
        upload_to=settings.AFTERBUY_BRAND_LOC, blank=True)
    isActive = models.BooleanField(default=True)

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


'''
ProductTypeData  is linked to Brand data
For 1 Brand there can be multiple Products
'''
    
class ProductTypeData(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, null=False)
    product_type = models.CharField(max_length=255, unique=True, null=False)
    product_image_loc = models.FileField(
        upload_to=settings.AFTERBUY_PRODUCT_TYPE_LOC, blank=True)
    isActive = models.BooleanField(default=True)
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

class ProductData(models.Model):
    id = models.AutoField(primary_key=True)
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    sap_customer_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)

    # Added below column for after buy application
    customer_product_number = models.CharField(
        max_length=255, null=True, blank=True)
    purchased_from = models.CharField(max_length=255, null=True, blank=True)
    seller_email = models.EmailField(max_length=255, null=True, blank=True)
    seller_phone = models.CharField(max_length=255, null=True, blank=True)
    warranty_yrs = models.FloatField(null=True, blank=True)
    insurance_yrs = models.FloatField(null=True, blank=True)

    invoice_loc = models.FileField(upload_to="invoice", blank=True)
    warranty_loc = models.FileField(upload_to="warrenty", blank=True)
    insurance_loc = models.FileField(upload_to="insurance", blank=True)

    last_modified = models.DateTimeField(null=False, default=datetime.now())
    created_on = models.DateTimeField(null=True, default=datetime.now())
    isActive = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    veh_reg_no = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Product Data"

    def __unicode__(self):
        return self.vin


STATUS_CHOICES = ((1, 'Unused'), (2, 'Closed'), (
    3, 'Expired'), (4, 'In Progress'), (
       5, 'Exceeds Limit'), (6, 'Closed Old Fsc'))

class CouponData(models.Model):
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

    class Meta:
        abstract = True
        verbose_name_plural = "Coupon Information"

    def __unicode__(self):
        return self.unique_service_coupon

class ServiceAdvisorCouponRelationship(models.Model):
    
    class Meta:
        abstract = True
        verbose_name_plural = 'Service Advisor And Coupon Relationship'


##################################################################
####################Message Template DB Storage###################


class MessageTemplate(models.Model):
    template_key = models.CharField(max_length=255, unique=True, null=False)
    template = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Message Template"

####################################################################
########################TOTP Details################################

class OTPToken(models.Model):
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "OTPs"

##################################################################
####################Message Template DB Storage###################


class EmailTemplate(models.Model):
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


class SASaveForm(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "SA Save Form"
    

class CustomerTempRegistration(models.Model):
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


######################################################################################

class ProductInsuranceInfo(models.Model):
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    insurance_brand_id = models.CharField(max_length=15, null=True, blank=True)
    insurance_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    insurance_email = models.EmailField(max_length=215, null=True, blank=True)
    insurance_phone = models.CharField(
        max_length=15, blank=False, null=False)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "product insurance info"
    
#######################################################################################

class ProductWarrantyInfo(models.Model):
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    warranty_brand_id = models.CharField(max_length=15, null=True, blank=True)
    warranty_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "product warranty info"
        
########################################################################################

class SparesData(models.Model):
    spare_name = models.CharField(max_length=50, null=True, blank=True)
    spare_contact = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        abstract = True
        verbose_name_plural = "spares data"
    
#########################################################################################

"""
Monkey-patch the Site object to include folder for template
"""
# FolderNameField(blank=True).contribute_to_class(Site,'folder_name')