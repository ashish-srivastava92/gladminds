    from django.shortcuts import render_to_response
from django.conf import settings
# from gladminds.models import Customer,Product,Service


def send_sms(request):
    return render_to_response('mobile.html')


def views_coupon_redeem_wsdl(request, document_root, show_indexes=False):
    return render_to_response(settings.COUPON_WSDL, content_type = 'application/xml')

def views_customer_registration_wsdl(request, document_root, show_indexes=False):
    return render_to_response(settings.CUSTOMER_REGISTRATION_WSDL, content_type = 'application/xml')
