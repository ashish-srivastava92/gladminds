from django.db import models
from django.contrib.auth.models import User

from gladminds.core import base_models

_APP_NAME = 'demo'


class BrandProductCategory(base_models.BrandProductCategory):
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Categories"


class UserProfile(base_models.UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='demo_users')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Users"


class Dealer(base_models.Dealer):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='demo_registered_dealer')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Dealer Data"


class AuthorizedServiceCenter(base_models.AuthorizedServiceCenter):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='demo_registered_asc')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Service center Data"


class ServiceAdvisor(base_models.ServiceAdvisor):
    user = models.OneToOneField(UserProfile, primary_key=True,
                            related_name='demo_service_advisor')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)
    asc = models.ForeignKey(AuthorizedServiceCenter, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Service Advisor Data"


class ServiceDeskUser(base_models.ServiceDeskUser):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "reporter info"


class Feedback(base_models.Feedback):
    reporter = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='demo_feedback_reporter')
    assignee = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='demo_feedback_assignee')
    previous_assignee = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='demo_previous_assignee')
    
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user feedback"


class Activity(base_models.Activity):
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user activity info"


class Comment(base_models.Comment):
    feedback_object = models.ForeignKey(Feedback, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user comments"


class FeedbackEvent(base_models.FeedbackEvent):
    feedback = models.ForeignKey(Feedback, null=True, blank=True)
    user = models.ForeignKey(ServiceDeskUser, null=True, blank=True)
    activity = models.ForeignKey(Activity, null=True, blank=True)
     
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user feedback event "


class ProductType(base_models.ProductType):
    brand_product_category = models.ForeignKey(
            BrandProductCategory, null=True, blank=True, related_name='demo_product_type')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Type"


class ProductData(base_models.ProductData):
    product_type = models.ForeignKey(ProductType, null=True, blank=True)
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Data"


class CouponData(base_models.CouponData):
    product = models.ForeignKey(ProductData, null=False, editable=False)
    service_advisor = models.ForeignKey(ServiceAdvisor, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Coupon Information"


class ServiceAdvisorCouponRelationship(base_models.ServiceAdvisorCouponRelationship):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor = models.ForeignKey(ServiceAdvisor, null=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = 'Service Advisor And Coupon Relationship'


class UCNRecovery(base_models.UCNRecovery):
    user = models.ForeignKey(UserProfile, related_name='demo_ucn_recovery')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "UCN recovery logs"


class OldFscData(base_models.OldFscData):
    product = models.ForeignKey(ProductData, null=True, blank=True)
    dealer = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Old Coupon Information"


class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='demo_otp_token')

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


class ASCTempRegistration(base_models.ASCTempRegistration):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "ASC Save Form"


class SATempRegistration(base_models.SATempRegistration):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "SA Save Form"


class CustomerTempRegistration(base_models.CustomerTempRegistration):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Customer temporary info"


class SparesData(base_models.SparesData):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "spare info"


class UserPreference(base_models.UserPreference):
    user = models.ForeignKey(UserProfile)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user preferences"
        unique_together = ("user", "key")


class SMSLog(base_models.SMSLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "SMS Log"


class EmailLog(base_models.EmailLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Log"


class DataFeedLog(base_models.DataFeedLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Feed Log"


class AuditLog(base_models.AuditLog):
    user = models.ForeignKey(UserProfile)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Audit Log"

class SLA(base_models.SLA):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "SLA config"