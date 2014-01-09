from django.db import models
from django.conf.urls import url
from tastypie.resources import Resource
from gladminds import utils,  message_template as templates
from gladminds.models import common
from gladminds.tasks import send_message


HANDLER_MAPPER = {
                  'reg':'register_customer',
                  'service': 'customer_service_detail',
                  'product': 'register_product_for_customer'
                  }

class GladmindsResources(Resource):    
    class Meta:
        resource_name = 'messages'
    
    def base_urls(self):
        return [
            url(r"^messages$", self.wrap_view('dispatch_gladminds'))
            ]   
    
    def dispatch_gladminds(self, request, **kwargs):
        message = request.body
        handler_str, attr_list = self.parse_message(message)
        handler = getattr(self, handler_str, None)
        to_be_serialized = handler(attr_list)
        to_be_serialized = {"status": to_be_serialized}
        return self.create_response(request, data = to_be_serialized)
    
    def parse_message(self, message):
        attr_list = message.split()
        print attr_list
        action = attr_list[0]
        if action:
            action = action.lower()
            
        return (HANDLER_MAPPER.get(action, None), attr_list)
    
    def register_customer(self, attr_list):
        phone_number = int(attr_list[1])
        try:
            object = common.Customer.objects.get(phone_number=phone_number)
            customer_id = object.__dict__['customer_id']
        except Exception as ex:
            customer_id = utils.generate_unique_customer_id()
            cust = common.Customer(customer_id = customer_id, phone_number = phone_number)
            cust.save()
        message = templates.CUSTOMER_REGISTER.format(customer_id)
        send_message.delay(phone_number=phone_number, message=message)
        return True
        
    
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

    def determine_format(self, request):
        return 'application/json'