from tastypie.constants import ALL
from tastypie.authorization import Authorization
from tastypie import fields
from django.http.response import HttpResponseRedirect
from django.conf.urls import url
from django.contrib.auth.models import User
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.afterbuy import models as afterbuy_models
from gladminds.settings import API_FLAG, COUPON_URL
from tastypie.utils.urls import trailing_slash


class IndustryResource(CustomBaseModelResource):
    class Meta:
        queryset = afterbuy_models.Industry.objects.all()
        resource_name = 'industry'
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete' ,'put']
        always_return_data =True


class BrandResource(CustomBaseModelResource):
    industry = fields.ForeignKey(IndustryResource, 'industry', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_models.Brand.objects.all()
        resource_name = "brands"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True


class BrandProductCategoryResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', null=True, blank=True, full=True)
    class Meta:
        queryset = afterbuy_models.BrandProductCategory.objects.all()
        resource_name = "brand_category"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True


