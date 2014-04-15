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
        coupon_obj = common.CouponData(unique_service_coupon=kwargs['unique_service_coupon']\
                                       , actual_service_date=kwargs.get('actual_service_date', None), vin=kwargs['product_data']\
                                       , valid_days=kwargs['valid_days'], valid_kms=kwargs['valid_kms']\
                                       , service_type=kwargs['service_type'], status=kwargs['status'], mark_expired_on=kwargs['mark_expired_on'])
        coupon_obj.save()
        return coupon_obj

    def get_product_obj(self, **kwargs):
        product_data = common.ProductData(
                    vin=kwargs['vin'], product_type=kwargs['producttype_data'], dealer_id=kwargs['dealer_data'], customer_phone_number=kwargs['customer_phone_number'], sap_customer_id=kwargs['sap_customer_id'])
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
        service_advisor_obj = common.ServiceAdvisor(service_advisor_id=kwargs[
                                    'service_advisor_id'], name=kwargs['name'], phone_number=kwargs['phone_number'])
        service_advisor_obj.save()
        return service_advisor_obj

    def get_dealer_service_advisor_obj(self, **kwargs):
        dealer_service_advisor_obj = common.ServiceAdvisorDealerRelationship(dealer_id=kwargs['dealer_data'], service_advisor_id=kwargs[
                                    'service_advisor_id'], status=kwargs['status'])
        dealer_service_advisor_obj.save()
        return dealer_service_advisor_obj

    def get_customer_obj(self, **kwargs):
        customer_obj = common.GladMindUsers(phone_number=kwargs['phone_number'])
        customer_obj.save()
        return customer_obj
    
    def filter_coupon_obj(self, coupon_id=None):
        coupon_obj = common.CouponData.objects.filter(unique_service_coupon=coupon_id)
        return coupon_obj[0]
        