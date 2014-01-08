from django.db import models
from django.db.models.fields.related import  ForeignKey,OneToOneField
  
class Customer(models.Model):
    customer_id=models.CharField(max_length=215,primary_key=True)
    phone_number = models.IntegerField(max_length=10,blank=False, null= False, unique= True)
    is_authenticated=models.BooleanField(default=False)
    class Meta:
        app_label="gladminds"
              
class Product(models.Model):
    product_id=models.CharField(max_length=215,primary_key=True) 
    brand_name=models.CharField(max_length=215)
    class Meta:
        app_label="gladminds" 
        
class Service(models.Model):
    product=ForeignKey(to=Product,related_name='product')
    unique_service_code=models.CharField(max_length=215,primary_key=True)
    class Meta:
        app_label="gladminds"  
        
class ProductPurchased(models.Model):
    customer_id=models.CharField(max_length=215,null= False)
    product_id=models.CharField(max_length=215,null= False)
    class Meta:
        app_label="gladminds" 
        
class RegisteredDealers(models.Model):
    phone_number = models.IntegerField(max_length=10,blank=False, null= False, unique= True)
    class Meta:
        app_label="gladminds" 
    
    
