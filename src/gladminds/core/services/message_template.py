from django.conf import settings
from gladminds.core.model_fetcher import models

def get_template(template_key):
    object = models.MessageTemplate.objects.get(template_key=template_key)
    return object.template

RCV_MESSAGE_FORMAT = "{key} {message}"

def get_message_template_mapper():
    return {
            settings.ALLOWED_KEYWORDS['register']: {
                           'receive': get_template('RCV_CUSTOMER_REGISTRATION'),
                           'send': get_template('SEND_CUSTOMER_REGISTER'),
                           'invalid': get_template('SEND_INVALID_MESSAGE'),
                           'handler': 'coupons.free_service_coupon.register_customer',
                           'auth_rule': ['open']
                                                   },
            settings.ALLOWED_KEYWORDS['service']:{
                           'receive':get_template('RCV_CUSTOMER_SERVICE_DETAIL'),
                           'send':get_template('SEND_CUSTOMER_SERVICE_DETAIL'),
                           'invalid':get_template('SEND_CUSTOMER_INVALID_CUSTOMER'),
                           'handler':'coupons.free_service_coupon.customer_service_detail',
                           'auth_rule': ['customer']
                           },
            settings.ALLOWED_KEYWORDS['check']:{
                         'receive': get_template('RCV_SA_COUPON_VALIDATION'),
                         'send':get_template('SEND_SA_VALID_COUPON'),
                         'invalid':get_template('SEND_SA_EXPIRED_COUPON'),
                         'handler':'coupons.free_service_coupon.validate_coupon',
                         'auth_rule': ['sa']
                         },
            settings.ALLOWED_KEYWORDS['close']:{
                            'receive': get_template('RCV_SA_COUPON_COMPLETE'),
                            'send':get_template('SEND_SA_CLOSE_COUPON'),
                            'invalid':get_template('SEND_INVALID_MESSAGE'),
                            'handler':'coupons.free_service_coupon.close_coupon',
                            'auth_rule': ['sa']
                            },
            settings.ALLOWED_KEYWORDS['brand']:{
                         'receive': get_template('RCV_CUSTOMER_BRAND_DATA'),
                         'send':get_template('SEND_BRAND_DATA'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'coupons.free_service_coupon.get_brand_data',
                        'auth_rule': ['open']
                         },
            settings.ALLOWED_KEYWORDS['customer_detail_recovery']:{
                        'receive': get_template('RCV_CUSTOMER_DETAILS'),
                        'send':get_template('SEND_CUSTOMER_DETAILS'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'coupons.free_service_coupon.send_customer_detail',
                        'auth_rule': ['open']
                         },
            settings.ALLOWED_KEYWORDS['service_desk']:{
                        'receive': get_template('RCV_USER_COMPLAINT'),
                        'send':get_template('SEND_RCV_FEEDBACK'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'service_desk.servicedesk_manager.save_feedback_ticket',
                        'auth_rule': ['open']
                        },
            settings.ALLOWED_KEYWORDS['accumulate_point']:{
                        'receive': get_template('RCV_ACCUMULATE_POINT'),
                        'send':get_template('SEND_ACCUMULATED_POINT'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'loyalty.loyalty.LoyaltyService.accumulate_point',
                        'auth_rule': ['open']
                        },
            settings.ALLOWED_KEYWORDS['check_point_balance']:{
                        'receive': get_template('RCV_CHK_BAL_POINT'),
                        'send':get_template('SEND_BALANCE_POINT'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'loyalty.loyalty.LoyaltyService.check_point_balance',
                        'auth_rule': ['open']
                        },
            settings.ALLOWED_KEYWORDS['redeem_point']:{
                        'receive': get_template('RCV_REDEEM_POINT'),
                        'send':get_template('SEND_REDEEM_POINT'),
                        'invalid':get_template('SEND_INVALID_MESSAGE'),
                        'handler':'loyalty.loyalty.LoyaltyService.redeem_point',
                        'auth_rule': ['open']
                        }
            }
