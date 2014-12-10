from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL

from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.afterbuy import models as afterbuy_models
from gladminds.core.apis.authentication import AccessTokenAuthentication


class IndustryResource(CustomBaseModelResource):
    class Meta:
        queryset = afterbuy_models.Industry.objects.all()
        resource_name = 'industries'
        authorization = DjangoAuthorization()
        authentication = AccessTokenAuthentication()
        always_return_data = True
        filtering = {
                     "name": ALL
                     }


class BrandResource(CustomBaseModelResource):
    industry = fields.ForeignKey(IndustryResource, 'industry', full=True)

    class Meta:
        queryset = afterbuy_models.Brand.objects.all()
        resource_name = "brands"
        authorization = DjangoAuthorization()
        authentication = AccessTokenAuthentication()
        always_return_data = True
        filtering = {
                     "industry": ALL_WITH_RELATIONS,
                     "name": ALL
                     }


class BrandProductCategoryResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', full=True)

    class Meta:
        queryset = afterbuy_models.BrandProductCategory.objects.all()
        resource_name = "brand-categories"
        authorization = DjangoAuthorization()
        authentication = AccessTokenAuthentication()
        always_return_data = True
