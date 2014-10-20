from datetime import datetime
from random import randint
from django.utils import timezone
from gladminds.afterbuy import models as common
from gladminds.afterbuy import models as afterbuy_common
from gladminds.core import base_models as common
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY

def save_otp(user, token):
    print "1"
    afterbuy_common.OTPToken.objects.filter(user=user).delete()
    print "2"
    token_obj = afterbuy_common.OTPToken(user=user, token=str(token), request_date=datetime.now(), email=user.user.email)
    token_obj.save()
    print "3"

def get_token(user, phone_number):
    totp=TOTP(TOTP_SECRET_KEY+str(randint(10000,99999))+str(phone_number))
    totp.time=30
    token = totp.token()
    save_otp(user, token)
    print token
    return token

def validate_otp(user, otp, phone):
    token_obj = common.OTPToken.objects.filter(user=user)[0]
    if int(otp) == int(token_obj.token) and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
        return True
    elif (timezone.now()-token_obj.request_date).seconds > OTP_VALIDITY:
        token_obj.delete()
    raise