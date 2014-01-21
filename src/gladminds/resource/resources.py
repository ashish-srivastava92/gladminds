from django.db import models
from django.conf.urls import url
from tastypie.resources import Resource
from gladminds import utils,  message_template as templates
from gladminds.models import common
from gladminds import smsparser
from gladminds.tasks import send_registration_detail, send_service_detail,send_reminder_message, send_coupon_close_message,send_coupon_detail_customer,send_brand_sms_customer,send_close_sms_customer
from datetime import datetime
from django.db import connection
from src.gladminds.tasks import send_coupon_close_message
__all__ = ['GladmindsTaskManager']

class GladmindsResources(Resource):

    class Meta:
        resource_name = 'messages'

    def base_urls(self):
        return [
            url(r"^messages$", self.wrap_view('dispatch_gladminds'))
        ]

    def dispatch_gladminds(self, request, **kwargs):
        if request.POST.get('text'):
            message = request.POST.get('text')
            phone_number = request.POST.get('phoneNumber')
        else:
            message = request.body
        sms_dict = smsparser.sms_parser(message=message)
        handler = getattr(self, sms_dict['handler'], None)
        to_be_serialized = handler(sms_dict, phone_number)
        to_be_serialized = {"status": to_be_serialized}
        return self.create_response(request, data=to_be_serialized)

    def parse_message(self, message):
        attr_list = message.split()
        print attr_list
        action = attr_list[0]
        if action:
            action = action.lower()
        return (HANDLER_MAPPER.get(action, None), attr_list)

    def register_customer(self, sms_dict, phone_number):
        customer_name = sms_dict['name']
        email_id = sms_dict['email_id']
        try:
            object = common.GladMindUsers.objects.get(
                phone_number=phone_number)
            gladmind_customer_id = object.__dict__['gladmind_customer_id']
        except Exception as ex:
            gladmind_customer_id = utils.generate_unique_customer_id()
            registration_date = datetime.now()
            cust = common.GladMindUsers(
                gladmind_customer_id=gladmind_customer_id,
                phone_number=phone_number,
                customer_name=customer_name,
                email_id=email_id,
                registration_date=registration_date)
            cust.save()
        message = templates.get_template('SEND_CUSTOMER_REGISTER').format(customer_name)
        send_registration_detail.delay(
            phone_number=phone_number, message=message)

        kwargs = {
            'action': 'SEND TO QUEUE',
            'reciever': '55680',
            'sender': str(phone_number),
            'message': message,
            'status': 'success'
        }

        utils.save_log(**kwargs)
        return True

    def customer_service_detail(self, sms_dict, phone_number):
        gladmind_customer_id = sms_dict['customer_id']
        message = None
        try:
            gladmind_user_object=common.GladMindUsers.objects.get(gladmind_customer_id=gladmind_customer_id)
            phone_number=str(gladmind_user_object)
            customer_object = common.CustomerData.objects.filter(
                phone_number__phone_number=phone_number)
            # FIXME: RIGHT NOW HANDLING FOR ONE PRODUCT ONLY
            vin = customer_object[0].vin
            coupon_object = common.CouponData.objects.filter(
                vin__vin=vin, status=1)
            service_code = ''.join(coupon_object[0].unique_service_coupon + 
                                       " Valid Days " + str(coupon_object[0].valid_days)
                                       + " Valid KMS " + str(coupon_object[0].valid_kms))
            message = templates.get_template('SEND_CUSTOMER_SERVICE_DETAIL').format(
                gladmind_customer_id, vin, service_code)
        except Exception as ex:
            message = templates.get_template('INVALID_SERVICE_DETAIL').format(
                gladmind_customer_id)
        send_service_detail.delay(phone_number=phone_number, message=message)
        kwargs = {
            'action': 'SEND TO QUEUE',
            'reciever': '55680',
            'sender': str(phone_number),
            'message': message,
            'status': 'success'
        }
        utils.save_log(**kwargs)
        return True

    def validate_coupon(self,sms_dict, phone_number):
        if self.validate_dealer(phone_number):
            vin = sms_dict['vin']
            actual_kms = int(sms_dict['kms'])
            service_type= sms_dict['service_type']
            message = None
            customer_message=None
            try:
                coupon_data=common.CouponData.objects.get(vin__vin=vin,service_type=service_type)
                if coupon_data.status!=1 or actual_kms>coupon_data.valid_kms:
                    next_coupon=common.CouponData.objects.filter(
                    vin__vin=vin,service_type__gt=coupon_data.service_type)[:1].get()
                    if coupon_data.status == 2:
                        pass
                    else:
                        coupon_data.status=3
                    coupon_data.save()
                    message = templates.get_template('SEND_SA_EXPIRED_COUPON').format(
                        next_coupon.service_type, service_type)
                    customer_message = templates.get_template('SEND_CUSTOMER_EXPIRED_COUPON').format(
                        coupon_data.unique_service_coupon, service_type,
                        next_coupon.unique_service_coupon,next_coupon.service_type)
                else:
                    message = templates.get_template('SEND_SA_VALID_COUPON').format(
                            service_type)
                    customer_message = templates.get_template('SEND_CUSTOMER_VALID_COUPON').format(
                            coupon_data.unique_service_coupon,service_type)
                    
            except Exception as ex:
                message = templates.get_template('SEND_INVALID_MESSAGE').format(
                    service_type)
            send_service_detail.delay(phone_number='dealer', message=message)
            send_coupon_detail_customer.delay(phone_number='dealer',
                                                           message=customer_message)
            kwargs = {
                'action': 'SEND TO QUEUE',
                'reciever': '55680',
                'sender': 'dealer',
                'message': message,
                'status': 'success'
            }

            utils.save_log(**kwargs)
            return True
        else:
            return False

    def close_coupon(self, sms_dict, phone_number):
        if self.validate_dealer(phone_number):
            vin = sms_dict['vin']
            unique_service_coupon = sms_dict['usc']
            message = None
            customer_message=None
            try:
                coupon_object = common.CouponData.objects.get(
                    vin__vin=vin,unique_service_coupon=unique_service_coupon)
                coupon_object.status = 2
                all_previous_coupon=common.CouponData.objects.filter(
                    vin__vin=vin,service_type__lt=coupon_object.service_type).update(status=3)
                coupon_object.save()
                message = templates.get_template('SEND_SA_CLOSE_COUPON')
                service_advisor_object=common.ServiceAdvisor.objects.get(phone_number=phone_number)
                customer_message=templates.get_template('SEND_CUSTOMER_CLOSE_COUPON').format(
                                    vin,service_advisor_object.name,phone_number)
            except:
                return False
        else:
            return False
        send_close_sms_customer.delay(phone_number='GCS',message=customer_message)
        send_coupon_close_message.delay(phone_number='dealer', message=message)
        kwargs = {
            'action': 'SEND TO QUEUE',
            'reciever': '55680',
            'sender': str(phone_number),
            'message': message,
            'status': 'success'
        }

        utils.save_log(**kwargs)
        return True

    def validate_dealer(self, phone_number):
        try:
            service_advisor_object = common.ServiceAdvisor.objects.get(
                phone_number=phone_number)
        except:
            return False
        return True
    
    def get_brand_data(self, sms_dict, phone_number):
        brand_id = sms_dict['brand_id']
        try:
            product_object=common.ProductData.objects.filter(
                    brand__brand_id=brand_id)
            customer_object=common.CustomerData.objects.filter(
                phone_number__phone_number=phone_number)
            valid_customer_data=filter(lambda x: x.product in product_object,customer_object)
            product_sap_id_vin=map(lambda x: {'sap_id':x.sap_customer_id,'vin':x.vin},valid_customer_data)
            brand_message=','.join("customer_id "+ data['sap_id']+" vin "+data['vin'] for data in product_sap_id_vin)
            
            message = templates.get_template('SEND_BRAND_DATA').format(brand_message)
            
        except Exception as ex:
            message=templates.get_template('SEND_INVALID_MESSAGE')
            
        send_brand_sms_customer.delay(phone_number='GCS',message=message)
        kwargs = {
            'action': 'SEND TO QUEUE',
            'reciever': '55680',
            'sender': str(phone_number),
            'message': message,
            'status': 'success'
        }

        utils.save_log(**kwargs)
        return True


    def determine_format(self, request):
        return 'application/json'
