import os
import json

from django.conf import settings
from django.test.client import Client
from tastypie.test import ResourceTestCase
from django.core import management
from django.contrib.auth.models import User
from gladminds.bajaj import models as common
from gladminds.management.commands import load_gm_migration_data
from gladminds.bajaj import models as aftersell_common

client  =  Client(SERVER_NAME='bajaj')

class GladmindsResourceTestCase(ResourceTestCase):
    multi_db=True

    def setUp(self):
        super(GladmindsResourceTestCase, self).setUp()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()
        self.MESSAGE_URL = "/v1/messages"

        #old implementation of test case;
        #new implementation do not use this
#         management.call_command('loaddata', 'etc/testdata/template.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/customer.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/brand.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/producttype.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/dealer.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/serviceadvisor.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/product.json', verbosity=0)
#         management.call_command('loaddata', 'etc/testdata/coupon.json', verbosity=0)
#         self.MESSAGE_URL = "/v1/messages"

    def assertSuccessfulHttpResponse(self, resp, msg=None):
        """
        Ensures the response is returning status between 200 and 299,
         both inclusive 
        """
        return self.assertTrue(resp.status_code >= 200 
                               and resp.status_code <= 299, msg)

    def get_coupon_obj(self, **kwargs):
        coupon_obj = common.CouponData(**kwargs)
        coupon_obj.save()
        return coupon_obj

    def get_product_obj(self, **kwargs):
        product_data = common.ProductData(**kwargs)
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

    def get_delear_obj(self, **kwargs):
        return self.create_user_profile(**kwargs)

    def get_product_type_obj(self, **kwargs):
        product_type_data_obj = common.ProductType(**kwargs)
        product_type_data_obj.save()
        return product_type_data_obj

    def get_brand_obj(self, **kwargs):
        #brand_obj = common.Brand(**kwargs)
        #brand_obj.save()
        #return brand_obj
        return None

    def get_service_advisor_obj(self, **kwargs):
        service_advisor_id = kwargs.get('service_advisor_id', None)
        status = kwargs.get('status', 'Y')
        user_profile_obj = self.create_user_profile(**kwargs)
        service_advisor_obj = common.ServiceAdvisor(user=user_profile_obj, 
                                                     status=status, service_advisor_id=service_advisor_id)
        service_advisor_obj.save()
        return service_advisor_obj
    
    def get_dealer_service_advisor_obj(self, **kwargs):
#         dealer_service_advisor_obj = aftersell_common.ServiceAdvisorDealerRelationship(**kwargs)
#         dealer_service_advisor_obj.save()
#         return dealer_service_advisor_obj
         return None

    def get_customer_obj(self, **kwargs):
        #customer_obj = common.GladMindUsers(**kwargs)
        #customer_obj.save()
        return None

    def filter_coupon_obj(self, coupon_id=None):
        coupon_obj = common.CouponData.objects.filter(unique_service_coupon=coupon_id)
        return coupon_obj[0]

    def get_temp_customer_obj(self, **kwargs):
        temp_customer_obj = common.CustomerTempRegistration.objects.get(**kwargs)
        return temp_customer_obj

    def get_temp_asc_obj(self, **kwargs):
        temp_asc_obj = aftersell_common.ASCTempRegistration.objects.get(**kwargs)
        return temp_asc_obj
