from smoke.utility import UtilityResourceTest
from integration.core.constants import EXISTING_SA_DATA,UPDATE_SA_DATA

class TestRegistrations(UtilityResourceTest):
    def test_register_customer(self):
        self.send_dispatch_feed()
        self.register_customer("10316", "123")
        self.get_sa_feed(phone="1111111111")
    
    def test_register_sa(self):
        self.register_sa("10316","123")
        result=self.get_sa_feed(phone="6767676767")
        self.check_result(result=result['objects'][0]['user'], value="SA29", parameter="user", inner_parameter="first_name")
    
    def test_register_existing_sa(self):
        self.send_service_advisor_feed()
        self.register_sa("10316","123",data=EXISTING_SA_DATA)
        result=self.get_sa_feed(phone="1111111111",status="Y")
        self.assertEqual(result['objects'].__len__(),1)
        self.check_result(result=result['objects'][0],parameter="dealer",value="GMDEALER031",inner_parameter="dealer_id")
    
    def test_register_update_sa(self):
        self.send_service_advisor_feed()
        self.register_sa("10316","123",data=UPDATE_SA_DATA)
        result=self.get_sa_feed(phone="1111111111")
        self.check_result(result=result['objects'][0],parameter="status",value="N")
        
    
    def test_register_asc(self):
        self.register_asc("10316","123")