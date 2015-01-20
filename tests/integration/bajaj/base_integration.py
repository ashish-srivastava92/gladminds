import os
import json

from django.conf import settings
from django.test.client import Client
from tastypie.test import ResourceTestCase
from django.core import management
from django.contrib.auth.models import User
from gladminds.management.commands import load_gm_migration_data, service_setup
from gladminds.bajaj import models
from integration.core.base_integration import CoreResourceTestCase

client  =  Client(SERVER_NAME='bajaj')

class BrandResourceTestCase(CoreResourceTestCase):
    multi_db=True

    def setUp(self):
        super(BrandResourceTestCase, self).setUp()
        load_email_obj = load_gm_migration_data.Command()
        load_email_obj.add_email_template()
        load_email_obj.add_sms_template()
        load_email_obj.add_group()
        load_services = service_setup.Command()
        load_services.create_service_types()
        load_services.create_services()
        load_services.create_industries()
        load_services.create_brands()
        load_services.create_brands_services()
        
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
        coupon_obj = models.CouponData(**kwargs)
        coupon_obj.save()
        return coupon_obj

    def get_product_obj(self, **kwargs):
        product_data = models.ProductData(**kwargs)
        product_data.save()
        return product_data
    
    def create_user_profile(self, **kwargs):
        name = kwargs.get('name', None)
        phone_number = kwargs.get('phone_number', None)
        user_obj = User(username=name, first_name=name)
        user_obj.save(using='bajaj')
        user_profile_obj = models.UserProfile(user=user_obj, phone_number=phone_number)
        user_profile_obj.save(using='bajaj')
        return user_profile_obj

    def get_delear_obj(self, **kwargs):
        dealer_obj =  models.Dealer(user=self.create_user_profile(**kwargs))
        dealer_obj.save()
        return dealer_obj

    def get_product_type_obj(self, **kwargs):
        product_type_data_obj = models.ProductType(**kwargs)
        product_type_data_obj.save()
        return product_type_data_obj

    def get_brand_obj(self, **kwargs):
        #brand_obj = models.Brand(**kwargs)
        #brand_obj.save()
        #return brand_obj
        return None

    def get_service_advisor_obj(self, **kwargs):
        service_advisor_id = kwargs.get('service_advisor_id', None)
        status = kwargs.get('status', 'Y')
        user_profile_obj = self.create_user_profile(**kwargs)
        service_advisor_obj = models.ServiceAdvisor(user=user_profile_obj, 
                                                     status=status, service_advisor_id=service_advisor_id)
        service_advisor_obj.save()
        return service_advisor_obj
    
    def get_dealer_service_advisor_obj(self, **kwargs):
#         dealer_service_advisor_obj = models.ServiceAdvisorDealerRelationship(**kwargs)
#         dealer_service_advisor_obj.save()
#         return dealer_service_advisor_obj
         return None

    def get_customer_obj(self, **kwargs):
        #customer_obj = models.GladMindUsers(**kwargs)
        #customer_obj.save()
        return None

    def filter_coupon_obj(self, coupon_id=None):
        coupon_obj = models.CouponData.objects.filter(unique_service_coupon=coupon_id)
        return coupon_obj[0]

    def get_temp_customer_obj(self, **kwargs):
        temp_customer_obj = models.CustomerTempRegistration.objects.get(**kwargs)
        return temp_customer_obj

    def get_temp_asc_obj(self, **kwargs):
        temp_asc_obj = models.ASCTempRegistration.objects.get(**kwargs)
        return temp_asc_obj
