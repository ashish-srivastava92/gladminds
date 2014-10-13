from django.contrib.admin import AdminSite
from gladminds.demo.models import BrandData

class DemoAdminSite(AdminSite):
    pass

brand_admin = DemoAdminSite(name='bajaj')

brand_admin.register(BrandData)