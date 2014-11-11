from tastypie.authorization import Authorization
from tastypie import fields

from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.gm import models as gm_models


class IndustryResource(CustomBaseModelResource):
    class Meta:
        queryset = gm_models.Industry.objects.all()
        resource_name = "industries"
        authorization = Authorization()


class BrandResource(CustomBaseModelResource):
    industry = fields.ForeignKey(IndustryResource, 'industry', full=True)

    class Meta:
        queryset = gm_models.Brand.objects.all()
        resource_name = "brands"
        authorization = Authorization()


class BrandCategoryResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', full=True)

    class Meta:
        queryset = gm_models.BrandCategory.objects.all()
        resource_name = "brand-categories"
        authorization = Authorization()
