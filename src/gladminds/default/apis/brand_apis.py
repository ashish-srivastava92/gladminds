from tastypie.authorization import Authorization
from tastypie import fields

from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.default import models as gm_models
from tastypie.constants import ALL


class IndustryResource(CustomBaseModelResource):
    class Meta:
        queryset = gm_models.Industry.objects.all()
        resource_name = "industries"
        authorization = Authorization()


class ServiceTypeResource(CustomBaseModelResource):

    class Meta:
        queryset = gm_models.ServiceType.objects.all()
        resource_name = "services"
        authorization = Authorization()


class ServiceResource(CustomBaseModelResource):
    service_type = fields.ForeignKey(ServiceTypeResource, 'type', full=True)

    class Meta:
        queryset = gm_models.Service.objects.all()
        resource_name = "service-types"
        authorization = Authorization()
        filtering = {
                     "service_type": ALL
                     }


class BrandResource(CustomBaseModelResource):
    industry = fields.OneToOneField(IndustryResource, 'industry', full=True)
    services = fields.ManyToManyField(ServiceResource, 'services', null=True, full=True)

    class Meta:
        queryset = gm_models.Brand.objects.all()
        resource_name = "brands"
        authorization = Authorization()


class BrandProductCategoryResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', full=True)

    class Meta:
        queryset = gm_models.BrandProductCategory.objects.all()
        resource_name = "brand-product-categories"
        authorization = Authorization()
        filtering = {
                     "brand": ALL
                     }