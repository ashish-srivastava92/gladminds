from django.shortcuts import render_to_response
from django.conf import settings

def send_sms(request):
    return render_to_response('mobile.html')


def views_coupon_redeem_wsdl(request, show_indexes=False):
    return render_to_response(settings.COUPON_WSDL, content_type = 'application/xml')

def views_customer_registration_wsdl(request, show_indexes=False):
    return render_to_response(settings.CUSTOMER_REGISTRATION_WSDL, content_type = 'application/xml')

def views_vin_sync_wsdl(request, show_indexes=False):
    return render_to_response(settings.VIN_SYNC_WSDL, content_type = 'application/xml')

def views_member_sync_wsdl(request, show_indexes=False):
    return render_to_response(settings.MEMBER_SYNC_WSDL, content_type = 'application/xml')

def views_purchase_sync_wsdl(request, show_indexes=False):
    return render_to_response(settings.PURCHASE_SYNC_WSDL, content_type = 'application/xml')