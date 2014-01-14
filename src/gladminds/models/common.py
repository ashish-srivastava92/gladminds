from django.db import models
from django.db.models.fields.related import  ForeignKey,OneToOneField
  
        
class RegisteredDealer(models.Model):
    dealer_id=models.CharField(max_length=10,blank=False, null= False)
    phone_number = models.IntegerField(max_length=10,blank=False, null= False, unique= True)
    class Meta:
        app_label="gladminds" 

class GladMindUsers(models.Model):
    gladmind_customer_id=models.CharField(max_length=215,null= False)
    phone_number=models.CharField(max_length=10)
    registration_date = models.DateTimeField()
    class Meta:
        app_label="gladminds" 
        verbose_name_plural = "Gladmind Users"
        
    def __unicode__(self):
        return self.phone_number
 

    def save(self, force_insert=False, force_update=False, using=None):
        return super(GladMindUsers, self).save(force_insert, force_update, using)
        
class CustomerData(models.Model):
    phone_number=models.ForeignKey(GladMindUsers, null=False)
    sap_customer_id=models.CharField(max_length=215,null= False)
    product_id=models.CharField(max_length=215,null= False)
    unique_service_code=models.CharField(max_length=215,null= False)
    valid_days = models.IntegerField(max_length=10)
    valid_kms=models.IntegerField(max_length=10)
    is_expired = models.BooleanField()
    is_closed = models.BooleanField()
    closed_date = models.DateTimeField(null=True)
    expired_date = models.DateTimeField(null=True)
    class Meta:
        app_label="gladminds" 
        verbose_name_plural = "Customer Data"
        
    def __unicode__(self):
        return self.unique_service_code
    
class ServiceCouponData(models.Model):
    service_coupon=models.ForeignKey(CustomerData,unique=True, null=False)
    last_reminder_date=models.DateTimeField(null=True)
    schedule_reminder_date=models.DateTimeField(null=True)
    class Meta:
        app_label="gladminds" 
    
        
    
    
    
