from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from gladminds.gm.models import UserProfile, GladMindUsers
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    USER_DESIGNATION, RATINGS
    

##########################################################################
########################## ASC Save Form #########################
ASC_STATUS_CHOICES = ((1, 'In Progress'), (2, 'Failed'))

class ASCSaveForm(models.Model):
    name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False,
                                                         unique=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.SmallIntegerField(choices=ASC_STATUS_CHOICES, default=1)
    timestamp = models.DateTimeField(default=datetime.now)
    dealer_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "ASC Save Form"


class UCNRecovery(models.Model):
    reason = models.TextField(null=False)
    user = models.ForeignKey(UserProfile)
    sap_customer_id = models.CharField(max_length=215, null=True, blank=True)
    file_location = models.CharField(max_length=215, null=True, blank=True)
    request_date = models.DateTimeField(default=datetime.now())

    class Meta:
        abstract = True
        verbose_name_plural = "UCN recovery logs"

###################################################################

######################DEALER-SA MODELS#############################


class RegisteredDealer(models.Model):
    dealer_id = models.CharField(
        max_length=25, blank=False, null=False, unique=True, help_text="Dealer Code must be unique")
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, default='dealer', blank=False)
    dependent_on = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Dealer Data"

    def __unicode__(self):
        return self.dealer_id


class ServiceAdvisor(models.Model):
    service_advisor_id = models.CharField(
        max_length=15, blank=False, unique=True, null=False)
    name = models.CharField(max_length=25, blank=False, null=False)
    phone_number = models.CharField(
        max_length=15, blank=False, null=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        verbose_name_plural = "Service Advisor Data"

    def __unicode__(self):
        return self.phone_number


#     NOT IN USE CHECK AND UNCOMMENT IT

# class RegisteredASC(models.Model):
#     user = models.OneToOneField(UserProfile, null=True, blank=True)
#     phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
#     asc_name = models.CharField(max_length=215)
#     email_id = models.EmailField(max_length=215, null=True, blank=True)
#     registration_date = models.DateTimeField(default=datetime.now())
#     address = models.CharField(max_length=255, null=True, blank=True)
#     city = models.CharField(max_length=255, null=True, blank=True)
#     country = models.CharField(max_length=255, null=True, blank=True)
#     state = models.CharField(max_length=255, null=True, blank=True)
#     img_url = models.FileField(upload_to="users", blank=True)
#     isActive = models.BooleanField(default=True)
#     asc_id = models.CharField(
#         max_length=20, blank=False, unique=True, null=False)
#     dealer_id = models.ForeignKey(RegisteredDealer, null=True, blank=True)
# 
#     class Meta:
#         abstract = True
#         verbose_name_plural = "Registered ASC Form"
        
    
class ServiceDeskUser(models.Model):
    user = models.OneToOneField(UserProfile, null=True, blank=True)
    email_id = models.EmailField(max_length=215, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    designation = models.CharField(max_length=10, choices = USER_DESIGNATION)
    
    class Meta:
        verbose_name_plural = "service desk users"
    
    def __unicode__(self):
        return self.phone_number
    

########################### Models Taken from Gladminds Common ##################

class UploadProductCSV(models.Model):
    file_location = settings.PROJECT_DIR + '/data/'
    upload_brand_feed = models.FileField(upload_to=file_location, blank=True)
    upload_dealer_feed = models.FileField(upload_to=file_location, blank=True)
    upload_product_dispatch_feed = models.FileField(
        upload_to=file_location, blank=True)
    upload_product_purchase_feed = models.FileField(
        upload_to=file_location, blank=True)
    upload_coupon_redeem_feed = models.FileField(
        upload_to=file_location, blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Upload Product Data"
        
class BrandData(models.Model):
    pk_brand_id = models.AutoField(primary_key=True)
    brand_id = models.CharField(
        max_length=50, null=False, unique=True, help_text="Brand Id must be unique")
    brand_name = models.CharField(max_length=250, null=False)
    brand_image_loc = models.FileField(
        upload_to=settings.AFTERBUY_BRAND_LOC, blank=True)
    isActive = models.BooleanField(default=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Brand Data"

    def __unicode__(self):
        return self.brand_id

    def image_tag(self):
        if self.brand_name == 'Bajaj':
            url = settings.STATIC_URL + 'img/bajaj.jpg'
            return u'<img src= ' + url + ' style="max-width: 37%;max-height: 15%" />'
        elif self.brand_name == 'Honda':
            url = settings.STATIC_URL + 'img/honda.jpg'
            return u'<img src= ' + url + ' style="max-width: 37%;max-height: 15%" />'
        else:
            url = settings.STATIC_URL + 'img/noimage.jpg'
            return u'<img src= ' + url + ' style="max-width: 37%;max-height: 15%" />'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


'''
ProductTypeData  is linked to Brand data
For 1 Brand there can be multiple Products
'''






####################################################################




##################################################################
####################Message Template DB Storage###################


class MessageTemplate(models.Model):
    template_key = models.CharField(max_length=255, unique=True, null=False)
    template = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Message Template"

####################################################################
########################TOTP Details################################

class OTPToken(models.Model):
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    token = models.CharField(max_length=256, null=False)
    request_date = models.DateTimeField(null=True, blank=True)
    email = models.CharField(max_length=50, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "OTPs"


##################################################################
####################Message Template DB Storage###################


class EmailTemplate(models.Model):
    template_key = models.CharField(max_length=255, unique=True, null=False,\
                                     blank=False)
    sender = models.CharField(max_length=512, null=False)
    reciever = models.CharField(max_length=512, null=False)
    subject = models.CharField(max_length=512, null=False)
    body = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=512, null=True)

    class Meta:
        abstract = True
        verbose_name_plural = "Email Template"


class SASaveForm(models.Model):
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    status = models.CharField(max_length=10, blank=False, null=False)

    class Meta:
        abstract = True
        verbose_name_plural = "SA Save Form"
    

"""
Monkey-patch the Site object to include folder for template
"""
# FolderNameField(blank=True).contribute_to_class(Site,'folder_name')