import json
import requests
from django.test.testcases import TestCase
import os
from smoke.base_smoke import BajajResourceTestCase
from integration.core.constants import DISPATCH_XML_DATA,PURCHASE_XML_DATA

class TestFeeds(BajajResourceTestCase):
        
    def test_product_dispatch(self):
        xml_data = DISPATCH_XML_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="products/1/"
        result = self.get(url)
        self.check_result(result,"product_id","XXXXXXXXXX")
    
    def test_product_purchase(self):
        self.test_product_dispatch()
        xml_data = PURCHASE_XML_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="products/1/"
        result = self.get(url)
        self.check_result(result,"customer_name","TestCustomer")
    
    
    
    