from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group, Permission

from gladminds.afterbuy.models import Brand, Consumer, ProductType,\
MessageTemplate, EmailTemplate, Industry, UserProduct, License,\
    ProductInsuranceInfo, ProductWarrantyInfo, PollutionCertificate,\
    BrandProductCategory, SMSLog, EmailLog


class AfterbuyAdminSite(AdminSite):
    pass

brand_admin = AfterbuyAdminSite(name='afterbuy')

brand_admin.register(Industry)
brand_admin.register(Brand)
brand_admin.register(BrandProductCategory)
brand_admin.register(Consumer)
brand_admin.register(ProductType)
brand_admin.register(UserProduct)
brand_admin.register(ProductInsuranceInfo)
brand_admin.register(ProductWarrantyInfo)
brand_admin.register(PollutionCertificate)
brand_admin.register(License)

brand_admin.register(User)
brand_admin.register(Group)
brand_admin.register(Permission)

brand_admin.register(MessageTemplate)
brand_admin.register(EmailTemplate)
brand_admin.register(SMSLog)
brand_admin.register(EmailLog)

