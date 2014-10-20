from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from gladminds.core.base_models import BaseModel, UserProfile, MessageTemplate,\
           EmailTemplate, SMSLog, EmailLog, AuditLog, Industry, Brand, OTPToken

class Industry(Industry):
    
    class Meta:
        app_label = "gm"
        verbose_name_plural = "Industries"

class ServiceType(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Service Types"

class Service(BaseModel):
    type = models.ForeignKey(ServiceType)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Services"

class Brand(Brand):
    industry = models.ForeignKey(Industry)
    services = models.ManyToManyField(Service, through="BrandService")

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Brands"

class BrandService(BaseModel):
    brand = models.ForeignKey(Brand)
    service = models.ForeignKey(Service)
    active = models.BooleanField(default=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"


class GladmindsUser(UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='gm_users')

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number

class OTPToken(OTPToken):
    user = models.ForeignKey(GladmindsUser)

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

class AuditLog(AuditLog):
    user_profile = models.ForeignKey(GladmindsUser)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Audit Log"        
