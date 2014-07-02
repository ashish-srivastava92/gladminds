from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from gladminds.models.common import GladMindUsers

class OTPToken(models.Model):
    user = models.ForeignKey(GladMindUsers, null=False, blank=False)
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        app_label = "afterbuy"
        verbose_name_plural = "OTPs"
