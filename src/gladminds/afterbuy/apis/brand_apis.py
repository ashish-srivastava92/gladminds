from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS

from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.afterbuy import models as afterbuy_models
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import CustomDjangoAuthorization


class IndustryResource(CustomBaseModelResource):
    class Meta:
        queryset = afterbuy_models.Industry.objects.all()
        resource_name = 'industries'
        authorization = CustomDjangoAuthorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post', 'delete','put']
        always_return_data =True


class BrandResource(CustomBaseModelResource):
    industry = fields.ForeignKey(IndustryResource, 'industry', full=True)

    class Meta:
        queryset = afterbuy_models.Brand.objects.all()
        resource_name = "brands"
        authorization = CustomDjangoAuthorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True
        filtering = {
                     "industry": ALL_WITH_RELATIONS
                     }


class BrandProductCategoryResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', full=True)

    class Meta:
        queryset = afterbuy_models.BrandProductCategory.objects.all()
        resource_name = "brand-categories"
        authorization = CustomDjangoAuthorization()
        authentication = AccessTokenAuthentication()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True
