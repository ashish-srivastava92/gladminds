from django.contrib.auth.models import User
from django.test import TestCase

from gladminds.bajaj import models as common
from gladminds.gm import models as gm_common
from gladminds.management.commands import load_gm_migration_data


class GladmindsUnitTestCase(TestCase):
    multi_db = True
    
    def setUp(self):
        super(GladmindsUnitTestCase, self).setUp()
        migration_obj = load_gm_migration_data.Command()
        migration_obj.add_email_template()
        migration_obj.add_sms_template()
        
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

    def create_user_profile(self, **kwargs):
        name = kwargs.get('name', None)
        phone_number = kwargs.get('phone_number', None)
        user_obj = User(username=name, first_name=name)
        user_obj.save()
        user_profile_obj = common.UserProfile(user=user_obj, phone_number=phone_number)
        user_profile_obj.save()
        return user_profile_obj

    #TODO: Using _get_model_obj() does not work on below function
    def get_delear_obj(self, **kwargs):
        user_profile_obj = self.create_user_profile(**kwargs)
        delear_data = common.Dealer(user=user_profile_obj, dealer_id=kwargs.get('name', None))
        delear_data.save()
        return delear_data

    def get_product_type_obj(self, **kwargs):
        return self._get_model_obj(common.ProductType(**kwargs))

    #TODO: Using _get_model_obj() does not work on below function
    def get_brand_obj(self):
        industry_obj = gm_common.Industry(name='automobiles', description='mock description')
        industry_obj.save()
        brand_obj = gm_common.Brand(industry=industry_obj)
        brand_obj.save()
        return brand_obj
    

    #TODO: Using _get_model_obj() does not work on below function
    def get_service_advisor_obj(self, **kwargs):
        service_advisor_id = kwargs.get('service_advisor_id', None)
        user_profile_obj = self.create_user_profile(**kwargs)
        service_advisor_obj = self._get_model_obj(common.ServiceAdvisor(user=user_profile_obj, 
                                                                service_advisor_id=service_advisor_id))
        return service_advisor_obj

    def get_dealer_service_advisor_obj(self, **kwargs):
        from datetime import datetime 
        dealer_obj = kwargs.get('dealer_id', None)
        service_advisor_obj = kwargs.get('service_advisor_id', None)
        status = kwargs.get('status', 'N')
        service_advisor_dealer_obj = common.ServiceAdvisor(user=service_advisor_obj.user, status=status,
                                                           created_date=datetime.now(), dealer=dealer_obj, service_advisor_id=service_advisor_obj.service_advisor_id) 
        service_advisor_dealer_obj.save()
        return service_advisor_dealer_obj

    def get_customer_obj(self, **kwargs):
        return self.create_user_profile(**kwargs)
    
    def get_asc_obj(self, **kwargs):
        asc_obj = common.AuthorizedServiceCenter(**kwargs)
        asc_obj.save()
        return asc_obj
        
    def _get_model_obj(self, model):
        model.save()
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
        