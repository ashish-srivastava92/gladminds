from django.db import models
from django.contrib.auth.models import User
from gladminds.core.base_models import BaseModel, MessageTemplate,\
           EmailTemplate, SMSLog, EmailLog, AuditLog, Industry, Brand,\
           ProductType, OTPToken, BrandCategory

_APP_NAME = 'afterbuy'


class Industry(Industry):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Industries"


class Brand(Brand):
    industry = models.ForeignKey(Industry)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brands"


class BrandCategory(BrandCategory):
    brand = models.ForeignKey(Brand)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Categories"


class ProductType(ProductType):
    brand_category = models.ForeignKey(
            BrandCategory, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Types"


class Consumer(BaseModel):
    user = models.OneToOneField(User, primary_key=True)
    consumer_id = models.CharField(
        max_length=50, unique=True)
    phone_number = models.CharField(
                   max_length=15, blank=True, null=True)
    image_url = models.CharField(
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
        app_label = _APP_NAME
        verbose_name_plural = "Consumers"


class OTPToken(OTPToken):
    user = models.ForeignKey(Consumer)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "OTPs"


class UserNotification(BaseModel):
    user = models.ForeignKey(Consumer)
    message = models.TextField()
    action = models.TextField(blank=True, null=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Notifications"


class UserProduct(models.Model):
    consumer = models.ForeignKey(Consumer)
    brand = models.ForeignKey(Brand)
    type = models.ForeignKey(ProductType)
    purchase_date = models.DateTimeField(null=True, blank=True)
    brand_product_id = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50)
    image_url = models.CharField(
                   max_length=200, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "User Products"


class UserMobileInfo(BaseModel):
    user = models.ForeignKey(Consumer)
    IMEI = models.CharField(max_length=50, null=True, blank=True, unique=True)
    ICCID = models.CharField(max_length=50, null=True, blank=True)
    phone_name = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    version = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Mobile Details"


class ProductInsuranceInfo(BaseModel):
    product = models.ForeignKey(UserProduct)
    agency_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=20, unique=True)
    premium = models.FloatField(null=True, blank=True)
    agency_contact = models.CharField(
        max_length=25, blank=True, null=True)
    insurance_type = models.CharField(max_length=15, null=True, blank=True)
    nominee = models.CharField(max_length=15, blank=True, null=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    vehicle_value = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Insurance Info"


class ProductWarrantyInfo(BaseModel):
    product = models.ForeignKey(UserProduct)
    issue_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "product warranty info"


class PollutionCertificate(BaseModel):
    product = models.ForeignKey(UserProduct)
    pucc_number = models.CharField(max_length=25)
    issue_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank= True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Pollution Certificate"


class RegistrationCertificate(BaseModel):
    product = models.ForeignKey(UserProduct)
    vehicle_registration_number = models.CharField(max_length=50)
    registration_date = models.DateTimeField(null=True, blank=True)
    chassis_number = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=25)
    address = models.CharField(max_length=512)
    registration_upto = models.DateTimeField(null=True, blank=True)
    manufacturer = models.CharField(max_length=512)
    manufacturing_date = models.DateTimeField(null=True, blank=True)
    model_number = models.CharField(max_length=50)
    colour = models.CharField(max_length=25)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Registration Certificate"


class License(BaseModel):
    product = models.ForeignKey(UserProduct)
    license_number = models.CharField(max_length=50)
    issue_date = models.DateTimeField(null=True)
    expiry_date = models.DateTimeField(null=True)
    blood_group = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "license"


class Invoice(BaseModel):
    product = models.ForeignKey(UserProduct)
    invoice_number = models.CharField(max_length=50)
    purchase_date = models.DateTimeField(null=True, blank=True)
    dealer_name = models.CharField(max_length=50)
    dealer_contact = models.CharField(
        max_length=25, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "invoice"


class Support (BaseModel):
    brand = models.ForeignKey(Brand)
    brand_category = models.ForeignKey(null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    toll_free = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.CharField(max_length=25, blank=True, null=True)

#     service_center_name = models.CharField(max_length=25, blank=True, null=True)
#     service_center_number = models.CharField(max_length=255, blank=True, null=True)
#     feedback_form = models.CharField(max_length=255, blank=True, null=True)
#     service_center_email_id = models.CharField(max_length=25, blank=True, null=True)
#     service_center_website = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "support"


class MessageTemplate(MessageTemplate):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Message Template"


class EmailTemplate(EmailTemplate):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Template"


class SMSLog(SMSLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "SMS Log"


class EmailLog(EmailLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Log"


class AuditLog(AuditLog):
    user = models.ForeignKey(Consumer)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Audit Log"
