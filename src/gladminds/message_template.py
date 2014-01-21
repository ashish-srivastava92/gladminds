from gladminds.models import common

#MESSAGE TEMPLATE SEND TO CLIENT
SEND_CUSTOMER_REGISTER = "Dear {0}, Congratulations. You have enrolled for AfterBuy; a completely \
hassle free one-stop place to value-track-care all your purchases & beyond."
SEND_CUSTOMER_SERVICE_DETAIL = "CUSTOMER ID: {0} PRODUCT ID: {1} COUPONS: {2}"
SEND_CUSTOMER_PRODUCT_REGISTER = "Successfully register PRODUCT ID: {0} INTO CUSTOMER ID: {1}"
SEND_CUSTOMER_INVALID_CUSTOMER = "Invalid CUSTOMER ID: {0}"
SEND_SA_VALID_COUPON="Customer can avail Free {0}"
SEND_SA_EXPIRED_COUPON="Free {1} expired and can avail {0} Free Service"
SEND_CUSTOMER_VALID_COUPON="Free Service Coupon {0} to Avail {1}"
SEND_CUSTOMER_EXPIRED_COUPON="Free Service Coupon {0} to Avail {1}\
 has expired (KMS/Date not valid) and Free Service Coupon {2} to Avail {3}"
SEND_SA_INVALID_COUPON_DETAIL="Wrong COUPON ID:{0}"
SEND_SA_UNAUTHORISED_SA="DEALER NOT AUTHORISED:{0}"
SEND_CUSTOMER_COUPON_REMINDER = "Reminder: Your Coupon {0} for product {1} will expire on {2}"
SEND_SA_CLOSE_COUPON="Service Completion Tagged into the System. Thank you."
SEND_CUSTOMER_CLOSE_COUPON="Your Bike {0} service is complete. Please pick your Bike before 6.30PM. {1}, {2}.Thank you."
SEND_INVALID_MESSAGE = "Invalid message"
SEND_BRAND_DATA="{0}"

#MESSAGE TEMPLATE RECEIVED FROM CLIENT
RCV_MESSAGE_FORMAT = "{key} {message}"
RCV_CUSTOMER_REGISTRATION = "{email_id} {name}"
RCV_CUSTOMER_SERVICE_DETAIL = "{customer_id}"
RCV_SA_COUPON_VALIDATION = "{vin} {kms} {service_type}"
RCV_SA_COUPON_COMPLETE = "{vin} {usc}"
RCV_CUSTOMER_BRAND_DATA="{brand_id}"

MESSAGE_TEMPLATE_MAPPER = {
            'gcp_reg':{
                       'receive':RCV_CUSTOMER_REGISTRATION,
                       'send':SEND_CUSTOMER_REGISTER,
                       'invalid':SEND_INVALID_MESSAGE,
                       'handler':'register_customer',
                       'auth_rule': ['open']
                       },
            'service':{
                       'receive':RCV_CUSTOMER_SERVICE_DETAIL,
                       'send':SEND_CUSTOMER_SERVICE_DETAIL,
                       'invalid':SEND_CUSTOMER_INVALID_CUSTOMER,
                       'handler':'customer_service_detail',
                       'auth_rule': ['customer']
                       },
            'check':{
                     'receive': RCV_SA_COUPON_VALIDATION,
                     'send':SEND_SA_VALID_COUPON,
                     'invalid':SEND_SA_EXPIRED_COUPON,
                     'handler':'validate_coupon',
                     'auth_rule': ['sa']
                     },
            'close':{
                        'receive': RCV_SA_COUPON_COMPLETE,
                        'send':SEND_SA_CLOSE_COUPON,
                        'invalid':SEND_INVALID_MESSAGE,
                        'handler':'close_coupon',
                        'auth_rule': ['sa']
                        },
            'brand':{
                     'receive': RCV_CUSTOMER_BRAND_DATA,
                     'send':SEND_BRAND_DATA,
                    'invalid':SEND_INVALID_MESSAGE,
                    'handler':'get_brand_data',
                    'auth_rule': ['open']
                     }
        }


