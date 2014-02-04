from gladminds import feed
from gladminds.models import common
from django.core.exceptions import ObjectDoesNotExist
from base_unit import GladmindsUnitTestCase
import time

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
    
    
    def test_brandproducttypefeed(self):
        tmp=self.timestamp
        obj = feed.BrandProductTypeFeed(data_source = self.brand_feed)
        obj.import_data()
        brand_data = common.BrandData.objects.get(brand_id = 'BRAND001_'+tmp)
        self.assertEqual(brand_data.brand_name, 'BRANDNAME_'+tmp, 'brand name not matched')
        producttype_data = common.ProductTypeData.objects.get(product_type = 'PRODUCTTYPE001_'+tmp)
        self.assertEqual(producttype_data.product_name, 'PRODUCTNAME1_'+tmp, 'Product type not matched')
        self.assertEqual(producttype_data.brand_id.brand_id, 'BRAND001_'+tmp, 'Brand Id is not matched in product type')
    
    def test_import_duplicate_feed(self):
        tmp=self.timestamp
        obj = feed.BrandProductTypeFeed(data_source = self.brand_feed_2)
        obj.import_data()
        brand_data = common.BrandData.objects.get(brand_id = 'BRAND002_'+tmp)
        self.assertEqual(brand_data.brand_name, 'BRANDNAME2_'+tmp, 'brand name not matched')
        producttype_data = common.ProductTypeData.objects.get(product_type = 'PRODUCTTYPE003_'+tmp)
        self.assertEqual(producttype_data.product_name, 'PRODUCTNAME3_'+tmp, 'Product type not matched')
        self.assertEqual(str(producttype_data.brand_id), 'BRAND002_'+tmp, 'Brand Id is not matched in product type')
        
        #Check Duplicate
        brand_data = common.BrandData.objects.get(brand_id = 'BRAND002_'+tmp)
        producttype_data = common.ProductTypeData.objects.filter(brand_id = brand_data, product_type = 'PRODUCTTYPE002_'+tmp)
        self.assertEqual(len(producttype_data), 0)
    
    def test_dealer_sa_feed(self):
        pass
    
    def test_product_dispatch_feed(self):
        pass
    
    def test_product_purchases_feed(self):
        pass
        
        
        
    