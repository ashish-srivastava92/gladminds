from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from gladminds.core.base_models import BaseModel

class Consumer(BaseModel):
    user = models.OneToOneField(User, primary_key=True)
    consumer_id = models.CharField(
        max_length=215, unique=True, null=True)
    phone_number = models.CharField(
                   max_length=15, blank=True, null=True)
    profile_pic = models.CharField(
                   max_length=200, blank=True, null=True)
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
    #added these attributes for afterbuy application
    accepted_terms = models.BooleanField(default=False)
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    tshirt_size = models.CharField(max_length=2, choices=SIZE_CHOICES,
                                   blank=True, null=True)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "consumer"

    def __unicode__(self):
        return self.phone_number


class Industry(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

class OTPToken(models.Model):
    user = models.ForeignKey(Consumer, null=False, blank=False)
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "OTPs"

class UserNotification(models.Model):
    user = models.ForeignKey(Consumer, null=False, blank=False)
    message = models.CharField(max_length=256, null=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "notifications"
        
        
class AuditLog(models.Model):
    date = models.DateTimeField()
    action = models.CharField(max_length=250)
    message = models.CharField(max_length=250)
    sender = models.CharField(max_length=250)
    reciever = models.CharField(max_length=250)
    status = models.CharField(max_length=250)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "audit logs"

class ProductTypeData(BaseModel):
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
            app_label = "afterbuy"
            verbose_name_plural = "Product Type"

    def __unicode__(self):
        return self.product_type

class ProductData(BaseModel):
    customer_phone_number = models.ForeignKey(
        Consumer, null=True, blank=True, related_name='bajaj_product_date')
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
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

class ProductInsuranceInfo(BaseModel):
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
        app_label = "afterbuy"
        verbose_name_plural = "product insurance info"


class ProductWarrantyInfo(BaseModel):
    product = models.ForeignKey(ProductData, null=False)
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    warranty_brand_id = models.CharField(max_length=15, null=True, blank=True)
    warranty_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "product warranty info"
        
class MessageTemplate(BaseModel):
    template_key = models.CharField(max_length=255, unique=True, null=False)
    template = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "Message Template"



class EmailTemplate(BaseModel):
    template_key = models.CharField(max_length=255, unique=True, null=False,\
                                     blank=False)
    sender = models.CharField(max_length=512, null=False)
    reciever = models.CharField(max_length=512, null=False)
    subject = models.CharField(max_length=512, null=False)
    body = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "Message Template"
        
class UserMobileInfo(models.Model):
    user = models.ForeignKey(GladmindsUser)
    IMEI = models.CharField(max_length=50, null=True, blank=True, unique=True)
    ICCID = models.CharField(max_length=50, null=True, blank=True)
    phone_name = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "mobile info"
