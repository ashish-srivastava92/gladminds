from django.db import models
from django.conf.urls import url
from tastypie.resources import Resource
from gladminds import utils,  message_template as templates
from gladminds.models import common
from gladminds.tasks import send_registration_detail,send_service_detail
from datetime import datetime

HANDLER_MAPPER = {
                  'reg':'register_customer',
                  'service': 'customer_service_detail',
                  'check':'validate_coupon'
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
            object = common.GladMindUsers.objects.get(phone_number=phone_number)
            gladmind_customer_id = object.__dict__['gladmind_customer_id']
        except Exception as ex:
            gladmind_customer_id = utils.generate_unique_customer_id()
            registration_date=datetime.now()
            cust = common.GladMindUsers(gladmind_customer_id =gladmind_customer_id, phone_number = phone_number
                                        ,registration_date=registration_date)
            cust.save()
        message = templates.CUSTOMER_REGISTER.format(gladmind_customer_id)
        send_registration_detail.delay(phone_number=phone_number, message=message)
        
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
        gladmind_customer_id = attr_list[1]
        phone_number = None
        message = None
        try:
            customer_object = common.GladMindUsers.objects.get(gladmind_customer_id = gladmind_customer_id)
            phone_number = customer_object.__dict__['phone_number']
            object = common.CustomerData.objects.filter(phone_number__phone_number=phone_number)
            product_id =object[0].product_id
            service_code=' ,'.join(data.unique_service_code +" Expiry Days "+str(data.valid_days)
                                   +" Valid KMS "+str(data.valid_kms) for data in object if data.product_id==product_id)
            message = templates.SERVICE_DETAIL.format(gladmind_customer_id, product_id, service_code)
        except Exception as ex:
            message = templates.INVALID_SERVICE_DETAIL.format(gladmind_customer_id)
        send_service_detail.delay(phone_number=phone_number, message=message)
        kwargs = {
                    'action':'SEND TO QUEUE',
                    'reciever': '55680',
                    'sender':str(phone_number),
                    'message': message,
                    'status':'success'
                  }
        
        utils.save_log(**kwargs)
        return True
    
    
    def validate_coupon(self, attr_list):
        unique_service_coupon = attr_list[1]
        actual_kms = int(attr_list[2])
        message = None
        try:
            customer_data_object = common.CustomerData.objects.get(unique_service_coupon = unique_service_coupon)
            if customer_data_object.is_expired:
                message = templates.EXPIRED_COUPON.format(unique_service_coupon)
            else:
                valid_kms=customer_data_object.valid_kms
                if (actual_kms>valid_kms):
                    message = templates.EXPIRED_COUPON.format(unique_service_coupon)
                else:
                    message = templates.VALID_COUPON.format(unique_service_coupon)
        except Exception as ex:
            message = templates.INVALID_COUPON_DETAIL.format(unique_service_coupon)
        send_service_detail.delay(phone_number='dealer', message=message)
        kwargs = {
                    'action':'SEND TO QUEUE',
                    'reciever': '55680',
                    'sender':'dealer',
                    'message': message,
                    'status':'success'
                  }
        
        utils.save_log(**kwargs)
        return True
    
    def determine_format(self, request):
        return 'application/json'
    

class GladmindsTaskManager(object):
    
    def get_customers_to_send_reminder(self):
        
        pass
    
    def import_data_from_sap(self):
        pass
