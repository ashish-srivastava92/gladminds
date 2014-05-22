from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest
from gladminds.models import common
from gladminds.tasks import send_otp
from django.contrib.auth.decorators import login_required
from gladminds import utils, message_template
from django.conf import settings
from gladminds.tasks import export_asc_registeration_to_sap
from gladminds.utils import get_task_queue
from gladminds.mail import sent_otp_email
import logging, json
import os
import csv

logger = logging.getLogger('gladminds')


def generate_otp(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST['mobile']
            email = request.POST.get('email', '')
            logger.info('OTP request received. Mobile: {0}'.format(phone_number))
            token = utils.get_token(phone_number, email=email)
            message = message_template.get_template('SEND_OTP').format(token)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = get_task_queue()
                task_queue.add('send_otp', {'phone_number':phone_number, 'message':message})
            else:
                send_otp.delay(phone_number=phone_number, message=message)
            logger.info('OTP sent to mobile {0}'.format(phone_number))
            #Send email if email address exist
            if email:
                sent_otp_email(data=token, receiver=email, subject='Forgot Password')
            return HttpResponseRedirect('/users/otp/validate?phone='+phone_number)
        except:
            logger.error('Invalid details, mobile {0}'.format(request.POST.get('mobile', '')))
            return HttpResponseRedirect('/users/otp/generate?details=invalid')
    elif request.method == 'GET':
        return render(request, 'portal/get_otp.html')

def validate_otp(request):
    if request.method == 'GET':
        return render(request, 'portal/validate_otp.html')
    elif request.method == 'POST':
        try:
            otp = request.POST['otp']
            phone_number = request.POST['phone']
            logger.info('OTP {0} recieved for validation. Mobile {1}'.format(otp, phone_number))
            utils.validate_otp(otp, phone_number)
            logger.info('OTP validated for mobile number {0}'.format(phone_number))
            return render(request, 'portal/reset_pass.html', {'otp': otp})
        except:
            logger.error('OTP validation failed for mobile number {0}'.format(phone_number))
            return HttpResponseRedirect('/users/otp/generate?token=invalid')

def update_pass(request):
    try:
        otp=request.POST['otp']
        password=request.POST['password']
        utils.update_pass(otp, password)
        logger.info('Password has been updated.')
        return HttpResponseRedirect('/dealers/?update=true')
    except:
        logger.error('Password update failed.')
        return HttpResponseRedirect('/dealers/?error=true')

@login_required(login_url='/dealers/')
def action(request, params):
    if request.method == 'GET':
        try:
            dealer = common.RegisteredDealer.objects.filter(
                dealer_id=request.user)[0]
            service_advisors = common.ServiceAdvisorDealerRelationship.objects\
                                        .filter(dealer_id=dealer, status='Y')
            sa_phone_list = []
            for service_advisor in service_advisors:
                sa_phone_list.append(service_advisor.service_advisor_id)
            return render_to_response('dealer/advisor_actions.html',
                  {'phones': sa_phone_list},
                  context_instance=RequestContext(request))
        except:
            logger.info(
                'No service advisor for dealer %s found active' % request.user)
            raise

    elif request.method == 'POST':
        raise NotImplementedError()

@login_required(login_url='/dealers/')
def redirect(request):
    return HttpResponseRedirect('/dealers/' + str(request.user))

def register(request, user=None):
    template_mapping = {
        "asc": "portal/asc_registration.html",
    }
    return render(request, template_mapping[user])


PASSED_MESSAGE = "Registration is complete"


def save_asc_registeration(data, brand='bajaj'):
    if common.RegisteredASC.objects.filter(phone_number=data['mobile_number'])\
        or common.ASCSaveForm.objects.filter(phone_number=data['mobile_number']):
        return {"message": "Already Registered Number"}

    try:
        dealer_data = common.RegisteredDealer.objects.\
                                            filter(dealer_id=data["dealer_id"])
        dealer_data = dealer_data if dealer_data else None

        asc_obj = common.ASCSaveForm(name=data['name'],
                 address=data['address'], password=data['pwd'],
                 phone_number=data['mobile_number'], email=data['email'],
                 pincode=data['pincode'], status=1)

        asc_obj.save()

        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("export_asc_registeration_to_sap", \
               {"phone_number": data['mobile_number'], "brand": brand})
        else:
            export_asc_registeration_to_sap.delay(phone_number=data[
                                        'mobile_number'], brand=brand)

    except Exception as ex:
        logger.info(ex)
    return {"message": PASSED_MESSAGE}


def register_user(request, user=None):
    save_user = {
        'asc': save_asc_registeration
    }
    status = save_user[user](request.POST)

    return HttpResponse(json.dumps(status), mimetype="application/json")

def delete_purchase(request):
    if request.GET.urlencode() != 'token=gm123':
        return HttpResponseBadRequest('Not allowed')
    
    with open('product_list.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for product in common.ProductData.objects.all():
            coupon_data = common.CouponData.objects.filter(vin=product)
            if len(coupon_data) > 3:
                spamwriter.writerow(str(product.vin))
#                if product.customer_phone_number:
#                    product.customer_phone_number.delete()
#                product.delete()

    with open('product_list.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        vin_objs = common.ProductData.objects.raw("""select gp.* from gladminds_productdata gp join gladminds_coupondata gc on gp.id = gc.vin_id  group by gc.vin_id having count(*)>3""")
        for vin_obj in vin_objs:
            spamwriter.writerow(str(vin_obj.vin))
#            if product.customer_phone_number:
#                product.customer_phone_number.delete()
#            product.delete()

    return HttpResponse(len(vin_objs))
        
