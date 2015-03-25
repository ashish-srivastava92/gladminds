from base_smoke import BajajResourceTestCase
from integration.core.constants import DISPATCH_XML_DATA,PURCHASE_XML_DATA,SERVICE_ADVISOR_DATA

class FeedsResourceTest(BajajResourceTestCase):
    def send_dispatch_feed(self):
        xml_data = DISPATCH_XML_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="products/?product_id=12345678901234565"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="dealer_id",value="GMDEALER001",inner_parameter="dealer_id") 
    
    def send_purchase_feed(self):
        self.send_dispatch_feed()
        xml_data = PURCHASE_XML_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="products/?product_id=12345678901234565"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="customer_name",value="TestCustomer")
    
    def send_service_advisor_feed(self):
        xml_data=SERVICE_ADVISOR_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="service-advisors/?service_advisor_id=GMDEALER001SA31"
        result=self.get(url)
        self.check_result(result=result['objects'][0],parameter="user",value="+911111111111",inner_parameter="phone_number")