from django.db import models
from tastypie.resources import Resource
from models import common 
import utils
import message_template as templates 


HANDLER_MAPPER = {
                  'reg':'register_customer',
                  'service': 'customer_service_detail',
                  'product': 'register_product_for_customer'
                  }

class GladmindsResources(Resource):
    
    class META:
        resource_name = 'messages'
        
    def __init__(self):
        Resource.__init__();
    
    def base_urls(self):
        return [
            url(r"^messages$", self.wrap_view('dispatch_handler'), kwargs={'handler': self.get_patients})
            ]   
    
    def dispatch_handler(self, request):
        message = request.body
        handler_str = parse_message(message)
        handler, attr_list = getattr(self, handler, None)
        handler(attr_list)
    
    def parse_message(self, message):
        attr_list = message.split()
        action = data[0]
        return (HANDLER_MAPPER[action], attr_list)
    
    def register_customer(self, attr_list):
        mobile_number = attr_list[1]
        #TODO: Verify this number from DB
        customer_id = utils.generate_unique_customer_id()
        return templates.CUSTOMER_REGISTER.format(customer_id)
    
    def register_product_for_customer(self, attr_list):
        customer_id = attr_list[1]
        product_id = attr_list[0]
        #Register the product into DB
        return templates.REGISTER_PRODUCT(product_id, customer_id)
        
    
    def customer_service_detail(self, attr_list):
        customer_id = attr_list[1]
        #Retrive the service list for customer
        product_id = ""
        service_detail = []
        return templates.SERVICE_DETAIL.format(customer_id, product_id, service_detail)
