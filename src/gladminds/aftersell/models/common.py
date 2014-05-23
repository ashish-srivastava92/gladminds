from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User


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
        app_label = "aftersell"
        verbose_name_plural = "Upload Product Data"


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


