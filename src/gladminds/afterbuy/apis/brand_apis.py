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

class BrandResource(CustomBaseModelResource):
    class Meta:
        queryset = afterbuy_models.Brand.objects.all()
        resource_name = "brands"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True

