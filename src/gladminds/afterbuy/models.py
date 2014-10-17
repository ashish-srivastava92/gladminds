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
        

class UserProducts(models.Model):
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    consumer_phone_number = models.ForeignKey(
        Consumer, null=True, blank=True)
    item_name = models.CharField(max_length=256, null=False)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    purchased_from = models.CharField(max_length=255, null=True, blank=True)
    seller_email = models.EmailField(max_length=255, null=True, blank=True)
    seller_phone = models.CharField(max_length=255, null=True, blank=True)
    warranty_yrs = models.FloatField(null=True, blank=True)
    insurance_yrs = models.FloatField(null=True, blank=True)
    invoice_loc = models.FileField(upload_to="invoice", blank=True)
    warranty_loc = models.FileField(upload_to="warrenty", blank=True)
    insurance_loc = models.FileField(upload_to="insurance", blank=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "userProducts"
    
    def __unicode__(self):
        return self.vin    
       
class UserMobileInfo(models.Model):
    user = models.ForeignKey(Consumer, null=False, blank=False)
    IMEI = models.CharField(max_length=50, null=True, blank=True, unique=True)
    ICCID = models.CharField(max_length=50, null=True, blank=True)
    phone_name = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "mobile info"


class ProductInsuranceInfo(BaseModel):
    product = models.ForeignKey(UserProducts, null=False)
    insurance_brand_id = models.CharField(max_length=15, null=True, blank=True)
    insurance_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    insurance_email = models.EmailField(max_length=215, null=True, blank=True)
    insurance_phone = models.CharField(
        max_length=15, blank=False, null=False)
    image_url = models.CharField(max_length=215, null=True, blank=True)
    insurance_agency_name =  models.CharField(max_length=215, null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    insurance_type = models.CharField(max_length=15,null=True, blank=True)
    vehicle_value = models.FloatField(min_value=0.0)
    nominee = models.CharField(max_length=15,blank=True,null=True)
    support_contact = models.CharField(max_length=12,blank=True,null=True)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "product insurance info"


class ProductWarrantyInfo(BaseModel):
    product = models.ForeignKey(UserProducts, null=False)
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

class PollutionCertificate(BaseModel):
    pucc_number = models.CharField()
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    image_url = models.CharField(max_length=215, null=True, blank=True)
    
    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "Pollution Certificate"


class RegistrationCertificate(BaseModel):
    vehicle_registration_number = models.CharField()
    registration_date = models.DateTimeField(null=True, blank=False)
    chassis_number = models.CharField()
    engine_number = models.CharField()
    owner_name = models.CharField(max_length=512)
    address = models.CharField(max_length=512)
    registration_upto = models.DateTimeField(null=True, blank=False)
    manufacturer = models.CharField(max_length=512)
    manufacturing_date = models.DateTimeField(null=True, blank=False)
    model_number = models.CharField()
    colour = models.CharField()
    image_url = models.CharField(max_length=215, null=True, blank=True)
    
    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "Registration Certificate"
    
class License(BaseModel):
    license_number = models.CharField()
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    blood_group = models.CharField()
    image_url = models.CharField(max_length=215, null=True, blank=True)
    
    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "license"
        
