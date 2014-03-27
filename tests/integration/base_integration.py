from tastypie.test import ResourceTestCase
from django.core import management
from gladminds.models import common
import os
from django.conf import settings
import json


class GladmindsResourceTestCase(ResourceTestCase):

    def setUp(self):
        super(GladmindsResourceTestCase, self).setUp()
        file_path = os.path.join(settings.BASE_DIR, 'etc/data/template.json')
        message_templates = json.loads(open(file_path).read())
        for message_temp in message_templates:
            fields = message_temp['fields']
            temp_obj = common.MessageTemplate(template_key=fields['template_key']\
                       , template=fields['template'], description=fields['description'])
            temp_obj.save()


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
        coupon_obj = common.CouponData(unique_service_coupon=kwargs['unique_service_coupon'],
                                vin=kwargs['product_data'], valid_days=kwargs['valid_days'], valid_kms=kwargs['valid_kms'], service_type=kwargs['service_type'], status='1')
        coupon_obj.save()
        return coupon_obj

    def get_product_obj(self, **kwargs):
        product_data = common.ProductData(
                    vin=kwargs['vin'], product_type=kwargs['producttype_data'], dealer_id=kwargs['dealer_data'], customer_phone_number=kwargs['customer_phone_number'])
        product_data.save()
        return product_data

    def get_delear_obj(self, **kwargs):
        delear_data = common.RegisteredDealer(dealer_id=kwargs['dealer_id'])
        delear_data.save()
        return delear_data

    def get_product_type_obj(self, **kwargs):
        product_type_data_obj = common.ProductTypeData(brand_id=kwargs['brand_id'], product_name=kwargs['product_name'], product_type=kwargs['product_type'])
        product_type_data_obj.save()
        return product_type_data_obj

    def get_brand_obj(self, **kwargs):
        brand_obj = common.BrandData(
                    brand_id=kwargs['brand_id'], brand_name=kwargs['brand_name'])
        brand_obj.save()
        return brand_obj

    def get_service_advisor_obj(self, **kwargs):
        service_advisor_obj = common.ServiceAdvisor(dealer_id=kwargs['dealer_data'], service_advisor_id=kwargs[
                                    'service_advisor_id'], name=kwargs['name'], phone_number=kwargs['phone_number'], status=kwargs['status'])
        service_advisor_obj.save()
        return service_advisor_obj

    def get_customer_obj(self, **kwargs):
        customer_obj = common.GladMindUsers(phone_number=kwargs['phone_number'])
        customer_obj.save()
        return customer_obj
        
        
        