from django.db import models

##################BRAND-PRPDUCT MODELS#######################
'''
BrandData contains brand related information
'''
class BrandData(models.Model):
    brand_id=models.CharField(max_length=50, null=False,unique=True,
                              help_text="Brand Id must be unique")
    brand_name=models.CharField(max_length=250, null=False,unique=True)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Brand Data"

    def __unicode__(self):
        return self.brand_id
    
    
'''
ProductData  is linked to Brand data
For 1 Brand there can be multiple Products
here productid is not vin example:all pulsar200 have same
product_id
'''
    
class ProductData(models.Model):
    brand=models.ForeignKey(BrandData ,null=False)
    product_name=models.CharField(max_length=215, null=False)
    product_id=models.CharField(max_length=215,unique=True, null=False)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Product Data"
        
    def __unicode__(self):
        return self.product_id
        
###################################################################

######################DEALER-SA MODELS#############################    

class RegisteredDealer(models.Model):
    dealer_id = models.CharField(
        max_length=10, blank=False, null=False, unique=True,
        help_text="Dealer Code must be unique")
    address = models.TextField(blank=False)

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Dealer Data"

    def __unicode__(self):
        return self.dealer_id


class ServiceAdvisor(models.Model):
    dealer = models.ForeignKey(RegisteredDealer, null=False)
    service_advisor_id=models.CharField(max_length=10, blank=False,unique=True, null=False)
    name = models.CharField(max_length=10, blank=False, null=False)
    phone_number = models.IntegerField(
        max_length=10, blank=False, null=False, unique=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Service Advisor Data"
    
    def __unicode__(self):
        return self.phone_number
        
##################################################################  

#############GLADMINDUSER & CUSTOMERDATA MODEL####################

'''
Gladmindusers have auto generated glamind customer id,
and unique phone numner
'''
class GladMindUsers(models.Model):
    gladmind_customer_id = models.CharField(max_length=215,unique=True, null=False)
    customer_name = models.CharField(max_length=215, null=True)
    email_id = models.EmailField(max_length=215, null=True)
    phone_number = models.CharField(max_length=10,unique=True)
    registration_date = models.DateTimeField()

    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Gladmind Users"

    def __unicode__(self):
        return self.phone_number

    def save(self, force_insert=False, force_update=False, using=None):
        return super(GladMindUsers, self).save(force_insert, force_update, using)
    
    
'''
CustomerData contains info about
which customer bought which product and
the vin of product and the dealer
'''

class CustomerData(models.Model):
    phone_number = models.ForeignKey(GladMindUsers, null=False)
    product= models.ForeignKey(ProductData, null=False)
    vin=models.CharField(max_length=215, null=False,unique=True)
    sap_customer_id = models.CharField(max_length=215, null=False)
    product_purchase_date = models.DateField()
    dealer = models.ForeignKey(RegisteredDealer, null=False)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Customer Data"
        
    def __unicode__(self):
        return self.vin
    
####################################################################

STATUS_CHOICES = ((1, 'open'), (2, 'closed'), (3, 'expired'))

class CouponData(models.Model):
    vin=models.ForeignKey(CustomerData, null=False)
    unique_service_coupon = models.CharField(
        max_length=215, unique=True, null=False)
    valid_days = models.IntegerField(max_length=10)
    valid_kms = models.IntegerField(max_length=10)
    service_type=models.IntegerField(max_length=10)
    sa_phone_number = models.ForeignKey(ServiceAdvisor, null=False)
    status= models.SmallIntegerField(choices=STATUS_CHOICES,
                                       default=1)
    closed_date = models.DateField(null=True, blank=True)
    mark_expired_on = models.DateField(null=True)
    actual_service_date = models.DateField(null=True, blank=True)
    actual_kms = models.CharField(max_length=10, null=True, blank=True)
    last_reminder_date = models.DateField(null=True, blank=True)
    schedule_reminder_date = models.DateField(null=True, blank=True)
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
