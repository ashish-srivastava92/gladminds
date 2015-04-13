from smoke.utility import UtilityResourceTest

class TestRegistrations(UtilityResourceTest):
    def test_register_customer(self):
        self.send_dispatch_feed()
        self.register_customer("10316", "123")
    
    def test_register_sa(self):
        self.register_sa("10316","123")
    
    def test_register_asc(self):
        self.register_asc("10316","123")