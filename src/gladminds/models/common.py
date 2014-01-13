from django.db import models
from django.db.models.fields.related import  ForeignKey,OneToOneField
  
class Customer(models.Model):
    customer_id=models.CharField(max_length=215,primary_key=True)
    phone_number = models.IntegerField(max_length=10,blank=False, null= False, unique= True)
    registration_date = models.DateTimeField()
    is_authenticated=models.BooleanField(default=False)
    class Meta:
        app_label="gladminds"
              
class Product(models.Model):
    product_id=models.CharField(max_length=215,primary_key=True) 
    brand_name=models.CharField(max_length=215)
    class Meta:
        app_label="gladminds" 
    
    def __unicode__(self):
        return self.product_id

    def save(self, force_insert=False, force_update=False, using=None):
        return super(Product, self).save(force_insert, force_update, using)
        
class Service(models.Model):
    product=models.ForeignKey(Product, null=True)
    unique_service_code=models.CharField(max_length=215,primary_key=True)
    valid_days = models.IntegerField(max_length=10)
    start_kms = models.IntegerField(max_length=10)
    end_kms = models.IntegerField(max_length=10)
    is_expired = models.BooleanField()
    is_closed = models.BooleanField()
    closed_date = models.DateTimeField(null=True)
    expired_date = models.DateTimeField(null=True)
    expiry_time=models.CharField(max_length=215, null=False)
    class Meta:
        app_label="gladminds"  
        
class ProductPurchased(models.Model):
    customer_id=models.CharField(max_length=215,null= False)
    sap_customer_id = models.CharField(max_length=215, null = False)
    purchased_date = models.DateTimeField()
    product_id=models.ForeignKey(Product, null=False,primary_key=True)
    class Meta:
        app_label="gladminds" 
        db_table = "productpurchased"
        verbose_name_plural = "product Purchased"
        
class RegisteredDealer(models.Model):
    phone_number = models.IntegerField(max_length=10,blank=False, null= False, unique= True)
    class Meta:
        app_label="gladminds" 
        


class GladMindUsers(models.Model):
    gcid=models.CharField(max_length=215,null= False)
    phone_number=models.CharField(max_length=10,null= False,unique= True)
    class Meta:
        app_label="gladminds" 
        
    def __unicode__(self):
        return self.gcid

    def save(self, force_insert=False, force_update=False, using=None):
        return super(GladMindUsers, self).save(force_insert, force_update, using)
        
class SAPData(models.Model):
    phone_number=models.ForeignKey(GladMindUsers, null=False)
    customer_id=models.CharField(max_length=215,null= False,unique= True)
    product_id=models.CharField(max_length=215,null= False,unique= True)
    unique_service_code=models.CharField(max_length=215,null= False)
    validity_days_kms=models.CharField(max_length=215,null= False)
    status=models.CharField(max_length=215,null= False)
    class Meta:
        app_label="gladminds" 
    
    
    
