from gladminds.core.base_models import *
from gladminds.gm.models import UserProfile, GladMindUsers



class ASCSaveForm(ASCSaveForm):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "ASC Save Form"


class UCNRecovery(UCNRecovery):
    user_id = models.ForeignKey(UserProfile, related_name='core_ucn_recovery')
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "UCN recovery logs"


class RegisteredDealer(RegisteredDealer):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Dealer Data"


class ServiceAdvisor(ServiceAdvisor):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Service Advisor Data"


class ServiceAdvisorDealerRelationship(ServiceAdvisorDealerRelationship):
    dealer_id = models.ForeignKey(RegisteredDealer, null=False)
    service_advisor_id = models.ForeignKey(ServiceAdvisor, null=False)
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Service Advisor And Dealer Relationship"


# class RegisteredASC(RegisteredASC):
#     pass
    
    
class ServiceDeskUser(ServiceDeskUser):
    user = models.OneToOneField(UserProfile, null=True, blank=True, related_name='core_service_desk_user')
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "service desk users"


class Feedback(Feedback):
    assign_to = models.ForeignKey(ServiceDeskUser, null=True, blank= True)
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "user feedback info"
        
        
class Comments(Comments):
    feedback_object = models.ForeignKey(Feedback, null=False, blank=False)
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "user comment info"    
    

class UploadProductCSV(UploadProductCSV):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Upload Product Data"


class BrandData(BrandData):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Brand Data"


class ProductTypeData(ProductTypeData):
    brand_id = models.ForeignKey(BrandData, null=False, related_name='core_product_type_date')
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Product Type"
    
    
class ProductData(ProductData):
    customer_phone_number = models.ForeignKey(
        GladMindUsers, null=True, blank=True, related_name='core_product_date')
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        app_label = "core"
        verbose_name_plural = "Product Data"


class CouponData(CouponData):
    vin = models.ForeignKey(ProductData, null=False, editable=False)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=True, blank=True)
    servicing_dealer = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        app_label = "core"
        verbose_name_plural = "Coupon Information"


##################################################################
#############Service Advisor and Coupon Relationship MODEL########


class ServiceAdvisorCouponRelationship(ServiceAdvisorCouponRelationship):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor_phone = models.ForeignKey(ServiceAdvisor, null=False)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        app_label = "core"
        verbose_name_plural = 'Service Advisor And Coupon Relationship'


class MessageTemplate(MessageTemplate):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Message Template"


class OTPToken(OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='core_otp_token')
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "OTPs"


class EmailTemplate(EmailTemplate):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "Email Template"


class SASaveForm(SASaveForm):
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "SA Save Form"


class CustomerTempRegistration(CustomerTempRegistration):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)

    class Meta:
        app_label = "core"
        verbose_name_plural = "Customer temporary info"

######################################################################################

class ProductInsuranceInfo(ProductInsuranceInfo):
    product = models.ForeignKey(ProductData, null=False)

    class Meta:
        app_label = "core"
        verbose_name_plural = "product insurance info"
    
#######################################################################################

class ProductWarrantyInfo(ProductWarrantyInfo):
    product = models.ForeignKey(ProductData, null=False)

    class Meta:
        app_label = "core"
        verbose_name_plural = "product warranty info"
        
########################################################################################

class SparesData(SparesData):
    spare_brand = models.ForeignKey(BrandData, null=False)
    
    class Meta:
        app_label = "core"
        verbose_name_plural = "spares data"
    
#########################################################################################

# from gladminds.core.models import *