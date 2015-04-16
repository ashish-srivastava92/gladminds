from base_smoke import BrandResourceTestCase
from gladminds.core.constants import CouponStatus
from integration.core.constants import BajajUrls
from integration.core.constants import DISPATCH_XML_DATA,PURCHASE_XML_DATA,SERVICE_ADVISOR_DATA,OLD_FSC_DATA\
,CREDIT_NOTE_DATA,CUSTOMER_DATA,ASC_DATA,SA_DATA,VIN_DATA,MOBILE_DATA

class UtilityResourceTest(BrandResourceTestCase):
    def send_dispatch_feed(self,xml_data=DISPATCH_XML_DATA):
        self.post_xml(data=xml_data, content_type='text/xml')
        url="v1/products/?product_id=12345678901232792"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="dealer_id",value="GMDEALER001",inner_parameter="dealer_id") 
    
    def send_purchase_feed(self,xml_data=PURCHASE_XML_DATA):
        self.send_dispatch_feed()
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
        self.post_as_dealer(uri=uri,data=data,isjson=False,username=username,password=password)
        url="v1/products/?product_id=12345678901232792"
        result = self.get(url)
        self.check_result(result=result['objects'][0],parameter="customer_phone_number",value="+917777777777")
    
    def search_vin(self,username,password):
        data=VIN_DATA
        uri="aftersell/exceptions/customer"
        result=self.post_as_dealer(uri=uri, username=username, password=password, data=data,isjson=False)
        return result
    
    def search_mobile(self,username,password):
        data=MOBILE_DATA
        uri="aftersell/exceptions/serviceadvisor"
        result=self.post_as_dealer(uri=uri,data=data,isjson=False,username=username,password=password)
        return result
    
    def register_sa(self,username,password,data=SA_DATA):
        uri="aftersell/register/sa"
        self.post_as_dealer(uri=uri,data=data,isjson=False,username=username,password=password)
    
    def register_asc(self,username,password):
        data=ASC_DATA
        uri="aftersell/register/asc"
        self.post_as_dealer(uri=uri,data=data,isjson=False,username=username,password=password)
    
    def get_sa_feed(self,phone,status=None):
        if status != None:
            url="v1/service-advisors/?user__phone_number__contains="+phone+"&status="+status
        else:
            url="v1/service-advisors/?user__phone_number__contains="+phone
        result=self.get(url)
        return result

    def check_coupon_open(self,unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.OPEN)
         
    def check_coupon_expired(self, unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.EXPIRED)
    
    def check_coupon_exceed_limit(self,unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.EXCEEDS_LIMIT)
        
    def check_coupon_inprogress(self,unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.IN_PROGRESS)
        
    def check_coupon_closed(self,unique_service_coupon):
        coupon = self.get(BajajUrls.COUPONS+'?unique_service_coupon='+unique_service_coupon)
        self.assertEqual(coupon['objects'][0]['status'], CouponStatus.CLOSED)
    
    def check_coupon(self,phone_number,data):
        data=(('text',data), ('phoneNumber',phone_number))
        coupon_data = self.post(BajajUrls.MESSAGES,isjson=False,data=data)
        self.assertTrue(coupon_data['status'])
    
    def check_coupon_false(self,phone_number,data):
        data=(('text',data), ('phoneNumber',phone_number))
        coupon_data = self.post(BajajUrls.MESSAGES,isjson=False,data=data)
        self.assertFalse(coupon_data['status'])     
        