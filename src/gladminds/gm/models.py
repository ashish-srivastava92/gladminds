from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from gladminds.core.base_models import BaseModel, UserProfile, MessageTemplate,\
           EmailTemplate, SMSLog, EmailLog, AuditLog


class Industry(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Industries"


class Service(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Services"


class Brand(BaseModel):
    brand_id = models.CharField(
        max_length=50, null=False, unique=True, help_text="Brand Id must be unique")
    brand_name = models.CharField(max_length=250, null=False)
    brand_logo = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    industry = models.ForeignKey(Industry)
    services = models.ManyToManyField(Service, through="BrandService")

    class Meta:
        app_label = "gm"
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


class BrandService(BaseModel):
    brand = models.ForeignKey(Brand)
    service = models.ForeignKey(Service)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "gm"


class GladmindsUser(UserProfile):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number

class OTPToken(BaseModel):
    user = models.ForeignKey(GladmindsUser)
    token = models.CharField(max_length=256)
    request_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "OTPs"

class MessageTemplate(MessageTemplate):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Message Template"


class EmailTemplate(EmailTemplate):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Email Template"

class AppPreferences(models.Model):

    """
    This model is used for storing application preferences
    """
    brand = models.ForeignKey(Brand, null=False)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    
    class Meta:
        app_label = "gm"
        unique_together = ("brand", "key")
        verbose_name_plural = "Application Preferences"

class SMSLog(SMSLog):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "SMS Log"
        
class EmailLog(EmailLog):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Email Log"

class AuditLog(base_models.DataFeedLog):
    user_profile = models.ForeignKey(GladmindsUser)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Audit Log"        
