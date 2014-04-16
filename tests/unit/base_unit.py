import unittest
from django.core import management
from gladminds.models import common 


class GladmindsUnitTestCase(unittest.TestCase):
    def setUp(self):
        super(GladmindsUnitTestCase, self).setUp()
#        management.call_command('loaddata', 'etc/testdata/template.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/customer.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/brand.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/producttype.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/dealer.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/serviceadvisor.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/product.json', verbosity=0)
#        management.call_command('loaddata', 'etc/testdata/coupon.json', verbosity=0)
        
    def get_coupon_obj(self, **kwargs):
        return self._get_model_obj(common.CouponData(**kwargs))

    #TODO: Using _get_model_obj() does not work on below function
    def get_product_obj(self, **kwargs):
        product_data = common.ProductData(**kwargs)
        product_data.save()
        return product_data

    #TODO: Using _get_model_obj() does not work on below function
    def get_delear_obj(self, **kwargs):
        delear_data = common.RegisteredDealer(**kwargs)
        delear_data.save()
        return delear_data

    def get_product_type_obj(self, **kwargs):
        return self._get_model_obj(common.ProductTypeData(**kwargs))

    #TODO: Using _get_model_obj() does not work on below function
    def get_brand_obj(self, **kwargs):
        brand_obj = common.BrandData(**kwargs)
        brand_obj.save()
        return brand_obj

    #TODO: Using _get_model_obj() does not work on below function
    def get_service_advisor_obj(self, **kwargs):
        service_advisor_obj = common.ServiceAdvisor(**kwargs)
        service_advisor_obj.save()
        return service_advisor_obj

    def get_dealer_service_advisor_obj(self, **kwargs):
        return self._get_model_obj(common.ServiceAdvisorDealerRelationship(**kwargs))

    def get_customer_obj(self, **kwargs):
        return self._get_model_obj(common.GladMindUsers(**kwargs))
    
    def _get_model_obj(self, model):
        model_obj = model.save()
        return model_obj
    
    def filter_coupon_obj(self, coupon_id=None):
        coupon_obj = common.CouponData.objects.filter(unique_service_coupon=coupon_id)
        return coupon_obj[0]
        