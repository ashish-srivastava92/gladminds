from gladminds.core import base_models
from django.db import models
from gladminds.gm.models import GladmindsUser
from django.contrib.auth.models import User


class UserProfile(base_models.UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='demo_users')

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Brand User"

class Dealer(base_models.Dealer):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Dealer Data"
    
class AuthorizedServiceCenter(base_models.AuthorizedServiceCenter):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Service center Data"


class ServiceAdvisor(base_models.ServiceAdvisor):
    user = models.OneToOneField(UserProfile, primary_key=True,
                            related_name='bajaj_service_advisor')    
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)
    asc_id = models.ForeignKey(RegisteredASC, null=True, blank=True)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Service Advisor Data"

class ServiceDeskUser(base_models.ServiceDeskUser):
    user = models.OneToOneField(UserProfile, null=True, blank=True, related_name='demo_service_desk_user')
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "service desk users"
        

class Feedback(base_models.Feedback):
    assign_to = models.ForeignKey(ServiceDeskUser, null=True, blank= True)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "user feedback info"


class Comments(base_models.Comments):
    feedback_object = models.ForeignKey(Feedback, null=False, blank=False)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "user comment info"    
        
class BrandData(base_models.BrandData):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Brand Data"


class ProductTypeData(base_models.ProductTypeData):
    brand_id = models.ForeignKey(BrandData, null=False, related_name='demo_product_type_date')
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Product Type"

class ProductData(base_models.ProductData):
    customer_phone_number = models.ForeignKey(
        GladmindsUser, null=True, blank=True, related_name='demo_product_date')
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Product Data"
    
        
class CouponData(base_models.CouponData):
    vin = models.ForeignKey(ProductData, null=False, editable=False)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=True, blank=True)
    servicing_dealer = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Coupon Information"


class ServiceAdvisorCouponRelationship(base_models.ServiceAdvisorCouponRelationship):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor_phone = models.ForeignKey(ServiceAdvisor, null=False)
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = 'Service Advisor And Coupon Relationship'

class UCNRecovery(base_models.UCNRecovery):
    user = models.ForeignKey(UserProfile, related_name='demo_ucn_recovery')
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "UCN recovery logs"

class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='demo_otp_token')
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "OTPs"

class MessageTemplate(base_models.MessageTemplate):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Message Template"


class EmailTemplate(base_models.EmailTemplate):

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Email Template"


class ASCTempRegistration(base_models.ASCTempRegistration):

    class Meta:
        app_label = "demo"
        verbose_name_plural = "ASC Save Form"

class SATempRegistration(base_models.SATempRegistration):

    class Meta:
        app_label = "demo"
        verbose_name_plural = "SA Save Form"


class CustomerTempRegistration(base_models.CustomerTempRegistration):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Customer temporary info"


class ProductInsuranceInfo(base_models.ProductInsuranceInfo):
    product = models.ForeignKey(ProductData, null=False)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "product insurance info"


class ProductWarrantyInfo(base_models.ProductWarrantyInfo):
    product = models.ForeignKey(ProductData, null=False)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "product warranty info"


class SparesData(base_models.SparesData):
    spare_brand = models.ForeignKey(BrandData, null=False)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "spare info"

