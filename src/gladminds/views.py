from django.shortcuts import render_to_response, render
from django.contrib.auth.views import login_required
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest
from gladminds.models import common
import logging, json
from gladminds.tasks import send_otp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from gladminds import utils, message_template
from django.conf import settings
from gladminds.utils import get_task_queue, get_customer_info,\
    get_sa_list, get_coupon_info
from gladminds.mail import sent_otp_email
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


@login_required(login_url='/user/login/')
def register(request, user=None):
    if request.method == 'GET':
        template_mapping = {
            'asc': {'template': 'portal/asc_registration.html', 'active_menu': 'register_asc'},
            'sa': {'template': 'portal/sa_registration.html', 'active_menu': 'register_sa'},
        }
        return render(request, template_mapping[user]['template'], {'active_menu' : template_mapping[user]['active_menu']})
    elif request.method == 'POST':
        save_user = {
            'asc': save_asc_registeration,
            'sa': save_sa_registration
        }
        status = save_user[user](request.POST)
        return HttpResponse({"status": status}, content_type="application/json")
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/user/login/')
def exceptions(request, exception=None):
    if request.method == 'GET':
        template = 'portal/exception.html'
        data=None
        data_mapping = {
            'close' : get_sa_list,
            'check' : get_sa_list
        }
        try:
            data = data_mapping[exception](request)
        except:
            #It is acceptable if there is no data_mapping defined for a function
            pass
        return render(request, template, {'active_menu' : exception, "data" : data})
    elif request.method == 'POST':
        function_mapping = {
            'customer' : get_customer_info,
            'recover' : get_coupon_info
        }
        try:
            data = function_mapping[exception](request)
            return HttpResponse(content=json.dumps(data),  content_type='application/json')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
        

SUCCESS_MESSAGE = "Registration is complete"
def save_asc_registeration(data):
    reject_keys = ['csrfmiddlewaretoken']
    data = {key: val for key, val in data.iteritems() \
                                    if key not in reject_keys}
    try:
        asc_obj = common.ASCSaveForm(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone-number'], email=data['email'],
                 pincode=data['pincode'])
        asc_obj.save()

    except KeyError:
        return HttpResponseBadRequest()
    return {"message": SUCCESS_MESSAGE}

def save_sa_registration(data):
    data= {key: val for key, val in data.iteritems()}
    try:
        asc_obj = common.SASaveForm(name=data['name'],
                 phone_number=data['phone-number'], status=data['status'])
        asc_obj.save()

    except KeyError:
        return HttpResponseBadRequest()
    return {"message": SUCCESS_MESSAGE}


