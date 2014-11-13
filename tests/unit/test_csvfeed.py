from django.core.exceptions import ObjectDoesNotExist
import time

from base_unit import GladmindsUnitTestCase
from gladminds.bajaj.feeds import feed
from gladminds.bajaj import models as common


class CSVFeedTest(GladmindsUnitTestCase):
    def setUp(self):
        super(CSVFeedTest, self).setUp()
        self.timestamp = str(int(time.time()))
        timestamp = self.timestamp
        self.brand_feed = [{'brand_id':'BRAND001_'+timestamp, 'brand_name': 'BRANDNAME_'+timestamp, 'product_type': 'PRODUCTTYPE001_'+timestamp, 'product_name': 'PRODUCTNAME1_'+timestamp},
                      {'brand_id':'BRAND001_'+timestamp, 'brand_name': 'BRANDNAME_'+timestamp, 'product_type': 'PRODUCTTYPE002_'+timestamp, 'product_name': 'PRODUCTNAME2_'+timestamp}]
         
        self.brand_feed_2 = [{'brand_id':'BRAND001_'+timestamp, 'brand_name': 'BRANDNAME_'+timestamp, 'product_type': 'PRODUCTTYPE001_'+timestamp, 'product_name': 'PRODUCTNAME1_'+timestamp},
                      {'brand_id':'BRAND002_'+timestamp, 'brand_name': 'BRANDNAME2_'+timestamp, 'product_type': 'PRODUCTTYPE003_'+timestamp, 'product_name': 'PRODUCTNAME3_'+timestamp},
                      {'brand_id':'BRAND002_'+timestamp, 'brand_name': 'BRANDNAME2_'+timestamp, 'product_type': 'PRODUCTTYPE002_'+timestamp, 'product_name': 'PRODUCTNAME2_'+timestamp}]
     
    """Below test cases check the functionality of BRAND feed. We only test brand, other feed like dealer, product are tested in other test class"""
         
    def test_brandproducttypefeed(self):
        tmp=self.timestamp
        obj = feed.BrandProductTypeFeed(data_source = self.brand_feed)
        obj.import_data()
        producttype_data = common.ProductType.objects.get(product_type = 'PRODUCTTYPE001_'+tmp)
        self.assertEqual(producttype_data.product_name, 'PRODUCTNAME1_'+tmp, 'Product type not matched')
    
    def test_import_duplicate_feed(self):
        tmp=self.timestamp
        obj = feed.BrandProductTypeFeed(data_source = self.brand_feed_2)
        obj.import_data()
        producttype_data = common.ProductType.objects.get(product_type = 'PRODUCTTYPE003_'+tmp)
        self.assertEqual(producttype_data.product_name, 'PRODUCTNAME3_'+tmp, 'Product type not matched')
          
        #Check Duplicate
        producttype_data = common.ProductType.objects.filter(product_type = 'PRODUCTTYPE002_'+tmp)
        self.assertEqual(len(producttype_data), 1)
 
class CSVFeedByFile(GladmindsUnitTestCase):
    def setUp(self):
        super(CSVFeedByFile, self).setUp()
        feed.load_feed()
     
    def tearDown(self):
        from django.conf import settings
        import os
        from os import listdir
        from os.path import isfile, join
        file_path = settings.DATA_CSV_PATH
        only_file = [f for f in listdir(file_path) if isfile(join(file_path, f))]
        for filename in only_file:
            actual_file_name = filename.split('-')
            current_file_path = file_path + "/" + filename
            rename_to = file_path + "/" + actual_file_name[0]
            try:
                os.rename(current_file_path, rename_to)
            except OSError as oe:
                logger.exception("[Excpetion]: {0}".format(oe))
 
     
    def _test_brand_import(self):
        brand_data = common.Brand.objects.get(brand_id = 'HERO001')
        self.assertEqual(brand_data.brand_name, 'HERO')
 
    def _test_service_advisor(self):
        sa_data = common.ServiceAdvisor.objects.get(phone_number = '+SA0000000002')
        self.assertEqual(sa_data.dealer_id.dealer_id, 'TESTD001')
         
        sa_data = common.ServiceAdvisor.objects.get(phone_number = '+SA0000000003')
        self.assertEqual(sa_data.dealer_id.dealer_id, 'TESTD002')
 
    def _test_product_dispatch(self):
        product_data = common.ProductData.objects.get(vin = 'TESTDDZZZHER44300')
        self.assertEqual(product_data.product_type.product_type, 'IMPULSE220')
        self.assertEqual(product_data.dealer_id.dealer_id, 'TESTD001')
         
        coupon_count = common.CouponData.objects.filter(vin__vin = 'TESTDDZZZHER44300', status = 1).count()
        self.assertEqual(coupon_count, 2)
         
        coupon_count = common.CouponData.objects.filter(vin__vin = 'TESTDDZZZHER44301', status = 1).count()
        self.assertEqual(coupon_count, 1)
     
    def _test_product_purchases(self):
        product_data = common.ProductData.objects.get(vin = 'TESTDDZZZHER44300')
        self.assertEqual(product_data.customer_phone_number.phone_number, '+CUST000000001')
        self.assertEqual(product_data.sap_customer_id, 'SAPTESTCUST001')
         
        product_data = common.ProductData.objects.get(vin = 'TESTDDZZZHER44301')
        self.assertEqual(product_data.customer_phone_number.phone_number, '+CUST000000002')
        self.assertEqual(product_data.sap_customer_id, 'SAPTESTCUST002')
         
    def _test_coupon_redeeem(self):
        coupon_data = common.CouponData.objects.get(vin__vin = 'TESTDDZZZHER44300', unique_service_coupon = 'HEROCOUP001')
#         self.assertEqual(coupon_data.sa_phone_number.phone_number, '+SA0000000001')
        self.assertEqual(int(coupon_data.actual_kms), 100)
         
        coupon_data = common.CouponData.objects.get(vin__vin = 'TESTDDZZZHER44301', unique_service_coupon = 'BAJAJCOUP002')
#         self.assertEqual(coupon_data.sa_phone_number.phone_number, '+SA0000000002')
        self.assertEqual(int(coupon_data.actual_kms), 500)
     
    def _test_user_registration(self):
#         customer_data = common.GladMindUsers.objects.get(phone_number = '+CUST000000001')
#         self.assertEqual(customer_data.customer_name, 'Test Customer')   
          pass