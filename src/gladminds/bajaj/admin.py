from django.contrib.admin import AdminSite
from gladminds.bajaj.models import BrandData

class BajajAdminSite(AdminSite):
    pass

brand_admin = BajajAdminSite(name='bajaj')

brand_admin.register(BrandData)