CUSTOMER_REGISTER = "Dear {0}, Congratulations. You have enrolled for AfterBuy; a completely \
hassle free one-stop place to value-track-care all your purchases & beyond."
SERVICE_DETAIL = "CUSTOMER ID: {0} PRODUCT ID: {1} COUPONS: {2}"
REGISTER_PRODUCT = "Successfully register PRODUCT ID: {0} INTO CUSTOMER ID: {1}"
INVALID_SERVICE_DETAIL = "Invalid CUSTOMER ID: {0}"
VALID_COUPON="Customer can avail Free {0}"
EXPIRED_COUPON="Free {1} expired and can avail {0} Free Service"
INVALID_COUPON_DETAIL="Wrong COUPON ID:{0}"
UNAUTHORISED_SA="DEALER NOT AUTHORISED:{0}"
REMINDER_COUPON_EXPIRY = "Reminder: Your Coupon {0} for product {1} will expire on {2}"
SA_CLOSE_COUPON="Service Completion Tagged into the System. Thank you."



#MESSAGE TEMPLATE SEND TO CLIENT
SEND_CUSTOMER_REGISTER = "Dear {0}, Congratulations. You have enrolled for AfterBuy; a completely \
hassle free one-stop place to value-track-care all your purchases & beyond."
SEND_CUSTOMER_SERVICE_DETAIL = "CUSTOMER ID: {0} PRODUCT ID: {1} COUPONS: {2}"
SEND_CUSTOMER_PRODUCT_REGISTER = "Successfully register PRODUCT ID: {0} INTO CUSTOMER ID: {1}"
SEND_CUSTOMER_INVALID_CUSTOMER = "Invalid CUSTOMER ID: {0}"
SEND_SA_VALID_COUPON="Customer can avail Free {0}"
SEND_SA_EXPIRED_COUPON="Free {1} expired and can avail {0} Free Service"
SEND_SA_INVALID_COUPON_DETAIL="Wrong COUPON ID:{0}"
SEND_SA_UNAUTHORISED_SA="DEALER NOT AUTHORISED:{0}"
SEND_CUSTOMER_COUPON_REMINDER = "Reminder: Your Coupon {0} for product {1} will expire on {2}"
SEND_SA_CLOSE_COUPON="Service Completion Tagged into the System. Thank you."

#MESSAGE TEMPLATE RECEIVED FROM CLIENT
RCV_MESSAGE_FORMAT = "{key} {message}"
RCV_CUSTOMER_REGISTRATION = "{email_id} {name}"
RCV_CUSTOMER_SERVICE_DETAIL = "{customer_id}"
RCV_SA_COUPON_VALIDATION = "{vin} {kms} {service_type}"
RCV_SA_COUPON_COMPLETE = "{vin} {usc}"

RCV_MESSAGE_TEMPLATE_MAPPER = {
            'gcp_reg':RCV_CUSTOMER_REGISTRATION,
            'service':RCV_CUSTOMER_SERVICE_DETAIL,
            'check':RCV_SA_COUPON_VALIDATION,
            'complete':RCV_SA_COUPON_COMPLETE
            }


