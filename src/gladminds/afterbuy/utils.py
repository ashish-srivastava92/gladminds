from datetime import datetime
from random import randint
from django.utils import timezone

from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from gladminds.afterbuy.models import common as afterbuy_common
from django_otp.oath import TOTP
from gladminds.settings import TOTP_SECRET_KEY, OTP_VALIDITY

def save_otp(user, token, email):
    afterbuy_common.OTPToken.objects.filter(user=user).delete()
    token_obj = afterbuy_common.OTPToken(user=user, token=str(token), request_date=datetime.now(), email=email)
    token_obj.save()

def get_token(user, phone_number, email=''):
    if email and user.email_id != email:
        raise
    totp=TOTP(TOTP_SECRET_KEY+str(randint(10000,99999))+str(phone_number))
    totp.time=30
    token = totp.token()
    save_otp(user, token, email)
    return token

def validate_otp(user, otp, phone):
    token_obj = afterbuy_common.OTPToken.objects.filter(user=user)[0]
    if int(otp) == int(token_obj.token) and (timezone.now()-token_obj.request_date).seconds <= OTP_VALIDITY:
        return True
    elif (timezone.now()-token_obj.request_date).seconds > OTP_VALIDITY:
        token_obj.delete()
    raise