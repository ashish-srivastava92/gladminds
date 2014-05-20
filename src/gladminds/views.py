from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from gladminds.models import common
import logging
from gladminds.tasks import send_otp
from django.contrib.auth.decorators import login_required
from gladminds import utils, message_template
from django.conf import settings
from gladminds.tasks import export_asc_registeration_to_sap
from gladminds.utils import get_task_queue, mobile_format
import json
from gladminds.mail import sent_otp_email
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
import logging, json, csv, os

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
    details_file = os.path.realpath('purchase_details.csv')
    vin_list = []
    with open(details_file, 'rb') as csvfile:
        
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            vin_list.append(row[0].split(',')[1])
        
        print vin_list
        
#    for vin in vin_list:
#        product_data = common.ProductData.objects.get(vin=vin)
#        print product_data
#        pass
