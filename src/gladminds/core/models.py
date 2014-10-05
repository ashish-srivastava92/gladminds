from gladminds.core.base_models import *



class ASCSaveForm(ASCSaveForm):
    pass

class UCNRecovery(UCNRecovery):
    pass

class RegisteredDealer(ServiceAdvisor):
    pass

class ServiceAdvisor(ServiceAdvisor):
    pass


##################################################################
#############Service Advisor and Registered Relationship MODEL####


class ServiceAdvisorDealerRelationship(models.Model):
    dealer_id = models.ForeignKey(RegisteredDealer, null=False)
    service_advisor_id = models.ForeignKey(ServiceAdvisor, null=False)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "Service Advisor And Dealer Relationship"


# class RegisteredASC(RegisteredASC):
#     pass
    
class Feedback(models.Model):
    reporter = models.CharField(max_length=15)
    reporter_email_id = models.CharField(max_length=50, null=True, blank= True)
    assign_to = models.ForeignKey(ServiceDeskUser, null=True, blank= True)
    message = models.CharField(max_length=512, null=True, blank=False)
    status = models.CharField(max_length=12, choices=FEEDBACK_STATUS)
    priority = models.CharField(max_length=12, choices=PRIORITY)
    type = models.CharField(max_length=12, choices=FEEDBACK_TYPE)
    subject = models.CharField(max_length=512, null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank= False)
    modified_date = models.DateTimeField(null=True, blank= True,auto_now=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    pending_from = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    wait_time = models.FloatField(max_length=20, null=True, blank=True, default = '0.0')
    remarks = models.CharField(max_length=512, null=True, blank=True)
    ratings = models.CharField(max_length=12, choices=RATINGS)
    root_cause = models.CharField(max_length=512, null=True, blank=True)
    resolution = models.CharField(max_length=512, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "aftersell feedback info"
        

class ServiceDeskUser(ServiceDeskUser):
    pass

        
class Comments(models.Model):
    feedback_object = models.ForeignKey(Feedback, null=False, blank=False, related_name='feedbcak_object')
    user = models.CharField(max_length=20, null=False, blank=False)
    comments_str = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(null=False, blank=False)
    modified_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    isDeleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        verbose_name_plural = "aftersell comment info"    
    


class UploadProductCSV(UploadProductCSV):
    pass

class BrandData(BrandData):
    pass


class ProductTypeData(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    brand_id = models.ForeignKey(BrandData, null=False)
    product_name = models.CharField(max_length=255, null=False)
    product_type = models.CharField(max_length=255, unique=True, null=False)
    product_image_loc = models.FileField(
        upload_to=settings.AFTERBUY_PRODUCT_TYPE_LOC, blank=True)
    isActive = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    warranty_email = models.EmailField(max_length=215, null=True, blank=True)
    warranty_phone = models.CharField(
        max_length=15, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Product Type"

    def __unicode__(self):
        return self.product_type
    
class ProductData(models.Model):
    id = models.AutoField(primary_key=True)
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    customer_phone_number = models.ForeignKey(
        GladMindUsers, null=True, blank=True)
    product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    sap_customer_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)

    # Added below column for after buy application
    customer_product_number = models.CharField(
        max_length=255, null=True, blank=True)
    purchased_from = models.CharField(max_length=255, null=True, blank=True)
    seller_email = models.EmailField(max_length=255, null=True, blank=True)
    seller_phone = models.CharField(max_length=255, null=True, blank=True)
    warranty_yrs = models.FloatField(null=True, blank=True)
    insurance_yrs = models.FloatField(null=True, blank=True)

    invoice_loc = models.FileField(upload_to="invoice", blank=True)
    warranty_loc = models.FileField(upload_to="warrenty", blank=True)
    insurance_loc = models.FileField(upload_to="insurance", blank=True)

    last_modified = models.DateTimeField(null=False, default=datetime.now())
    created_on = models.DateTimeField(null=True, default=datetime.now())
    isActive = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    veh_reg_no = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Data"

    def __unicode__(self):
        return self.vin

STATUS_CHOICES = ((1, 'Unused'), (2, 'Closed'), (
    3, 'Expired'), (4, 'In Progress'), (5, 'Exceeds Limit'))

    

class CouponData(models.Model):
    vin = models.ForeignKey(ProductData, null=False, editable=False)
    unique_service_coupon = models.CharField(
        max_length=215, unique=True, null=False)
    valid_days = models.IntegerField(max_length=10, null=False)
    valid_kms = models.IntegerField(max_length=10, null=False)
    service_type = models.IntegerField(max_length=10, null=False)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, db_index=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    mark_expired_on = models.DateTimeField(null=True, blank=True)
    actual_service_date = models.DateTimeField(null=True, blank=True)
    actual_kms = models.CharField(max_length=10, null=True, blank=True)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    schedule_reminder_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    extended_date = models.DateTimeField(null=True, blank=True)
    servicing_dealer = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Coupon Information"

    def __unicode__(self):
        return self.unique_service_coupon

##################################################################
#############Service Advisor and Coupon Relationship MODEL########


class ServiceAdvisorCouponRelationship(models.Model):
    unique_service_coupon = models.ForeignKey(CouponData, null=False)
    service_advisor_phone = models.ForeignKey(ServiceAdvisor, null=False)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = 'Service Advisor And Coupon Relationship'



class MessageTemplate(MessageTemplate):
    pass

class OTPToken(OTPToken):
    pass

class EmailTemplate(EmailTemplate):
    pass

class SASaveForm(SASaveForm):
    pass

class CustomerTempRegistration(models.Model):
    product_data = models.ForeignKey(ProductData, null=True, blank=True)
    new_customer_name = models.CharField(max_length=50, null=True, blank=True)
    new_number = models.CharField(max_length=15)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    temp_customer_id = models.CharField(max_length=50, null=False, blank=False, unique=True)
    sent_to_sap = models.BooleanField(default=False)
    remarks = models.CharField(max_length=500, null=True, blank=True)
    tagged_sap_id = models.CharField(
        max_length=215, null=True, blank=True, unique=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Customer temporary info"

    def __unicode__(self):
        return self.new_customer_name

######################################################################################

class ProductInsuranceInfo(models.Model):
    product = models.ForeignKey(ProductData, null=False)
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    insurance_brand_id = models.CharField(max_length=15, null=True, blank=True)
    insurance_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    insurance_email = models.EmailField(max_length=215, null=True, blank=True)
    insurance_phone = models.CharField(
        max_length=15, blank=False, null=False)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "product insurance info"
    
#######################################################################################

class ProductWarrantyInfo(models.Model):
    product = models.ForeignKey(ProductData, null=False)
    issue_date = models.DateTimeField(null=True, blank=False)
    expiry_date = models.DateTimeField(null=True, blank= False)
    warranty_brand_id = models.CharField(max_length=15, null=True, blank=True)
    warranty_brand_name = models.CharField(max_length=50, null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "product warranty info"
        
########################################################################################

class SparesData(models.Model):
    spare_brand = models.ForeignKey(BrandData, null=False, related_name='+')
    spare_name = models.CharField(max_length=50, null=True, blank=True)
    spare_contact = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        abstract = True
        verbose_name_plural = "spares data"
    
#########################################################################################

# from gladminds.core.models import *