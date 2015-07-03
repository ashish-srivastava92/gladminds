from django.contrib.admin import AdminSite
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group, Permission

from gladminds.core.auth_helper import GmApps
from gladminds.core.model_fetcher import get_model


class AfterbuyAdminSite(AdminSite):
    pass

class BrandAdmin(ModelAdmin):
    search_fields = ('name', 'industry__name')
    list_display = ('name', 'industry')


class IndustryAdmin(ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


class ConsumerAdmin(ModelAdmin):
    search_fields = ('phone_number',)
    list_display = ('user', 'phone_number')


class ProductTypeAdmin(ModelAdmin):
    search_fields = ('product_type',)
    list_display = ('product_type', 'image_url')

def get_admin_site_custom(brand):
    brand_admin = AfterbuyAdminSite(name=brand)

    brand_admin.register(get_model("Industry", brand), IndustryAdmin)
    brand_admin.register(get_model("Brand", brand), BrandAdmin)
    brand_admin.register(get_model("BrandProductCategory"))
    brand_admin.register(get_model("ServiceType"))
    brand_admin.register(get_model("Service"))
    brand_admin.register(get_model("Consumer", brand), ConsumerAdmin)
    brand_admin.register(get_model("ProductType",brand), ProductTypeAdmin)
    brand_admin.register(get_model("UserProduct", brand))
    brand_admin.register(get_model("ProductInsuranceInfo", brand))
    brand_admin.register(get_model("ProductWarrantyInfo", brand))
    brand_admin.register(get_model("PollutionCertificate", brand))
    brand_admin.register(get_model("License", brand))
    brand_admin.register(get_model("MessageTemplate", brand))
    brand_admin.register(get_model("EmailTemplate", brand))
    brand_admin.register(get_model("SMSLog", brand))
    brand_admin.register(get_model("EmailLog", brand))
    brand_admin.register(get_model("EmailToken", brand))
    brand_admin.register(get_model("OTPToken", brand))
    brand_admin.register(get_model("ProductSpecification", brand))
    brand_admin.register(get_model("ProductFeature", brand))
    brand_admin.register(get_model("RecommendedPart", brand))
    brand_admin.register(get_model("Constant", brand))
    
    brand_admin.register(User, UserAdmin)
    brand_admin.register(Group, GroupAdmin)
    brand_admin.register(Permission)
    
    return brand_admin

brand_admin = get_admin_site_custom(GmApps.AFTERBUY)
