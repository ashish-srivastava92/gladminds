from django.db import models
from django.db.models.fields.related import  ForeignKey,OneToOneField
  
        

   
class Customer(models.Model):
    cid=models.CharField(max_length=215,primary_key=True)
    phone_number = models.CharField(max_length=10,blank=False, null= False, unique= True)
    class Meta:
        app_label="gladminds"
        
        
class Product(models.Model):
    customer=ForeignKey(to=Customer,related_name='customer')
    product_id=models.CharField(max_length=215,primary_key=True) 
    product_name=models.CharField(max_length=215)
    class Meta:
        app_label="gladminds" 
        
class Service(models.Model):
    product=ForeignKey(to=Product,related_name='product')
    services_code=models.CharField(max_length=215,primary_key=True)
    class Meta:
        app_label="gladminds"  
