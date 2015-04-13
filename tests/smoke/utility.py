from base_smoke import BrandResourceTestCase
from integration.core.constants import DISPATCH_XML_DATA,PURCHASE_XML_DATA,SERVICE_ADVISOR_DATA,OLD_FSC_DATA\
,CREDIT_NOTE_DATA,CUSTOMER_DATA,ASC_DATA,SA_DATA,EXISTING_SA_DATA,UPDATE_SA_DATA

class UtilityResourceTest(BrandResourceTestCase):
    def send_dispatch_feed(self):
        xml_data = DISPATCH_XML_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="v1/products/?product_id=12345678901232792"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="dealer_id",value="GMDEALER001",inner_parameter="dealer_id") 
    
    def send_purchase_feed(self):
        self.send_dispatch_feed()
        xml_data = PURCHASE_XML_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="v1/products/?product_id=12345678901232792"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="customer_name",value="TestU2927")
    
    def send_service_advisor_feed(self):
        xml_data=SERVICE_ADVISOR_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="v1/service-advisors/?service_advisor_id=GMDEALER001SA31"
        result=self.get(url)
        self.check_result(result=result['objects'][0],parameter="user",value="+911111111111",inner_parameter="phone_number")
    
    def send_old_fsc_feed(self):
        xml_data=OLD_FSC_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="v1/coupons/?product__product_id=12345678901232792&&service_type=2"
        result=self.get(url)
        self.check_result(result=result['objects'][0],parameter="status",value=6)
    
    def send_credit_note_feed(self):
        xml_data=CREDIT_NOTE_DATA
        self.post_xml(data=xml_data, content_type='text/xml')
        url="v1/coupons/?product__product_id=12345678901232792&&service_type=1"
        result=self.get(url)
        self.check_result(result=result['objects'][0],parameter="credit_note",value="Well Done")

    def register_customer(self,username,password):
        data=CUSTOMER_DATA
        uri="aftersell/register/customer"
        self.post_as_dealer(uri=uri,data=data,isjson="False",username=username,password=password)
        url="v1/products/?product_id=12345678901232792"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="customer_phone_number",value="+917777777777")
    
    def register_sa(self,username,password):
        data=SA_DATA
        ex_data=EXISTING_SA_DATA
        update_data=UPDATE_SA_DATA
        self.send_service_advisor_feed()
        uri="aftersell/register/sa"
        self.post_as_dealer(uri=uri,data=ex_data,isjson="False",username=username,password=password)
        url="v1/service-advisors/?user__phone_number__contains=1111111111&status=Y"
        result=self.get(url)
        self.assertEqual(result['objects'].__len__(),1)
        self.check_result(result=result['objects'][0],parameter="dealer",value="GMDEALER031",inner_parameter="dealer_id")
        self.post_as_dealer(uri=uri,data=update_data,isjson="False",username=username,password=password)
        url="v1/service-advisors/?service_advisor_id=GMDEALER001SA31"
        result=self.get(url)
        self.check_result(result=result['objects'][0],parameter="status",value="N")
        self.post_as_dealer(uri=uri,data=data,isjson="False",username=username,password=password)
        url="v1/service-advisors/?user__phone_number__contains=6767676767"
        result=self.get(url)
        self.check_result(result=result['objects'][0]['user'], value="SA29", parameter="user", inner_parameter="first_name")
    
    def register_asc(self,username,password):
        data=ASC_DATA
        uri="aftersell/register/asc"
        self.post_as_dealer(uri=uri,data=data,isjson="False",username=username,password=password)

        
        