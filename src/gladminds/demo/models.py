from gladminds.core import base_models
from django.db import models
from gladminds.gm.models import UserProfile, GladMindUsers


class ASCSaveForm(base_models.ASCSaveForm):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "ASC Save Form"


class UCNRecovery(base_models.UCNRecovery):
    user = models.ForeignKey(UserProfile, related_name='demo_ucn_recovery')
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "UCN recovery logs"


class RegisteredDealer(base_models.RegisteredDealer):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Dealer Data"


class ServiceAdvisor(base_models.ServiceAdvisor):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Service Advisor Data"


class ServiceAdvisorDealerRelationship(base_models.ServiceAdvisorDealerRelationship):
    dealer_id = models.ForeignKey(RegisteredDealer, null=False)
    service_advisor_id = models.ForeignKey(ServiceAdvisor, null=False)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Service Advisor And Dealer Relationship"


# class RegisteredASC(base_models.RegisteredASC):
#     class Meta:
#         app_label = "demo"
#         verbose_name_plural = "Registered ASC Form"

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


class UploadProductCSV(base_models.UploadProductCSV):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Upload Product Data"
    
        
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
        GladMindUsers, null=True, blank=True, related_name='demo_product_date')
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Product Data"
    
        
class CouponData(base_models.CouponData):
    vin = models.ForeignKey(ProductData, null=False, editable=False)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=True, blank=True)
    servicing_dealer = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Coupon Information"


class ServiceAdvisorCouponRelationship(base_models.ServiceAdvisorCouponRelationship):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor_phone = models.ForeignKey(ServiceAdvisor, null=False)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = 'Service Advisor And Coupon Relationship'


class MessageTemplate(base_models.MessageTemplate):
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "Message Template"


class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='demo_otp_token')
    
    class Meta:
        app_label = "demo"
        verbose_name_plural = "OTPs"


class EmailTemplate(base_models.EmailTemplate):

    class Meta:
        app_label = "demo"
        verbose_name_plural = "Email Template"


class SASaveForm(base_models.SASaveForm):

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

