from smoke.utility import UtilityResourceTest

class TestFeeds(UtilityResourceTest):
        
    def test_product_dispatch(self):
        self.send_dispatch_feed()        
    
    def test_product_purchase(self):
        self.send_dispatch_feed()
        self.send_purchase_feed()
    
    def test_service_advisor_feed(self):
        self.send_service_advisor_feed()

    def test_old_fsc_feed(self):
        self.send_dispatch_feed()
        self.send_old_fsc_feed()
    
    def test_credit_note_feed(self):
        self.send_dispatch_feed()
        self.send_purchase_feed()
        self.send_credit_note_feed()
    
    
    