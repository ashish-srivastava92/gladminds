from django.core.exceptions import ObjectDoesNotExist
from gladminds.models import common

def get_template(template_key):
    object = common.MessageTemplate.objects.get(template_key = template_key)
    return object.template

RCV_MESSAGE_FORMAT = "{key} {message}"



MESSAGE_TEMPLATE_MAPPER = {
            'gcp_reg':{
                       'receive':get_template('RCV_CUSTOMER_REGISTRATION'),
                       'send':get_template('SEND_CUSTOMER_REGISTER'),
                       'invalid':get_template('SEND_INVALID_MESSAGE'),
                       'handler':'register_customer',
                       'auth_rule': ['open']
                       },
            'service':{
                       'receive':get_template('RCV_CUSTOMER_SERVICE_DETAIL'),
                       'send':get_template('SEND_CUSTOMER_SERVICE_DETAIL'),
                       'invalid':get_template('SEND_CUSTOMER_INVALID_CUSTOMER'),
                       'handler':'customer_service_detail',
                       'auth_rule': ['customer']
                       },
            'check':{
                     'receive': get_template('RCV_SA_COUPON_VALIDATION'),
                     'send':get_template('SEND_SA_VALID_COUPON'),
                     'invalid':get_template('SEND_SA_EXPIRED_COUPON'),
                     'handler':'validate_coupon',
                     'auth_rule': ['sa']
                     },
            'close':{
                        'receive': get_template('RCV_SA_COUPON_COMPLETE'),
                        'send':get_template('SEND_SA_CLOSE_COUPON'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'close_coupon',
                        'auth_rule': ['sa']
                        },
            'brand':{
                     'receive': get_template('RCV_CUSTOMER_BRAND_DATA'),
                     'send':get_template('SEND_BRAND_DATA'),
                    'invalid':get_template('SEND_INVALID_MESSAGE'),
                    'handler':'get_brand_data',
                    'auth_rule': ['open']
                     }
        }
