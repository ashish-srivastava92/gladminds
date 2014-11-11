import django.test
from gladminds.bajaj import models


class GladmindsUnitTestCase(django.test.TestCase):
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
        return self._get_model_obj(models.CouponData(**kwargs))

    #TODO: Using _get_model_obj() does not work on below function
    def get_product_obj(self, **kwargs):
        product_data = models.ProductData(**kwargs)
        product_data.save()
        return product_data
    
    #TODO: Using _get_model_obj() does not work on below function
    def get_user_obj(self, **kwargs):
        user = models.User
        delear_data = models.Dealer(**kwargs)
        delear_data.save()
        return delear_data
    
    #TODO: Using _get_model_obj() does not work on below function
    def get_delear_obj(self, **kwargs):
        delear_data = models.Dealer(**kwargs)
        delear_data.save()
        return delear_data

    def get_product_type_obj(self, **kwargs):
        return self._get_model_obj(models.ProductType(**kwargs))

    #TODO: Using _get_model_obj() does not work on below function
    def get_brand_obj(self, **kwargs):
#         brand_obj = common.BrandData(**kwargs)
#         brand_obj.save()
#         return brand_obj
        return None

    #TODO: Using _get_model_obj() does not work on below function
    def get_service_advisor_obj(self, **kwargs):
        service_advisor_obj = models.ServiceAdvisor(**kwargs)
        service_advisor_obj.save()
        return service_advisor_obj

    def get_dealer_service_advisor_obj(self, **kwargs):
        #return self._get_model_obj(aftersell_common.ServiceAdvisorDealerRelationship(**kwargs))
        return None

    def get_customer_obj(self, **kwargs):
        return self._get_model_obj(models.UserProfile(**kwargs))
    
    def get_asc_obj(self, **kwargs):
        asc_obj = models.AuthorizedServiceCenter(**kwargs)
        asc_obj.save()
        return asc_obj
        
    def _get_model_obj(self, model):
        model_obj = model.save()
        return model
    
    def filter_coupon_obj(self, coupon_id=None):
        coupon_obj = models.CouponData.objects.filter(unique_service_coupon=coupon_id)
        return coupon_obj[0]
    
    def get_datafeed_log(self, **kwargs):
        feed_log = models.DataFeedLog(**kwargs)
        feed_log.save()
        return feed_log
    
    def get_message_template(self, **kwargs):
        msg_template = models.MessageTemplate(**kwargs)
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
        