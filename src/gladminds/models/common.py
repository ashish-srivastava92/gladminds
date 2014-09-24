from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

##################BRAND-PRPDUCT MODELS#######################
'''
BrandData contains brand related information
'''


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    phone_number = models.CharField(
                   max_length=15, blank=True, null=True)
    profile_pic = models.CharField(
                   max_length=200, blank=True, null=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "User Profile"

    def __unicode__(self):
        return self.user


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
        app_label = "gladminds"
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
        app_label = "gladminds"
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
    brand_id = models.ForeignKey(BrandData, null=False)
    product_name = models.CharField(max_length=255, null=False)
    product_type = models.CharField(max_length=255, unique=True, null=False)
    product_image_loc = models.FileField(
        upload_to=settings.AFTERBUY_PRODUCT_TYPE_LOC, blank=True)
    isActive = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    warranty_email = models.EmailField(max_length=215, null=True, blank=True)
    warranty_phone = models.CharField(
        max_length=15, blank=True, null=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Product Type"

    def __unicode__(self):
        return self.product_type

#############GLADMINDUSER & CUSTOMERDATA MODEL####################

'''
Gladmindusers have auto generated glamind customer id,
and unique phone numner
'''


class GladMindUsers(models.Model):
    user = models.OneToOneField(UserProfile, null=True, blank=True)
    gladmind_customer_id = models.CharField(
        max_length=215, unique=True, null=True)
    customer_name = models.CharField(max_length=215)
    email_id = models.EmailField(max_length=215, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    registration_date = models.DateTimeField(default=datetime.now())
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.CharField(max_length=255, null=True, blank=True)
    img_url = models.FileField(upload_to="users", blank=True)
    thumb_url = models.FileField(upload_to="users", blank=True)
    isActive = models.BooleanField(default=True)
    #added these attributes for afterbuy application
    accepted_terms = models.BooleanField(default=False)
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other'),
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True, null=True)
    tshirt_size = models.CharField(max_length=2, choices=SIZE_CHOICES, blank=True, null=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number

    def save(self, force_insert=False, force_update=False, using=None):
        return super(GladMindUsers, self).save(force_insert, force_update, using)

'''
CustomerData contains info about
which customer bought which product and
the vin of product and the dealer
'''


class ProductData(models.Model):
    id = models.AutoField(primary_key=True)
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    customer_phone_number = models.ForeignKey(
        GladMindUsers, null=True, blank=True)
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    sap_customer_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    dealer_id = models.ForeignKey('aftersell.RegisteredDealer', null=True, blank=True)
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
        app_label = "gladminds"
        verbose_name_plural = "Product Data"

    def __unicode__(self):
        return self.vin

####################################################################

STATUS_CHOICES = ((1, 'Unused'), (2, 'Closed'), (
    3, 'Expired'), (4, 'In Progress'), (5, 'Exceeds Limit'))


class CouponData(models.Model):
    vin = models.ForeignKey(ProductData, null=False, editable=False)
    unique_service_coupon = models.CharField(
        max_length=215, unique=True, null=False)
    valid_days = models.IntegerField(max_length=10, null=False)
    valid_kms = models.IntegerField(max_length=10, null=False)
    service_type = models.IntegerField(max_length=10, null=False)
    sa_phone_number = models.ForeignKey('aftersell.ServiceAdvisor', null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, db_index=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    mark_expired_on = models.DateTimeField(null=True, blank=True)
    actual_service_date = models.DateTimeField(null=True, blank=True)
    actual_kms = models.CharField(max_length=10, null=True, blank=True)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    schedule_reminder_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    extended_date = models.DateTimeField(null=True, blank=True)
    servicing_dealer = models.ForeignKey('aftersell.RegisteredDealer', null=True, blank=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Coupon Information"

    def __unicode__(self):
        return self.unique_service_coupon

##################################################################
#############Service Advisor and Coupon Relationship MODEL########


class ServiceAdvisorCouponRelationship(models.Model):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor_phone = models.ForeignKey('aftersell.ServiceAdvisor', null=False)
    dealer_id = models.ForeignKey('aftersell.RegisteredDealer', null=True, blank=True)

    class Meta:
        app_label = 'gladminds'
        verbose_name_plural = 'Service Advisor And Coupon Relationship'

##################################################################
####################Message Template DB Storage###################


class MessageTemplate(models.Model):
    template_key = models.CharField(max_length=255, unique=True, null=False)
    template = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Message Template"


####################################################################
########################TOTP Details################################

class OTPToken(models.Model):
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        app_label = "gladminds"
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
        app_label = "gladminds"
        verbose_name_plural = "Email Template"


class SASaveForm(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "SA Save Form"


class CustomerTempRegistration(models.Model):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)
    new_customer_name = models.CharField(max_length=50, null=True, blank=True)
    new_number = models.CharField(max_length=15)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    temp_customer_id = models.CharField(max_length=50, null=False, blank=False, unique=True)
    sent_to_sap = models.BooleanField(default=False)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    tagged_sap_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Customer temporary info"

    def __unicode__(self):
        return self.new_customer_name
    
######################################################################################

class ProductInsuranceInfo(models.Model):
    product = models.ForeignKey(ProductData, null=False)
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
        app_label = "gladminds"
        verbose_name_plural = "product insurance info"
    
#######################################################################################

class ProductWarrantyInfo(models.Model):
    product = models.ForeignKey(ProductData, null=False)
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    warranty_brand_id = models.CharField(max_length=15, null=True, blank=True)
    warranty_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "product warranty info"
        
########################################################################################

class SparesData(models.Model):
    spare_brand = models.ForeignKey(BrandData, null=False)
    spare_name = models.CharField(max_length=50, null=True, blank=True)
    spare_contact = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "spare info"
    
#########################################################################################

class UserPreferences(models.Model):
    """
    This model is used for storing user preferences
    """
    user_details = models.ForeignKey(UserProfile)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def unicode(self):
        return self.user_details

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "User Preferences"
        unique_together = ("user_details", "key")

