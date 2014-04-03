from django.db import models
from django.conf import settings
from django.contrib.auth.models import User 
from datetime import datetime
##################BRAND-PRPDUCT MODELS#######################
'''
BrandData contains brand related information
'''


class UploadProductCSV(models.Model):
    file_location=settings.PROJECT_DIR+'/data/'
    upload_brand_feed= models.FileField(upload_to=file_location, blank=True)
    upload_dealer_feed=models.FileField(upload_to=file_location, blank=True)
    upload_product_dispatch_feed= models.FileField(upload_to=file_location, blank=True)
    upload_product_purchase_feed= models.FileField(upload_to=file_location, blank=True)
    upload_coupon_redeem_feed= models.FileField(upload_to=file_location, blank=True)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Upload Product Data"

class BrandData(models.Model):
    pk_brand_id=models.AutoField(primary_key=True)
    brand_id=models.CharField(max_length=50, null=False,unique=True, help_text="Brand Id must be unique")
    brand_name=models.CharField(max_length=250, null=False)
    brand_image_loc = models.FileField(upload_to=settings.AFTERBUY_BRAND_LOC, blank=True)
    isActive = models.BooleanField(default=True)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Brand Data"

    def __unicode__(self):
        return self.brand_id
    
    def image_tag(self):
        if self.brand_name =='Bajaj':
            url=settings.STATIC_URL+'img/bajaj.jpg'
            return u'<img src= '+url+' style="max-width: 37%;max-height: 15%" />'
        elif self.brand_name=='Honda':
            url=settings.STATIC_URL+'img/honda.jpg'
            return u'<img src= '+url+' style="max-width: 37%;max-height: 15%" />'
        else:
            url=settings.STATIC_URL+'img/noimage.jpg'
            return u'<img src= '+url+' style="max-width: 37%;max-height: 15%" />'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    
'''
ProductTypeData  is linked to Brand data
For 1 Brand there can be multiple Products
'''
    
class ProductTypeData(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    brand_id=models.ForeignKey(BrandData ,null=False)
    product_name=models.CharField(max_length=255, null=False)
    product_type=models.CharField(max_length=255,unique=True, null=False)
    product_image_loc = models.FileField(upload_to=settings.AFTERBUY_PRODUCT_TYPE_LOC, blank=True)
    isActive = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Product Type"
        
    def __unicode__(self):
        return self.product_type
        
###################################################################

######################DEALER-SA MODELS#############################    


class RegisteredDealer(models.Model):
    dealer_id = models.CharField(max_length=25, blank=False, null=False, unique=True, help_text="Dealer Code must be unique")
    address = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Dealer Data"

    def __unicode__(self):
        return self.dealer_id


class ServiceAdvisor(models.Model):
    service_advisor_id = models.CharField(max_length=15, blank=False, unique=True, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Service Advisor Data"

    def __unicode__(self):
        return self.phone_number

##################################################################
#############Service Advisor and Registered Relationship MODEL####


class ServiceAdvisorDealerRelationship(models.Model):
    dealer_id = models.ForeignKey(RegisteredDealer, null=False)
    service_advisor_id = models.ForeignKey(ServiceAdvisor, null=False)
    status = models.CharField(max_length=10, blank=False, null=False)
    id = models.AutoField(primary_key=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Service Advisor And Dealer Relationship"

    def __unicode__(self):
        return self.id

##################################################################

#############GLADMINDUSER & CUSTOMERDATA MODEL####################

'''
Gladmindusers have auto generated glamind customer id,
and unique phone numner
'''
class GladMindUsers(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    gladmind_customer_id = models.CharField(max_length=215,unique=True, null=True)
    customer_name = models.CharField(max_length=215)
    email_id = models.EmailField(max_length=215, null=True, blank=True)
    phone_number = models.CharField(max_length=15,unique=True)
    registration_date = models.DateTimeField(default=datetime.now())
    address=models.CharField(max_length=255, null=True, blank=True)
    country=models.CharField(max_length=255, null=True, blank=True)
    state=models.CharField(max_length=255, null=True, blank=True)
    date_of_birth=models.CharField(max_length=255, null=True, blank=True)
    gender=models.IntegerField(max_length=50, null=True, blank=True)
    img_url=models.FileField(upload_to="users", blank=True)
    thumb_url=models.FileField(upload_to="users" , blank=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number

    def save(self, force_insert=False, force_update=False, using=None):
        return super(GladMindUsers, self).save(force_insert, force_update, using)
    
'''
CustomerData contains info about
which customer bought which product and
the vin of product and the dealer
'''

class ProductData(models.Model):
    id=models.AutoField(primary_key=True)
    vin=models.CharField(max_length=215, null=True, unique=True, blank=True)
    customer_phone_number = models.ForeignKey(GladMindUsers, null=True, blank=True)
    product_type= models.ForeignKey(ProductTypeData, null=True, blank=True)
    sap_customer_id = models.CharField(max_length=215, null=True, blank=True, unique=True)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    invoice_date=models.DateTimeField(null=True, blank=True)
    dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    
    #Added below column for after buy application
    customer_product_number = models.CharField(max_length=255, null=True, blank=True)
    purchased_from=models.CharField(max_length=255, null=True, blank=True)
    seller_email=models.EmailField(max_length=255, null=True, blank=True)
    seller_phone=models.CharField(max_length=255, null=True, blank=True)
    warranty_yrs=models.FloatField(null=True,blank=True)
    insurance_yrs=models.FloatField(null=True, blank=True)
    
    invoice_loc=models.FileField(upload_to="invoice", blank=True)
    warranty_loc=models.FileField(upload_to="warrenty", blank=True)
    insurance_loc=models.FileField(upload_to="insurance", blank=True)
    
    last_modified=models.DateTimeField(null=False,default=datetime.now())
    created_on=models.DateTimeField(null=True, default=datetime.now())
    isActive = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Product Data"
        
    def __unicode__(self):
        return self.vin
    
####################################################################

STATUS_CHOICES = ((1, 'Unused'), (2, 'Closed'), (3, 'Expired'),(4,'In Progress'))

class CouponData(models.Model):
    vin = models.ForeignKey(ProductData, null=False)
    unique_service_coupon = models.CharField(max_length=215, unique=True, null=False)
    valid_days = models.IntegerField(max_length=10,null=False)
    valid_kms = models.IntegerField(max_length=10,null=False)
    service_type=models.IntegerField(max_length=10,null=False)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=True, blank=True)
    status= models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    closed_date = models.DateTimeField(null=True, blank=True)
    mark_expired_on = models.DateTimeField(null=True, blank=True)
    actual_service_date = models.DateTimeField(null=True, blank=True)
    actual_kms = models.CharField(max_length=10, null=True, blank=True)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    schedule_reminder_date = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = "gladminds"
        ordering = ['service_type',]
        verbose_name_plural = "Coupon Information"

class MessageTemplate(models.Model):
    template_key = models.CharField(max_length=255, unique=True, null=False)
    template = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Message Template"
