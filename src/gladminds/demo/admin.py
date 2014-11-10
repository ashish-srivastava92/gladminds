from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from gladminds.demo.models import UserProfile, Dealer, AuthorizedServiceCenter,\
ServiceAdvisor, ProductData, CouponData, MessageTemplate, EmailTemplate, BrandCategory


class DemoAdminSite(AdminSite):
    pass

brand_admin = DemoAdminSite(name='demo')

brand_admin.register(User)
brand_admin.register(UserProfile)
brand_admin.register(Dealer)
#brand_admin.register(DispatchedProduct, ListDispatchedProduct)
brand_admin.register(AuthorizedServiceCenter)
# brand_admin.register(ServiceAdvisor, ServiceAdvisorAdmin)
# brand_admin.register(ProductData, ProductDataAdmin)
# brand_admin.register(CouponData)
# brand_admin.register(EmailTemplate, EmailTemplateAdmin)
# brand_admin.register(MessageTemplate, MessageTemplateAdmin)
brand_admin.register(BrandCategory)
brand_admin.register(ServiceAdvisor)
brand_admin.register(ProductData)
brand_admin.register(CouponData)
brand_admin.register(EmailTemplate)
brand_admin.register(MessageTemplate)