from django.db import models
from django.contrib.auth.models import User
from gladminds.core import base_models
from gladminds.core.auth_helper import GmApps
from django.conf import settings
from gladminds.core.model_helpers import validate_image, validate_file

_APP_NAME = GmApps.BAJAJ


class BrandProductCategory(base_models.BrandProductCategory):
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Categories"


class UserProfile(base_models.UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='bajaj_users')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Users"


class Dealer(base_models.Dealer):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='bajaj_registered_dealer')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Dealer Data"

class ZonalServiceManager(base_models.ZonalServiceManager):
    '''details of Zonal Service Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    
    class Meta:
        app_label = _APP_NAME 


class AreaServiceManager(base_models.AreaServiceManager):
    '''details of Area Service Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    zsm = models.ForeignKey(ZonalServiceManager, null=True, blank=True)
    
    class Meta:
        app_label = _APP_NAME 


class AuthorizedServiceCenter(base_models.AuthorizedServiceCenter):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='bajaj_registered_asc')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)
    asm = models.ForeignKey(AreaServiceManager, null=True, blank=True)
    

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Service center Data"


class ServiceAdvisor(base_models.ServiceAdvisor):
    user = models.OneToOneField(UserProfile, primary_key=True,
                            related_name='bajaj_service_advisor')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)
    asc = models.ForeignKey(AuthorizedServiceCenter, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Service Advisor Data"


class ServiceDeskUser(base_models.ServiceDeskUser):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Service Desk Users"


class Feedback(base_models.Feedback):
    reporter = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='bajaj_feedback_reporter')
    assignee = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='bajaj_feedback_assignee')
    previous_assignee = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='bajaj_previous_assignee')
    
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user feedback"


class Activity(base_models.Activity):
    feedback = models.ForeignKey(Feedback, null=True, blank=True)
    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "user activity info"


class Comment(base_models.Comment):
    feedback_object = models.ForeignKey(Feedback,null=True, blank=True)

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
            BrandProductCategory, null=True, blank=True, related_name='bajaj_product_type')

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
    user = models.ForeignKey(UserProfile, related_name='bajaj_ucn_recovery')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "UCN recovery logs"


class OldFscData(base_models.OldFscData):
    product = models.ForeignKey(ProductData, null=True, blank=True)
    dealer = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Old Coupon Information"

class CDMSData(base_models.CDMSData):
    unique_service_coupon = models.ForeignKey(CouponData, null=True, editable=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "CDMS Information"

class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='bajaj_otp_token')

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


class FeedFailureLog(base_models.FeedFailureLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Feed Failure Log"


class VinSyncFeedLog(base_models.VinSyncFeedLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Vin Sycn Feed"


class AuditLog(base_models.AuditLog):
    user = models.ForeignKey(UserProfile)

    class Meta:
        app_label = _APP_NAME


class SLA(base_models.SLA):

    class Meta:
        app_label = _APP_NAME

class ServiceType(base_models.ServiceType):
    class Meta:
        app_label = _APP_NAME
    

class Service(base_models.Service):
    service_type = models.ForeignKey(ServiceType)
    training_material_url = models.FileField(upload_to='{0}/bajaj/training_material'.format(settings.ENV),
                                  max_length=255, null=True, blank=True,
                                  validators=[validate_file])

    class Meta:
        app_label = _APP_NAME


class Constant(base_models.Constant):
    ''' contains all the constants'''
    class Meta:
        app_label = _APP_NAME
        
        
class NationalSalesManager(base_models.NationalSalesManager):
    '''details of National Sales Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME


class AreaSalesManager(base_models.AreaSalesManager):
    '''details of Area Service Manager'''
    '''details of National Sales Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    nsm = models.ForeignKey(NationalSalesManager, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME


class Distributor(base_models.Distributor):
    '''details of Distributor'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    asm = models.ForeignKey(AreaSalesManager, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME


class Retailer(base_models.Retailer):
    '''details of retailer'''

    class Meta:
        app_label = _APP_NAME


class Mechanic(base_models.Mechanic):
    '''details of Mechanic'''
    registered_by_distributor = models.ForeignKey(Distributor, null=True, blank=True)
    preferred_retailer = models.ForeignKey(Retailer, null=True, blank=True)
    image_url = models.FileField(upload_to='{0}/bajaj/mechanics'.format(settings.ENV),
                                  max_length=255, null=True, blank=True,
                                  validators=[validate_image])

    class Meta:
        app_label = _APP_NAME

class SparePartMasterData(base_models.SparePartMasterData):
    '''details of Spare Part'''
    product_type = models.ForeignKey(ProductType, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME


class SparePartUPC(base_models.SparePartUPC):
    '''details of Spare Part'''
    part_number = models.ForeignKey(SparePartMasterData)

    class Meta:
        app_label = _APP_NAME

class SparePartPoint(base_models.SparePartPoint):
    '''details of Spare Part'''
    part_number = models.ForeignKey(SparePartMasterData)

    class Meta:
        app_label = _APP_NAME


class AccumulationRequest(base_models.AccumulationRequest):
    '''details of Spare Part'''

    member = models.ForeignKey(Mechanic)
    upcs = models.ManyToManyField(SparePartUPC)
    asm = models.ForeignKey(AreaSalesManager, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME

class Partner(base_models.Partner):
    '''details of partner'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME

class ProductCatalog(base_models.ProductCatalog):
    '''details of retailer'''
    partner = models.ForeignKey(Partner, null=True, blank=True)
    image_url = models.FileField(upload_to='{0}/bajaj/redeem_products'.format(settings.ENV),
                                  max_length=255, null=True, blank=True,
                                  validators=[validate_image])

    class Meta:
        app_label = _APP_NAME

class RedemptionRequest(base_models.RedemptionRequest):
    '''details of redemption request'''
    product = models.ForeignKey(ProductCatalog)
    member = models.ForeignKey(Mechanic)
    partner = models.ForeignKey(Partner, null=True, blank=True)
    image_url = models.FileField(upload_to='{0}/bajaj/proof_delivery'.format(settings.ENV),
                              max_length=255, null=True, blank=True,
                              validators=[validate_image])

    class Meta:
        app_label = _APP_NAME

class WelcomeKit(base_models.WelcomeKit):
    '''details of welcome kit'''
    member = models.ForeignKey(Mechanic)
    partner = models.ForeignKey(Partner, null=True, blank=True)
    image_url = models.FileField(upload_to='{0}/bajaj/proof_delivery'.format(settings.ENV),
                              max_length=255, null=True, blank=True,
                              validators=[validate_image])

    class Meta:
        app_label = _APP_NAME

class DateDimension(base_models.DateDimension):
    '''
    Date dimension table
    '''
    class Meta:
        app_label = _APP_NAME


class CouponFact(base_models.CouponFact):
    '''Coupon Fact Table for reporting'''
    date = models.ForeignKey(DateDimension)

    class Meta:
        app_label = _APP_NAME
        unique_together = ("date", "data_type")
        
class LoyaltySLA(base_models.LoyaltySLA):

    class Meta:
        app_label = _APP_NAME
        unique_together = ("status", "action")
