from django.db import models
from django.conf.urls import url
from tastypie.resources import Resource
from gladminds import utils,  message_template as templates
from gladminds.models import common
from gladminds.tasks import send_message
from datetime import datetime


HANDLER_MAPPER = {
                  'reg':'register_customer',
                  'service': 'customer_service_detail',
                  }

class GladmindsResources(Resource):    
    class Meta:
        resource_name = 'messages'
    
    def base_urls(self):
        return [
            url(r"^messages$", self.wrap_view('dispatch_gladminds'))
            ]   
    
    def dispatch_gladminds(self, request, **kwargs):
        if request.POST.get('text'):
            message=request.POST.get('text')
        else:
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
        
        kwargs = {
                    'action':'SEND TO QUEUE',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        
        utils.save_log(**kwargs)
        return True

    def customer_service_detail(self, attr_list):
        customer_id = attr_list[1]
        phone_number = None
        message = None
        try:
            customer_object = common.Customer.objects.get(customer_id = customer_id)
            phone_number = customer_object.__dict__['customer_id']
            object = common.ProductPurchased.objects.get(customer_id = customer_id)
            product_id = object.product_id
            service_object = common.Service.objects.filter(product__product_id = product_id)
            service_code=' ,'.join(object.__dict__['unique_service_code'] +" Expiry Duration "+ object.__dict__['expiry_time'] for object in service_object)
            message = templates.SERVICE_DETAIL.format(customer_id, product_id, service_code)
        except Exception as ex:
            message = templates.INVALID_SERVICE_DETAIL.format(customer_id)
        send_message.delay(phone_number=phone_number, message=message)
        kwargs = {
                    'action':'SEND TO QUEUE',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        
        utils.save_log(**kwargs)
        return True

    def determine_format(self, request):
        return 'application/json'