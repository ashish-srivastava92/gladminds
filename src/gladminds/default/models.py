from django.db import models
from django.contrib.auth.models import User

from gladminds.core import base_models
from gladminds.core.auth_helper import GmApps

_APP_NAME = GmApps.GM


class Industry(base_models.Industry):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Industries"


class ServiceType(base_models.BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Service Types"


class Service(base_models.BaseModel):
    service_type = models.ForeignKey(ServiceType)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Services"


class Brand(base_models.Brand):
    industry = models.ForeignKey(Industry)
    services = models.ManyToManyField(Service, through="BrandService",
                                      null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brands"


class BrandProductCategory(base_models.BrandProductCategory):
    brand = models.ForeignKey(Brand)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Categories"


class BrandService(base_models.BaseModel):
    brand = models.ForeignKey(Brand)
    service = models.ForeignKey(Service)
    active = models.BooleanField(default=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        app_label = _APP_NAME


class GladmindsUser(base_models.UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='gm_users')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number


class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(GladmindsUser)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "OTPs"


class MessageTemplate(base_models.MessageTemplate):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Message Template"


class EmailTemplate(base_models.EmailTemplate):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Template"


class AppPreferences(models.Model):

    """
    This model is used for storing application preferences
    """
    brand = models.ForeignKey(Brand, null=False)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    class Meta:
        app_label = _APP_NAME
        unique_together = ("brand", "key")
        verbose_name_plural = "Application Preferences"


class SMSLog(base_models.SMSLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "SMS Log"


class EmailLog(base_models.EmailLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Log"


class AuditLog(base_models.AuditLog):
    user_profile = models.ForeignKey(GladmindsUser)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Audit Log"
