import json
import requests
from django.test.testcases import TestCase
import os
from smoke.utility import FeedsResourceTest

class TestFeeds(FeedsResourceTest):
        
    def test_product_dispatch(self):
        self.send_dispatch_feed()        
    
    def test_product_purchase(self):
        self.send_dispatch_feed()
        self.send_purchase_feed()
    
    def test_service_advisor_feed(self):
        self.send_service_advisor_feed()

    
    
    