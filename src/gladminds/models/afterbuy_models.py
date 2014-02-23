from django.db import models
from django.conf import settings

'''
 MyItems model define items of user
'''       
class MyItems(models.Model):
    item_id=models.AutoField(primary_key=True)
    u_id=models.CharField(max_length=255, null=False)
    p_id=models.CharField(max_length=255, null=False)
    m_id=models.CharField(max_length=255, null=False)
    item_num=models.CharField(max_length=255, null=False)
    pur_date=models.DateTimeField(null=False)
    purchased_from=models.CharField(max_length=255, null=False)
    seller_email=models.EmailField(max_length=255, null=False)
    seller_phone=models.CharField(max_length=255, null=False)
    warranty_yrs=models.FloatField(null=False)
    insurance_yrs=models.FloatField(null=False)
    invoice_url=models.CharField(max_length=255, null=False)
    warranty_url=models.CharField(max_length=255, null=False)
    insurance_url=models.CharField(max_length=255, null=False)
    date=models.DateTimeField(null=False)
    edited=models.DateTimeField(null=False,default='2000-00-00 00:00:00')
    active = models.PositiveIntegerField(max_length=1,default=1,null=False)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "MyItems"       
        
class Products(models.Model):
    p_id= models.AutoField(primary_key=True)
    product=models.CharField(max_length=255, null=False)
    prd_img=models.CharField(max_length=255, null=False)
    active = models.PositiveIntegerField(max_length=1,default=0,null=False)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Products"    
        
        
'''
Registration model defines user registration details
'''
class Registration(models.Model):
    id=models.AutoField(primary_key=True)
    unique_id=models.CharField(max_length=255, null=False)
    name=models.CharField(max_length=255, null=False)
    email=models.EmailField(max_length=255, null=False)
    mobile=models.CharField(max_length=255, null=False)
    password=models.CharField(max_length=50, null=False)
    address=models.CharField(max_length=255,unique=True, null=False)
    country=models.CharField(max_length=50, null=False)
    dob=models.CharField(max_length=50, null=False)
    gender=models.IntegerField(max_length=50, null=False)
    img_url=models.CharField(max_length=50, null=False)
    thumb_url=models.CharField(max_length=50, null=False)
    enabled = models.PositiveIntegerField(max_length=1,default=1,null=False)
    red_date=models.DateTimeField(null=False)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Registration"
        
class Manufacturer(models.Model):
    m_id=models.AutoField(primary_key=True)
    manufacturer=models.CharField(max_length=255, null=False)
    m_logo=models.CharField(max_length=255, null=False)
    active = models.PositiveIntegerField(max_length=1,default=1,null=False)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "Manufacturer"


from django.contrib.auth.models import User  
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    unique_id=models.CharField(max_length=20, null=False ,unique=True)
    address=models.CharField(max_length=255, null=False)
    country=models.CharField(max_length=255, null=False)
    state=models.CharField(max_length=255, null=False)
    mobile_number=models.CharField(max_length=255, null=False)
    class Meta:
        app_label = "gladminds"
        verbose_name_plural = "User"
    
        
