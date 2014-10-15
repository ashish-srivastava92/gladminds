from django.db import models
from django.contrib.auth.models import User

from gladminds.core.base_models import BaseModel


class GladmindsUser(BaseModel):
    user = models.OneToOneField(User, primary_key=True)
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
    gladmind_customer_id = models.CharField(
        max_length=215, unique=True, null=True)
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
        app_label = "gm"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number


class OTPToken(models.Model):
    user = models.ForeignKey(GladmindsUser)
    token = models.CharField(max_length=256)
    request_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "OTPs"


class UserNotification(models.Model):
    user = models.ForeignKey(GladmindsUser)
    message = models.CharField(max_length=256, null=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "notification"


class UserProducts(models.Model):
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    customer_phone_number = models.ForeignKey(
        GladmindsUser, null=True, blank=True)
    item_name = models.CharField(max_length=256, null=False)
#     product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
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
        app_label = "gm"
        verbose_name_plural = "userProducts"

    def __unicode__(self):
        return self.vin


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
