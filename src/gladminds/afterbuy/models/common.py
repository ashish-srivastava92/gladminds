from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from gladminds.models import GladMindUsers, ProductData, ProductTypeData

class OTPToken(models.Model):
    user = models.ForeignKey(GladMindUsers, null=False, blank=False)
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "OTPs"
        
class UserNotification(models.Model):
    user = models.ForeignKey(GladMindUsers, null=False, blank=False)
    message = models.CharField(max_length=256, null=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "notification"
<<<<<<< HEAD
        
class UserProducts(models.Model):
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    customer_phone_number = models.ForeignKey(
        GladMindUsers, null=True, blank=True)
    item_name = models.CharField(max_length=256, null=False)
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
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
        
class UserFeedback(models.Model):
    user = models.ForeignKey(GladMindUsers, null=False, blank=False)
    feedback_type = models.CharField(max_length=55, null=False)
    message = models.CharField(max_length=256, null=False)
    
    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "userFeedbacks"
        
=======

class UserMobileInfo(models.Model):
    user = models.ForeignKey(GladMindUsers, null=False, blank=False)
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
>>>>>>> upstream/gm_1_4
