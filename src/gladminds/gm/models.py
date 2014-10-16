from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from gladminds.core.base_models import BaseModel, MessageTemplate, EmailTemplate


class Industry(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)


class Service(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Services"


class Brand(BaseModel):
    brand_id = models.CharField(
        max_length=50, null=False, unique=True, help_text="Brand Id must be unique")
    brand_name = models.CharField(max_length=250, null=False)
    brand_logo = models.CharField(max_length=200, null=True, blank=False)
    is_active = models.BooleanField(default=True)
    industry = models.ForeignKey(Industry)
    services = models.ManyToManyField(Service, through="BrandService")

    class Meta:
        app_label = "gm"
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


class BrandService(BaseModel):
    brand = models.ForeignKey(Brand)
    service = models.ForeignKey(Service)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "gm"


class GladmindsUser(BaseModel):
    user = models.OneToOneField(User, primary_key=True)
    gladmind_customer_id = models.CharField(
        max_length=215, unique=True, null=True)
    phone_number = models.CharField(
                   max_length=15, blank=True, null=True)
    profile_pic = models.CharField(
                   max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other'),
    )
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              blank=True, null=True)
    #added these attributes for afterbuy application
    accepted_terms = models.BooleanField(default=False)
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    )

    tshirt_size = models.CharField(max_length=2, choices=SIZE_CHOICES,
                                   blank=True, null=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.phone_number


class UserProduct(BaseModel):
    gm_user = models.ForeignKey(GladmindsUser)
    brand = models.ForeignKey(Brand)
    product_type = models.CharField(max_length=100)
    product_id = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "User Products"


class OTPToken(BaseModel):
    user = models.ForeignKey(GladmindsUser)
    token = models.CharField(max_length=256)
    request_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "OTPs"


class UserNotification(BaseModel):
    gm_user = models.ForeignKey(GladmindsUser)
    message = models.CharField(max_length=256, null=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "notification"


class MessageTemplate(MessageTemplate):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Message Template"


class EmailTemplate(EmailTemplate):

    class Meta:
        app_label = "gm"
        verbose_name_plural = "Email Template"



##################################################################################################



class UserProducts(models.Model):
    vin = models.CharField(max_length=215, null=True, unique=True, blank=True)
    customer_phone_number = models.ForeignKey(
        GladmindsUser, null=True, blank=True)
    item_name = models.CharField(max_length=256, null=False)
#     product_type = models.ForeignKey(ProductTypeData, null=True, blank=True)
    product_purchase_date = models.DateTimeField(null=True, blank=True)
    purchased_from = models.CharField(max_length=255, null=True, blank=True)
    seller_email = models.EmailField(max_length=255, null=True, blank=True)
    seller_phone = models.CharField(max_length=255, null=True, blank=True)
    warranty_yrs = models.FloatField(null=True, blank=True)
    insurance_yrs = models.FloatField(null=True, blank=True)
    invoice_loc = models.FileField(upload_to="invoice", blank=True)
    warranty_loc = models.FileField(upload_to="warrenty", blank=True)
    insurance_loc = models.FileField(upload_to="insurance", blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "userProducts"

    def __unicode__(self):
        return self.vin


class UserMobileInfo(models.Model):
    user = models.ForeignKey(GladmindsUser)
    IMEI = models.CharField(max_length=50, null=True, blank=True, unique=True)
    ICCID = models.CharField(max_length=50, null=True, blank=True)
    phone_name = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = "gm"
        verbose_name_plural = "mobile info"

