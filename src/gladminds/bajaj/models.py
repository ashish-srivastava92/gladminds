from django.db import models
from django.contrib.auth.models import User

from gladminds.core import base_models
from gladminds.gm.models import GladmindsUser


class UserProfile(base_models.UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='bajaj_users')

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Brand Users"


class Dealer(base_models.Dealer):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='bajaj_registered_dealer')

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Dealer Data"

class AuthorizedServiceCenter(base_models.AuthorizedServiceCenter):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='bajaj_registered_asc')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Service center Data"

class ServiceAdvisor(base_models.ServiceAdvisor):
    user = models.OneToOneField(UserProfile, primary_key=True,
                            related_name='bajaj_service_advisor')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)
    asc = models.ForeignKey(AuthorizedServiceCenter, null=True, blank=True)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Service Advisor Data"

class ServiceDeskUser(base_models.ServiceDeskUser):
    user = models.OneToOneField(UserProfile, null=True, blank=True, related_name='bajaj_service_desk_user')

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "service desk users"


class Feedback(base_models.Feedback):
    assign_to = models.ForeignKey(ServiceDeskUser, null=True, blank=True)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "user feedback info"


class Comments(base_models.Comments):
    feedback_object = models.ForeignKey(Feedback, null=False, blank=False)
    
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "user comment info"


class ProductTypeData(base_models.ProductTypeData):

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Product Type"


class ProductData(base_models.ProductData):
    customer_phone_number = models.ForeignKey(
        GladmindsUser, null=True, blank=True, related_name='bajaj_product_date')
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Product Data"


class CouponData(base_models.CouponData):
    vin = models.ForeignKey(ProductData, null=False, editable=False)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=True, blank=True)
    servicing_dealer = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Coupon Information"


class ServiceAdvisorCouponRelationship(base_models.ServiceAdvisorCouponRelationship):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor_phone = models.ForeignKey(ServiceAdvisor, null=False)
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = 'Service Advisor And Coupon Relationship'

class UCNRecovery(base_models.UCNRecovery):
    user = models.ForeignKey(UserProfile, related_name='bajaj_ucn_recovery')

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "UCN recovery logs"

class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='bajaj_otp_token')
    
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "OTPs"


class MessageTemplate(base_models.MessageTemplate):
    
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Message Template"

class EmailTemplate(base_models.EmailTemplate):

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Email Template"

class ASCTempRegistration(base_models.ASCTempRegistration):

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "ASC Save Form"

class SATempRegistration(base_models.SATempRegistration):

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "SA Save Form"


class CustomerTempRegistration(base_models.CustomerTempRegistration):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)
    
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Customer temporary info"


class ProductInsuranceInfo(base_models.ProductInsuranceInfo):
    product = models.ForeignKey(ProductData, null=False)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "product insurance info"


class ProductWarrantyInfo(base_models.ProductWarrantyInfo):
    product = models.ForeignKey(ProductData, null=False)

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "product warranty info"


class SparesData(base_models.SparesData):

    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "spare info"

