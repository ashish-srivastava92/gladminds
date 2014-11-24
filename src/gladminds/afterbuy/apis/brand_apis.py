from tastypie.authorization import Authorization
from tastypie import fields
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.afterbuy import models as afterbuy_models
from gladminds.bajaj.apis.user_apis import AccessTokenAuthentication


class IndustryResource(CustomBaseModelResource):
    class Meta:
        queryset = afterbuy_models.Industry.objects.all()
        resource_name = 'industries'
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete' ,'put']
        always_return_data =True


class BrandResource(CustomBaseModelResource):
    industry = fields.ForeignKey(IndustryResource, 'industry', full=True)

    class Meta:
        queryset = afterbuy_models.Brand.objects.all()
        resource_name = "brands"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True


class BrandProductCategoryResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', full=True)
    class Meta:
        queryset = afterbuy_models.BrandProductCategory.objects.all()
        resource_name = "brand-categories"
        authorization = Authorization()
        detail_allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True


