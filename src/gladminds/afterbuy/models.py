from uuid import uuid4
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext as _
from constance import config
from gladminds.core import base_models
from gladminds.core.constants import GENDER_CHOICES, SIZE_CHOICES, FUEL_CHOICES
from gladminds.core.model_helpers import PhoneField
from gladminds.core.auth_helper import GmApps
from gladminds.afterbuy.managers.email_token_manager import EmailTokenManager
from gladminds.core.managers.mail import send_email_activation,\
    sent_password_reset_link

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

_APP_NAME = GmApps.AFTERBUY


class Industry(base_models.Industry):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Industries"


class Brand(base_models.Brand):
    industry = models.ForeignKey(Industry)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brands"


class BrandProductCategory(base_models.BrandProductCategory):
    brand = models.ForeignKey(Brand)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Categories"


class ProductType(base_models.ProductType):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Types"


class Consumer(base_models.BaseModel):
    user = models.OneToOneField(User, primary_key=True)
    consumer_id = models.CharField(
        max_length=50, unique=True, default=uuid4)
    phone_number = PhoneField(unique=True)
    image_url = models.CharField(
                   max_length=200, default=settings.DEFAULT_IMAGE_ID)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              blank=True, null=True)
    #added these attributes for afterbuy application
    accepted_terms = models.BooleanField(default=False)
    tshirt_size = models.CharField(max_length=2, choices=SIZE_CHOICES,
                                   blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Consumers"

    def __unicode__(self):
        return self.phone_number + " "+ self.user.first_name


class UserProduct(base_models.BaseModel):
    consumer = models.ForeignKey(Consumer)
    brand = models.ForeignKey(Brand)
    nick_name = models.CharField(max_length=100, default="")
    product_type = models.ForeignKey(ProductType)
    purchase_date = models.DateTimeField(null=True, blank=True)
    brand_product_id = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.CharField(
                   max_length=200, blank=True, null=True)
    color = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "User Products"


class ProductSupport(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.CharField(max_length=25, blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Support"


class RegistrationCertificate(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    registration_number = models.CharField(max_length=50)
    registration_date = models.DateTimeField(null=True, blank=True)
    chassis_number = models.CharField(max_length=50)
    engine_number = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=25)
    relation_name = models.CharField(max_length=25)
    address = models.CharField(max_length=512, null=True, blank=True)
    registration_upto = models.DateTimeField(null=True, blank=True)
    model_year = models.DateField(null=True, blank=True)
    model = models.CharField(max_length=50)
    image_url = models.CharField(max_length=215, null=True, blank=True)
    fuel = models.CharField(max_length=15, choices=FUEL_CHOICES, default='Petrol')
    cylinder = models.IntegerField(blank=True, null=True)
    seating = models.IntegerField(blank=True, null=True)
    cc = models.IntegerField(blank=True, null=True)
    body = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Registration Certificate"


class ProductInsuranceInfo(base_models.BaseModel):
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
    is_expired = models.BooleanField(default=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Product Insurance Info"


class ProductWarrantyInfo(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    issue_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    policy_number = models.CharField(max_length=15, unique=True, blank=True)
    premium = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "product warranty info"


class PollutionCertificate(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    pucc_number = models.CharField(max_length=25)
    issue_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank= True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Pollution Certificate"


class License(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    license_number = models.CharField(max_length=50)
    issue_date = models.DateTimeField(null=True)
    expiry_date = models.DateTimeField(null=True)
    blood_group = models.CharField(max_length=50, null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "license"


class Invoice(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    invoice_number = models.CharField(max_length=50)
    dealer_name = models.CharField(max_length=50)
    dealer_contact = models.CharField(
        max_length=25, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=215, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "invoice"


class Support (base_models.BaseModel):
    brand = models.ForeignKey(Brand)
    brand_product_category = models.ForeignKey(BrandProductCategory, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    toll_free = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email_id = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "support"


class OTPToken(base_models.OTPToken):
    user = models.ForeignKey(Consumer, blank=True, null=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "OTPs"


class UserNotification(base_models.BaseModel):
    consumer = models.ForeignKey(Consumer)
    message = models.TextField()
    action = models.TextField(blank=True, null=True)
    notification_read = models.BooleanField(default=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "User Notifications"


class UserMobileInfo(base_models.BaseModel):
    consumer = models.ForeignKey(Consumer)
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


class UserPreference(base_models.UserPreference):
    consumer = models.ForeignKey(Consumer)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Consumer Preferences"
        unique_together = ("consumer", "key")


class BrandPreference(base_models.BrandPreference):
    brand = models.ForeignKey(Brand)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Brand Preferences"
        unique_together = ("brand", "key")


class Interest(base_models.BaseModel):
    interest_type = models.CharField(max_length=20)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Interests"


class SellInformation(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    amount = models.FloatField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_negotiable = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Interests"


class UserProductImages(base_models.BaseModel):
    product = models.ForeignKey(UserProduct)
    image_url = models.CharField(
                   max_length=200, blank=True, null=True)
    type = models.CharField(max_length=20, default='primary')

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "UserProductImages"


class ServiceType(base_models.BaseModel):
    name = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "ServiceTypes" 


class Service(base_models.BaseModel):
    consumer = models.ForeignKey(Consumer)
    service_type = models.ForeignKey(ServiceType)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Services"


class MessageTemplate(base_models.MessageTemplate):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Message Template"


class EmailTemplate(base_models.EmailTemplate):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Template"


class SMSLog(base_models.SMSLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "SMS Log"


class EmailLog(base_models.EmailLog):

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Email Log"


class AuditLog(base_models.AuditLog):
    user = models.ForeignKey(Consumer, null=True, blank=True)

    class Meta:
        app_label = _APP_NAME
        verbose_name_plural = "Audit Log"


class EmailToken(models.Model):
    ACTIVATED = u"ALREADY_ACTIVATED"
    activation_key = models.CharField(_('activation key'), max_length=40)
    user = models.ForeignKey(Consumer)
    objects = EmailTokenManager()

    class Meta:
        verbose_name_plural = 'email_tokens'

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        Key expiration is determined by a two-step process:
        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.user.date_joined + expiration_date <= datetime_now())
    activation_key_expired.boolean = True

    def send_activation_email(self, reciever_email, site, trigger_mail):
        """
        Send an activation email to the user associated with this
        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'base_url': settings.DOMAIN_BASE_URL}
        if trigger_mail == 'forgot-password':
            ctx_dict = {'activation_key': self.activation_key,
                    'link': config.AFTERBUY_FORGOT_PASSWORD_URL}
            sent_password_reset_link(reciever_email, ctx_dict)
        else:
            send_email_activation(reciever_email, ctx_dict)
