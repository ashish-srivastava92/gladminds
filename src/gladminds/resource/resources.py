from django.db import models
from django.conf.urls import url
from tastypie.resources import Resource
from gladminds import utils,  message_template as templates
from gladminds.models import common
from gladminds import smsparser
from gladminds.tasks import send_registration_detail, send_service_detail, send_reminder_message, send_coupon_close_message
from datetime import datetime
from django.db import connection
from src.gladminds.tasks import send_coupon_close_message
__all__ = ['GladmindsTaskManager']

HANDLER_MAPPER = {
    'gcp_reg': 'register_customer',
    'service': 'customer_service_detail',
    'check': 'validate_coupon',
    'complete': 'close_coupon'
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
        message = templates.SEND_CUSTOMER_REGISTER.format(customer_name)
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
            message = templates.SEND_CUSTOMER_SERVICE_DETAIL.format(
                gladmind_customer_id, vin, service_code)
        except Exception as ex:
            message = templates.INVALID_SERVICE_DETAIL.format(
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

    def validate_coupon(self, attr_list, phone_number):
        if self.validate_dealer(phone_number):
            product_id = attr_list[1]
            actual_kms = int(attr_list[2])
            unique_service_coupon = attr_list[3]
            message = None
            try:
                customer_data = common.CustomerData.objects.filter(
                    product_id=product_id)
                customer_data_object = common.CustomerData.objects.get(
                    unique_service_coupon=unique_service_coupon)
                if customer_data_object.is_expired or customer_data_object.is_closed:
                    count = 0
                    for data in customer_data:
                        if data.unique_service_coupon == unique_service_coupon:
                            count = count + 1
                            break
                        else:
                            count = count + 1
                    new_unique_service_coupon = customer_data[
                        count].unique_service_coupon
                    message = templates.EXPIRED_COUPON.format(
                        new_unique_service_coupon, unique_service_coupon)
                else:
                    valid_kms = customer_data_object.valid_kms
                    if (actual_kms > valid_kms):
                        count = 0
                        for data in customer_data:
                            if data.unique_service_coupon == unique_service_coupon:
                                count = count + 1
                                break
                            else:
                                count = count + 1
                        new_unique_service_coupon = customer_data[
                            count].unique_service_coupon
                        customer_data_object.is_expired = True
                        customer_data_object.save()
                        message = templates.EXPIRED_COUPON.format(
                            new_unique_service_coupon, unique_service_coupon)
                    else:
                        message = templates.VALID_COUPON.format(
                            unique_service_coupon)
            except Exception as ex:
                message = templates.INVALID_COUPON_DETAIL.format(
                    unique_service_coupon)
            send_service_detail.delay(phone_number='dealer', message=message)
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

    def close_coupon(self, attr_list, phone_number):
        if self.validate_dealer(phone_number):
            product_id = attr_list[1]
            unique_service_coupon = attr_list[2]
            message = None
            try:
                customer_data_object = common.CustomerData.objects.get(
                    unique_service_coupon=unique_service_coupon)
                customer_data_object.is_closed = True
                customer_data_object.save()
                message = templates.SA_CLOSE_COUPON
            except:
                return False
        else:
            return False
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

    def determine_format(self, request):
        return 'application/json'
