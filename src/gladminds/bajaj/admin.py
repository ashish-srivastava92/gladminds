from django.contrib.admin import AdminSite
from gladminds.bajaj.models import BrandData
from django.contrib.auth.models import User

from gladminds.bajaj.models import UserProfile


class BajajAdminSite(AdminSite):
    pass

brand_admin = BajajAdminSite(name='bajaj')

brand_admin.register(BrandData)
brand_admin.register(User)
brand_admin.register(UserProfile)