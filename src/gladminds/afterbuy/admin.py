from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group, Permission
from constance.admin import Config, ConstanceAdmin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from gladminds.afterbuy.models import Brand, Consumer, ProductType,\
MessageTemplate, EmailTemplate, Industry, UserProduct, License,\
    ProductInsuranceInfo, ProductWarrantyInfo, PollutionCertificate,\
    BrandProductCategory, SMSLog, EmailLog, OTPToken, EmailToken
from gladminds.core.admin_helper import IndustryAdmin, BrandAdmin
from gladminds.core.auth_helper import GmApps


class AfterbuyAdminSite(AdminSite):
    pass


class ConsumerAdmin(ModelAdmin):
    search_fields = ('phone_number',)
    list_display = ('user', 'phone_number')


brand_admin = AfterbuyAdminSite(name=GmApps.AFTERBUY)

brand_admin.register(Industry, IndustryAdmin)
brand_admin.register(Brand, BrandAdmin)
brand_admin.register(BrandProductCategory)
brand_admin.register(Consumer, ConsumerAdmin)
brand_admin.register(ProductType)
brand_admin.register(UserProduct)
brand_admin.register(ProductInsuranceInfo)
brand_admin.register(ProductWarrantyInfo)
brand_admin.register(PollutionCertificate)
brand_admin.register(License)

brand_admin.register(User, UserAdmin)
brand_admin.register(Group, GroupAdmin)
brand_admin.register(Permission)

brand_admin.register(MessageTemplate)
brand_admin.register(EmailTemplate)
brand_admin.register(SMSLog)
brand_admin.register(EmailLog)
brand_admin.register(EmailToken)
brand_admin.register(OTPToken)

#https://github.com/comoga/django-constance/issues/51
setattr(Config._meta, 'object_name', 'Config')
brand_admin.register([Config], ConstanceAdmin)

