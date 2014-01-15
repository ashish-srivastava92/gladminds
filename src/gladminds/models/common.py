from django.db import models
from django.db.models.fields.related import  ForeignKey,OneToOneField
  
        
class RegisteredDealer(models.Model):
    dealer_id=models.CharField(max_length=10,blank=False, null= False)
    phone_number = models.IntegerField(max_length=10,blank=False, null= False, unique= True)
    class Meta:
        app_label="gladminds" 
    def __unicode__(self):
        return self.dealer_id

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
    unique_service_coupon=models.CharField(max_length=215,unique= True,null= False)
    valid_days = models.IntegerField(max_length=10)
    valid_kms=models.IntegerField(max_length=10)
    is_expired = models.BooleanField()
    is_closed = models.BooleanField()
    closed_date = models.DateField(null=True,blank=True)
    expired_date = models.DateField(null=True)
    product_purchase_date=models.DateField()
    actual_service_date=models.DateField(null=True,blank=True)
    actual_kms=models.CharField(max_length=10,null= True,blank=True)
    dealer=models.ForeignKey(RegisteredDealer, null=False)
    last_reminder_date=models.DateField(null=True,blank=True)
    schedule_reminder_date=models.DateField(null=True,blank=True)
    class Meta:
        app_label="gladminds" 
        verbose_name_plural = "Customer Data"
        
   

    
        
    
    
    
