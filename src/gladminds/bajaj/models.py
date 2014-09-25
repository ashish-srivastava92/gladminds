from gladminds.core import models as base_models


class ASCSaveForm(base_models.ASCSaveForm):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "ASC Save Form"

class UCNRecovery(base_models.UCNRecovery):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "UCN recovery logs"

class RegisteredDealer(base_models.RegisteredDealer):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Dealer Data"

class ServiceAdvisor(base_models.ServiceAdvisor):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Service Advisor Data"

class ServiceAdvisorDealerRelationship(base_models.ServiceAdvisorDealerRelationship):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Service Advisor And Dealer Relationship"

class RegisteredASC(base_models.RegisteredASC):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Registered ASC Form"
    
class ServiceDeskUser(base_models.ServiceDeskUser):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "service desk users"

class Feedback(base_models.Feedback):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "user feedback info"

class Comments(base_models.Comments):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "user comment info"

class UploadProductCSV(base_models.UploadProductCSV):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Upload Product Data"
        
class BrandData(base_models.BrandData):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Brand Data"

class ProductTypeData(base_models.ProductTypeData):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Product Type"
    
class ProductData(base_models.ProductData):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Product Data"
        
class CouponData(base_models.CouponData):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Coupon Information"

class ServiceAdvisorCouponRelationship(base_models.ServiceAdvisorCouponRelationship):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = 'Service Advisor And Coupon Relationship'

class MessageTemplate(base_models.MessageTemplate):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Message Template"

class OTPToken(base_models.OTPToken):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "OTPs"

class EmailTemplate(base_models.EmailTemplate):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Email Template"

class SASaveForm(base_models.SASaveForm):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "SA Save Form"

class CustomerTempRegistration(base_models.CustomerTempRegistration):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "Customer temporary info"

class ProductInsuranceInfo(base_models.ProductInsuranceInfo):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "product insurance info"

class ProductWarrantyInfo(base_models.ProductWarrantyInfo):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "product warranty info"

class SparesData(base_models.SparesData):
    class Meta:
        app_label = "bajaj"
        verbose_name_plural = "spare info"
