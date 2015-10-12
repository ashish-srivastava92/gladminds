from django.db import models
from django.contrib.auth.models import User
from gladminds.core import base_models, constants
 
_APP_NAME ='core'
 
 
class BrandProductCategory(base_models.BrandProductCategory):
    class Meta(base_models.BrandProductCategory.Meta):
        app_label = _APP_NAME


class UserProfile(base_models.UserProfile):
    user = models.OneToOneField(User, primary_key=True,
                                        related_name='core_users')
    
    class Meta(base_models.UserProfile.Meta):
        app_label = _APP_NAME

class ZonalServiceManager(base_models.ZonalServiceManager):
    '''details of Zonal Service Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    
    class Meta(base_models.ZonalServiceManager.Meta):
        app_label = _APP_NAME 


class AreaServiceManager(base_models.AreaServiceManager):
    '''details of Area Service Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    zsm = models.ForeignKey(ZonalServiceManager, null=True, blank=True)
    
    class Meta(base_models.AreaServiceManager.Meta):
        app_label = _APP_NAME 
        
class CircleHead(base_models.CircleHead):
    '''details of Circle Heads'''
    user =  models.OneToOneField(UserProfile)
    
    class Meta(base_models.CircleHead.Meta):
        app_label = _APP_NAME
        
class RegionalManager(base_models.RegionalManager):
    '''details of Regional Manager'''
    user =  models.OneToOneField(UserProfile)
    circle_head = models.ForeignKey(CircleHead, null=True, blank=True)

    class Meta(base_models.RegionalManager.Meta):
        app_label = _APP_NAME
        
class Territory(base_models.Territory):
    '''List of territories'''
    
    class Meta(base_models.Territory.Meta):
        app_label = _APP_NAME

class State(base_models.State):
    ''' List of states mapped to territory'''
    territory = models.ForeignKey(Territory, null=True, blank=True)
 
    class Meta(base_models.State.Meta):
        app_label = _APP_NAME
        
class Dealer(base_models.Dealer):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='core_registered_dealer')
    asm = models.ForeignKey(AreaServiceManager, null=True, blank=True)
    

    class Meta(base_models.Dealer.Meta):
        app_label = _APP_NAME

class AuthorizedServiceCenter(base_models.AuthorizedServiceCenter):
    user = models.OneToOneField(UserProfile, primary_key=True,
                                related_name='core_registered_asc')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)
    asm = models.ForeignKey(AreaServiceManager, null=True, blank=True)
    

    class Meta(base_models.AuthorizedServiceCenter.Meta):
        app_label = _APP_NAME


class ServiceAdvisor(base_models.ServiceAdvisor):
    user = models.OneToOneField(UserProfile, primary_key=True,
                            related_name='core_service_advisor')
    dealer = models.ForeignKey(Dealer, null=True, blank=True)
    asc = models.ForeignKey(AuthorizedServiceCenter, null=True, blank=True)

    class Meta(base_models.ServiceAdvisor.Meta):
        app_label = _APP_NAME


class BrandDepartment(base_models.BrandDepartment):
    
    class Meta(base_models.BrandDepartment.Meta):
        app_label = _APP_NAME


class DepartmentSubCategories(base_models.DepartmentSubCategories):
    department = models.ForeignKey(BrandDepartment, related_name="department_sub_categories", null=True, blank=True)
    
    class Meta(base_models.DepartmentSubCategories.Meta):
        app_label = _APP_NAME


class ServiceDeskUser(base_models.ServiceDeskUser):
    user_profile = models.ForeignKey(UserProfile, null=True, blank=True)
    sub_department = models.ForeignKey(DepartmentSubCategories, related_name="sub_department_user", null=True, blank=True)
    
    class Meta(base_models.ServiceDeskUser.Meta):
        app_label = _APP_NAME


class Feedback(base_models.Feedback):
    priority = models.CharField(max_length=12, choices=constants.DEMO_PRIORITY, default='P3')
    reporter = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='core_feedback_reporter')
    assignee = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='core_feedback_assignee')
    previous_assignee = models.ForeignKey(ServiceDeskUser, null=True, blank=True, related_name='core_previous_assignee')
    sub_department = models.ForeignKey(DepartmentSubCategories,null=True, blank=True) 
    
    class Meta(base_models.Feedback.Meta):
        app_label = _APP_NAME


class Activity(base_models.Activity):
    feedback = models.ForeignKey(Feedback, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name="core_activity_users")
    
    class Meta(base_models.Activity.Meta):
        app_label = _APP_NAME


class Comment(base_models.Comment):
    feedback_object = models.ForeignKey(Feedback,null=True, blank=True)

    class Meta(base_models.Comment.Meta):
        app_label = _APP_NAME


class FeedbackEvent(base_models.FeedbackEvent):
    feedback = models.ForeignKey(Feedback, null=True, blank=True)
    user = models.ForeignKey(ServiceDeskUser, null=True, blank=True)
    activity = models.ForeignKey(Activity, null=True, blank=True)
     
    class Meta(base_models.FeedbackEvent.Meta):
        app_label = _APP_NAME


class ProductType(base_models.ProductType):
    brand_product_category = models.ForeignKey(
            BrandProductCategory, null=True, blank=True, related_name='core_product_type')

    class Meta(base_models.ProductType.Meta):
        app_label = _APP_NAME


class ProductData(base_models.ProductData):
    product_type = models.ForeignKey(ProductType, null=True, blank=True)
    dealer_id = models.ForeignKey(Dealer, null=True, blank=True)

    class Meta(base_models.ProductData.Meta):
        app_label = _APP_NAME

# class DispatchedProduct(ProductData):
# 
#     class Meta:
#         proxy = True

class CouponData(base_models.CouponData):
    product = models.ForeignKey(ProductData, null=False, editable=False)
    service_advisor = models.ForeignKey(ServiceAdvisor, null=True, blank=True)

    class Meta(base_models.CouponData.Meta):
        app_label = _APP_NAME


class ServiceAdvisorCouponRelationship(base_models.ServiceAdvisorCouponRelationship):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor = models.ForeignKey(ServiceAdvisor, null=False)

    class Meta(base_models.ServiceAdvisorCouponRelationship.Meta):
        app_label = _APP_NAME


class UCNRecovery(base_models.UCNRecovery):
    user = models.ForeignKey(UserProfile, related_name='core_ucn_recovery')

    class Meta(base_models.UCNRecovery.Meta):
        app_label = _APP_NAME


class OldFscData(base_models.OldFscData):
    product = models.ForeignKey(ProductData, null=True, blank=True)

    class Meta(base_models.OldFscData.Meta):
        app_label = _APP_NAME

class CDMSData(base_models.CDMSData):
    unique_service_coupon = models.ForeignKey(CouponData, null=True, editable=False)

    class Meta(base_models.CDMSData.Meta):
        app_label = _APP_NAME

class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(UserProfile, null=True, blank=True, related_name='core_otp_token')

    class Meta(base_models.OTPToken.Meta):
        app_label = _APP_NAME


class MessageTemplate(base_models.MessageTemplate):

    class Meta(base_models.MessageTemplate.Meta):
        app_label = _APP_NAME


class EmailTemplate(base_models.EmailTemplate):

    class Meta(base_models.EmailTemplate.Meta):
        app_label = _APP_NAME


class ASCTempRegistration(base_models.ASCTempRegistration):

    class Meta(base_models.ASCTempRegistration.Meta):
        app_label = _APP_NAME


class SATempRegistration(base_models.SATempRegistration):

    class Meta(base_models.SATempRegistration.Meta):
        app_label = _APP_NAME


class CustomerTempRegistration(base_models.CustomerTempRegistration):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)

    class Meta(base_models.CustomerTempRegistration.Meta):
        app_label = _APP_NAME

class CustomerUpdateFailure(base_models.CustomerUpdateFailure):
    '''stores data when phone number update exceeds the limit'''
    product_id = models.ForeignKey(ProductData, null=False, blank=False)
    
    class Meta(base_models.CustomerUpdateFailure.Meta):
        app_label = _APP_NAME
        
class CustomerUpdateHistory(base_models.CustomerUpdateHistory):
    '''Stores the updated values of registered customer'''
    temp_customer = models.ForeignKey(CustomerTempRegistration)

    class Meta(base_models.CustomerUpdateHistory.Meta):
        app_label = _APP_NAME


class UserPreference(base_models.UserPreference):
    user = models.ForeignKey(UserProfile)

    class Meta(base_models.UserPreference.Meta):
        app_label = _APP_NAME
        unique_together = ("user", "key")


class SMSLog(base_models.SMSLog):

    class Meta(base_models.SMSLog.Meta):
        app_label = _APP_NAME


class EmailLog(base_models.EmailLog):

    class Meta(base_models.EmailLog.Meta):
        app_label = _APP_NAME


class DataFeedLog(base_models.DataFeedLog):

    class Meta(base_models.DataFeedLog.Meta):
        app_label = _APP_NAME


class FeedFailureLog(base_models.FeedFailureLog):

    class Meta(base_models.FeedFailureLog.Meta):
        app_label = _APP_NAME


class VinSyncFeedLog(base_models.VinSyncFeedLog):

    class Meta(base_models.VinSyncFeedLog.Meta):
        app_label = _APP_NAME


class AuditLog(base_models.AuditLog):
    user = models.ForeignKey(UserProfile)

    class Meta(base_models.AuditLog.Meta):
        app_label = _APP_NAME


class SLA(base_models.SLA):
    priority = models.CharField(max_length=12, choices=constants.DEMO_PRIORITY, unique=True)
    
    class Meta(base_models.SLA.Meta):
        app_label = _APP_NAME

class ServiceType(base_models.ServiceType):
    
    class Meta(base_models.ServiceType.Meta):
        app_label = _APP_NAME
    

class Service(base_models.Service):
    service_type = models.ForeignKey(ServiceType)

    class Meta(base_models.Service.Meta):
        app_label = _APP_NAME


class Constant(base_models.Constant):
    ''' contains all the constants'''
    
    class Meta(base_models.Constant.Meta):
        app_label = _APP_NAME
        
class DateDimension(base_models.DateDimension):
    '''
    Date dimension table
    '''
    class Meta(base_models.DateDimension.Meta):
        app_label = _APP_NAME


class CouponFact(base_models.CouponFact):
    '''Coupon Fact Table for reporting'''
    date = models.ForeignKey(DateDimension)

    class Meta(base_models.CouponFact.Meta):
        app_label = _APP_NAME
        unique_together = ("date", "data_type")

############################### CTS MODELS ###################################################
class Transporter(base_models.Transporter):
    '''details of Transporter'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    
    class Meta(base_models.Transporter.Meta):
        app_label = _APP_NAME 


class Supervisor(base_models.Supervisor):
    '''details of Supervisor'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    transporter = models.ForeignKey(Transporter, null=True, blank=True)
    
    class Meta(base_models.Supervisor.Meta):
        app_label = _APP_NAME 

class ContainerIndent(base_models.ContainerIndent):
    ''' details of Container Indent'''

    class Meta(base_models.ContainerIndent.Meta):
        app_label = _APP_NAME

class ContainerLR(base_models.ContainerLR):
    ''' details of Container LR'''
    zib_indent_num = models.ForeignKey(ContainerIndent)
    transporter = models.ForeignKey(Transporter)

    class Meta(base_models.ContainerLR.Meta):
        app_label = _APP_NAME


class ContainerTracker(base_models.ContainerTracker):
    ''' details of Container Tracker'''
    transporter = models.ForeignKey(Transporter)

    class Meta(base_models.ContainerTracker.Meta):
        app_label = _APP_NAME

#######################LOYALTY MODELS#################################
class Territory(base_models.Territory):
    '''List of territories'''
    
    class Meta(base_models.Territory.Meta):
        app_label = _APP_NAME

class State(base_models.State):
    ''' List of states mapped to territory'''
    territory = models.ForeignKey(Territory, null=True, blank=True)
 
    class Meta(base_models.State.Meta):
        app_label = _APP_NAME

class City(base_models.City):
    ''' List of cities mapped to states'''
    state = models.ForeignKey(State, null=True, blank=True)    
   
    class Meta(base_models.City.Meta):
        app_label = _APP_NAME

class NationalSparesManager(base_models.NationalSparesManager):
    '''details of National Spares Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    territory = models.ManyToManyField(Territory)

    class Meta(base_models.NationalSparesManager.Meta):
        app_label = _APP_NAME
        
class NationalSalesManager(base_models.NationalSalesManager):
    '''details of National Sales Manager'''
    user = models.ForeignKey(UserProfile)
    territory = models.ManyToManyField(Territory)

    class Meta(base_models.NationalSalesManager.Meta):
        app_label = _APP_NAME
        
class AreaSalesManager(base_models.AreaSalesManager):
    '''details of Area Sales Manager'''
    user =  models.OneToOneField(UserProfile)
    #name = models.CharField(max_length=50, null=True, blank=True)
    #nsm = models.ForeignKey(NationalSalesManager, null=True, blank=True)
    state = models.ManyToManyField(State)
    
    class Meta(base_models.AreaSalesManager.Meta):
        app_label = _APP_NAME
    
    def __unicode__(self):
        return self.user.user.username
    rm = models.ForeignKey(RegionalManager, null=True, blank=True)
    state = models.ManyToManyField(State)
    
    class Meta(base_models.AreaSalesManager.Meta):
        app_label = _APP_NAME
    
    def __unicode__(self):
        return self.user.user.username

class AreaSparesManager(base_models.AreaSparesManager):
    '''details of Area Spares Manager'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    state = models.ManyToManyField(State)
    nsm = models.ForeignKey(NationalSparesManager, null=True, blank=True)

    class Meta(base_models.AreaSparesManager.Meta):
        app_label = _APP_NAME

class Distributor(base_models.Distributor):
    '''details of Distributor'''
    user = models.ForeignKey(UserProfile)
    territory = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15)
    profile = models.CharField(max_length=15)
    language = models.CharField(max_length=10, null=True, blank=True)
    territory = models.CharField(max_length=10, null=True, blank=True) 
    
    class Meta(base_models.Distributor.Meta):
        app_label = _APP_NAME

class DistributorStaff(base_models.DistributorStaff):
    '''details of Distributor Staff'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    distributor = models.ForeignKey(Distributor, null=True, blank=True)
    
    class Meta(base_models.DistributorStaff.Meta):
        app_label = _APP_NAME

class DistributorSalesRep(base_models.DistributorSalesRep):
    '''details of Distributor Sales Rep'''
    user = models.ForeignKey(UserProfile)
    distributor = models.ForeignKey(Distributor)
    
    class Meta(base_models.DistributorSalesRep.Meta):
        app_label = _APP_NAME
        
    def __unicode__(self):
        return self.distributor_sales_code + ' ' + self.user.user.first_name + \
                                ' ' + self.user.user.last_name

class Retailer(base_models.Retailer):
    '''details of retailer'''
    user = models.ForeignKey(UserProfile)
    billing_code = models.CharField(max_length=15)
    distributor = models.ForeignKey(Distributor)
    approved = models.PositiveSmallIntegerField(default=constants.STATUS['WAITING_FOR_APPROVAL'])
    territory = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=15)
    profile = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.DecimalField(max_digits = 10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits = 11, decimal_places=6, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)
    rejected_reason = models.CharField(max_length=300, null=True, blank=True)
    
    class Meta(base_models.Retailer.Meta):
        app_label = _APP_NAME

    def __unicode__(self):
        return self.retailer_code + ' ' + self.retailer_name
    
class RetailerCollection(base_models.RetailerCollection):
    '''details of retailer collection'''
    retailer = models.ForeignKey(Retailer)
    dsr = models.ForeignKey(DistributorSalesRep)
    order_amount = models.CharField(max_length = 20)
    collected_amount = models.CharField(max_length = 20)
    outstanding_amount = models.CharField(max_length = 20)
    
    class Meta(base_models.RetailerCollection.Meta):
        app_label = _APP_NAME

class DSRWorkAllocation(base_models.DSRWorkAllocation):
    '''details of DSR work allocation'''
    distributor = models.ForeignKey(Distributor)
    dsr = models.ForeignKey(DistributorSalesRep)
    retailer = models.ForeignKey(Retailer)
    date = models.DateTimeField(null = True, blank=True)
    
    class Meta(base_models.DSRWorkAllocation.Meta):
        app_label = _APP_NAME
        
class DSRScorecardReport(base_models.DSRScorecardReport):
    '''details of DSRScorecardReport'''
    serial_number = models.CharField(max_length = 5)
    goals = models.CharField(max_length = 255, null = True, blank = True)
    target = models.CharField(max_length = 255, null = True, blank = True)
    actual = models.CharField(max_length = 255,  null = True, blank = True)
    measures = models.CharField(max_length = 255, null = True, blank = True)
    weight = models.CharField(max_length = 255, null = True, blank = True)
    total_score = models.CharField(max_length = 255, null = True, blank = True)
    
    class Meta(base_models.DSRScorecardReport.Meta):
        app_label = _APP_NAME
        
class PartModels(base_models.PartModels):
    ''' details of parts models'''
    
    class Meta(base_models.PartModels.Meta):
        app_label = _APP_NAME
        
class Categories(base_models.Categories):
    ''' details of model categories'''
    
    class Meta(base_models.Categories.Meta):
        app_label = _APP_NAME
        
class SubCategories(base_models.SubCategories):
    ''' details of model sub categories'''
    
    class Meta(base_models.SubCategories.Meta):
        app_label = _APP_NAME
        
class CvCategories(base_models.CvCategories):
    ''' details of alternate parts and pricing '''
    name = models.CharField(max_length = 255)
    usps = models.TextField(null=True,blank=True)
    importance = models.TextField(null=True,blank=True)
    image_url = models.CharField(max_length = 255, null=True,blank=True)
    active = models.BooleanField(default = True)
    
    class Meta(base_models.CvCategories.Meta):
        app_label = _APP_NAME
        
class PartPricing(base_models.PartPricing):
    ''' details of parts models'''
    
    class Meta(base_models.PartPricing.Meta):
        app_label = _APP_NAME
        
class PartMasterCv(base_models.PartMasterCv):
    ''' details of spare parts and pricing '''
    bajaj_id = models.IntegerField()
    part_number = models.CharField(max_length = 255)
    description = models.TextField()
    part_model = models.TextField()
    valid_from = models.DateField()
    part_models = models.CharField(max_length = 255)
    category = models.ForeignKey(CvCategories)
    mrp = models.CharField(max_length = 255)
    active = models.BooleanField(default = True)
    
    class Meta(base_models.PartMasterCv.Meta):
        app_label = _APP_NAME
        
class OrderPart(base_models.OrderPart):
    ''' details of ordering spare parts by dsr or retailer'''
    order_id = models.CharField(max_length = 40)
    order_date = models.DateField()
    part = models.ForeignKey(PartMasterCv)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits = 5, decimal_places=2)
    line_total = models.DecimalField(max_digits = 8, decimal_places=2)
    total_amount = models.DecimalField(max_digits = 10, decimal_places=2)
    fullfill = models.NullBooleanField()
    delivered = models.IntegerField(null=True, blank=True)
    no_fullfill_reason = models.CharField(max_length=300, null=True, blank=True)
    dsr = models.ForeignKey(DistributorSalesRep, null = True, blank=True)
    accept = models.BooleanField(default = False)
    retailer = models.ForeignKey(Retailer)
    distributor = models.ForeignKey(Distributor)
    
    class Meta(base_models.OrderPart.Meta):
        app_label = _APP_NAME

class AlternateParts(base_models.AlternateParts):
    ''' details of alternate parts and pricing '''
    part_number = models.CharField(max_length = 255)
    part_name = models.CharField(max_length = 255)
    old_part_number = models.CharField(max_length = 255)
    model_name = models.CharField(max_length = 255)
    active = models.BooleanField(default = True)
    
    class Meta(base_models.AlternateParts.Meta):
        app_label = _APP_NAME
        
class Kit(base_models.Kit):
    ''' details of alternate parts and pricing '''
    part_number = models.CharField(max_length = 255)
    description = models.TextField()
    kit_applicability = models.TextField()
    mrp = models.CharField(max_length = 255)
    valid_from = models.CharField(max_length = 255)
    part_models = models.CharField(max_length = 255)
    active = models.BooleanField(default = True)
    
    class Meta(base_models.Kit.Meta):
        app_label = _APP_NAME
        
class Member(base_models.Member):
    '''details of Member'''
    registered_by_distributor = models.ForeignKey(Distributor, null=True, blank=True)
    preferred_retailer = models.ForeignKey(Retailer, null=True, blank=True)
    state = models.ForeignKey(State)


    class Meta(base_models.Member.Meta):
        app_label = _APP_NAME

class SparePartMasterData(base_models.SparePartMasterData):
    '''details of Spare Part'''
    product_type = models.ForeignKey(ProductType, null=True, blank=True)

    class Meta(base_models.SparePartMasterData.Meta):
        app_label = _APP_NAME


class SparePartUPC(base_models.SparePartUPC):
    '''details of Spare Part UPC'''
    part_number = models.ForeignKey(SparePartMasterData)

    class Meta(base_models.SparePartUPC.Meta):
        app_label = _APP_NAME

class SparePartPoint(base_models.SparePartPoint):
    '''details of Spare Part points'''
    part_number = models.ForeignKey(SparePartMasterData)

    class Meta(base_models.SparePartPoint.Meta):
        app_label = _APP_NAME
        unique_together = ('part_number', 'territory',)


class AccumulationRequest(base_models.AccumulationRequest):
    '''details of Accumulation request'''
    member = models.ForeignKey(Member)
    upcs = models.ManyToManyField(SparePartUPC)
    asm = models.ForeignKey(AreaSparesManager, null=True, blank=True)

    class Meta(base_models.AccumulationRequest.Meta):
        app_label = _APP_NAME

class Partner(base_models.Partner):
    '''details of RPs and LPs'''
    user = models.ForeignKey(UserProfile, null=True, blank=True)

    class Meta(base_models.Partner.Meta):
        app_label = _APP_NAME

class ProductCatalog(base_models.ProductCatalog):
    '''details of Product Catalog'''
    partner = models.ForeignKey(Partner, null=True, blank=True)

    class Meta(base_models.ProductCatalog.Meta):
        app_label = _APP_NAME

class RedemptionRequest(base_models.RedemptionRequest):
    '''details of Redemption Request'''
    product = models.ForeignKey(ProductCatalog)
    member = models.ForeignKey(Member)
    partner = models.ForeignKey(Partner, null=True, blank=True)

    class Meta(base_models.RedemptionRequest.Meta):
        app_label = _APP_NAME

class WelcomeKit(base_models.WelcomeKit):
    '''details of welcome kit'''
    member = models.ForeignKey(Member)
    partner = models.ForeignKey(Partner, null=True, blank=True)

    class Meta(base_models.WelcomeKit.Meta):
        app_label = _APP_NAME

class CommentThread(base_models.CommentThread):
    '''details of activities done by service-desk user'''
    welcome_kit = models.ForeignKey(WelcomeKit, null=True, blank=True)
    redemption = models.ForeignKey(RedemptionRequest, null=True, blank=True)
    user = models.ForeignKey(User, related_name="core_comments_user")

    class Meta(base_models.CommentThread.Meta):
        app_label = _APP_NAME
        
class LoyaltySLA(base_models.LoyaltySLA):

    class Meta(base_models.LoyaltySLA.Meta):
        app_label = _APP_NAME
        unique_together = ("status", "action")

class DiscrepantAccumulation(base_models.DiscrepantAccumulation):
    upc = models.ForeignKey(SparePartUPC)
    new_member = models.ForeignKey(Member)
    accumulation_request = models.ForeignKey(AccumulationRequest)
     
    class Meta(base_models.DiscrepantAccumulation.Meta):
        app_label = _APP_NAME

############################### ECO MODELS ###################################################      

class ECORelease(base_models.ECORelease):
    '''Details of ECO Release'''
    class Meta(base_models.ECORelease.Meta):
        app_label = _APP_NAME

class ECOImplementation(base_models.ECOImplementation):
    '''Details of ECO Implementation'''
    class Meta(base_models.ECOImplementation.Meta):
        app_label = _APP_NAME

class BrandVertical(base_models.BrandVertical):
    '''Stores the different vertical
    a brand can have'''
    class Meta(base_models.BrandVertical.Meta):
        app_label = _APP_NAME

class BrandProductRange(base_models.BrandProductRange):
    '''Different range of product a brand provides'''
    class Meta(base_models.BrandProductRange.Meta):
            app_label = _APP_NAME

class BOMHeader(base_models.BOMHeader):
    '''Details of Header BOM'''
    class Meta(base_models.BOMHeader.Meta):
            app_label = _APP_NAME
            
class BOMPlate(base_models.BOMPlate):
    '''Details of BOM Plates'''
    class Meta(base_models.BOMPlate.Meta):
        app_label = _APP_NAME
        
class BOMPart(base_models.BOMPart):
    '''Details of  BOM Parts'''
    class Meta(base_models.BOMPart.Meta):
            app_label = _APP_NAME
        
class BOMPlatePart(base_models.BOMPlatePart):
    '''Details of BOM Plates and part relation'''
    bom = models.ForeignKey(BOMHeader)
    plate = models.ForeignKey(BOMPlate)
    part = models.ForeignKey(BOMPart)

class Meta(base_models.BOMPlatePart.Meta):
            app_label = _APP_NAME

class BOMVisualization(base_models.BOMVisualization):
    '''Details of BOM Plates cordinates'''
    bom = models.ForeignKey(BOMPlatePart)
    
    class Meta(base_models.BOMVisualization.Meta):
            app_label = _APP_NAME
            
class ServiceCircular(base_models.ServiceCircular):
    '''Save the service circular created for a product'''
    model_sku_code = models.ManyToManyField(BrandProductRange)
    
    class Meta(base_models.ServiceCircular.Meta):
        app_label = _APP_NAME

class ManufacturingData(base_models.ManufacturingData):
    '''Manufacturing data of a product'''
    class Meta(base_models.ManufacturingData.Meta):
        app_label = _APP_NAME

