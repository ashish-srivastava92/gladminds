import unittest
from django.core import management
from gladminds.models import common
from gladminds.aftersell.models import logs


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
    
    def get_asc_obj(self, **kwargs):
        asc_obj = common.RegisteredASC(**kwargs)
        asc_obj.save()
        return asc_obj
        
    def _get_model_obj(self, model):
        model_obj = model.save()
        return model_obj
    
    def filter_coupon_obj(self, coupon_id=None):
        coupon_obj = common.CouponData.objects.filter(unique_service_coupon=coupon_id)
        return coupon_obj[0]
    
    def get_datafeed_log(self, **kwargs):
        feed_log = logs.DataFeedLog(**kwargs)
        feed_log.save()
        return feed_log
    
    def get_message_template(self, **kwargs):
        msg_template = common.MessageTemplate(**kwargs)
        msg_template.save()
        return msg_template

class RequestObject(object):
    '''
    This class creates a request type of object.
    '''
    def __init__(self, user=None, data=None, file=None):
        self.user = user
        self.POST = data
        self.FILES = file
        