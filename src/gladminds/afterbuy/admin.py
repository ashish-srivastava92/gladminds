from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from gladminds.afterbuy.models import Brand, Consumer, ProductType,\
MessageTemplate, EmailTemplate, Industry, UserProduct


class AfterbuyAdminSite(AdminSite):
    pass

brand_admin = AfterbuyAdminSite(name='afterbuy')

brand_admin.register(Industry)
brand_admin.register(Brand)
brand_admin.register(User)
brand_admin.register(Consumer)
brand_admin.register(ProductType)
brand_admin.register(UserProduct)
brand_admin.register(MessageTemplate)
brand_admin.register(EmailTemplate)

