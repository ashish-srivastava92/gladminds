from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from gladminds.models import GladMindUsers

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