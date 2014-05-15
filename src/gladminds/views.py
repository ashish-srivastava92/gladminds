from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest
from gladminds.models import common
from gladminds.tasks import send_otp
from django.contrib.auth.decorators import login_required
from gladminds import utils, message_template
from django.conf import settings
from gladminds.utils import get_task_queue, get_customer_info,\
    get_sa_list, recover_coupon_info
from gladminds.tasks import export_asc_registeration_to_sap
from gladminds.mail import sent_otp_email
from django.contrib.auth.models import Group
import logging, json

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

def redirect_user(request):
    asc_group = Group.objects.get(name='ascs')
    if asc_group in request.user.groups.all():
        return HttpResponseRedirect('/register/sa')
    return HttpResponseRedirect('/register/asc')

@login_required(login_url='/user/login/')
def register(request, menu):
    groups = []
    for group in request.user.groups.all():
        groups.append(str(group.name))
    if request.method == 'GET':
        template_mapping = {
            'asc': {'template': 'portal/asc_registration.html', 'active_menu': 'register_asc'},
            'sa': {'template': 'portal/sa_registration.html', 'active_menu': 'register_sa'},
            'customer': {'template': 'portal/customer_registration.html', 'active_menu': 'register_customer'},
        }
        return render(request, template_mapping[menu]['template'], {'active_menu' : template_mapping[menu]['active_menu']\
                                                                    , 'groups': groups})
    elif request.method == 'POST':
        save_user = {
            'asc': save_asc_registeration,
            'sa': save_sa_registration
        }

        response_object = save_user[menu](request.POST, groups)
        return HttpResponse(response_object, content_type="application/json")
    else:
        return HttpResponseBadRequest()

def asc_registration(request):
    if request.method == 'GET':
        return render(request, 'portal/asc_registration.html', {'asc_registration': True})
    elif request.method == 'POST':
        save_user = {
            'asc': save_asc_registeration,
        }
        response_object = save_user['asc'](request.POST, ['self'])
        return HttpResponse(response_object, content_type="application/json")       

@login_required(login_url='/user/login/')
def exceptions(request, exception=None):
    groups = []
    for group in request.user.groups.all():
        groups.append(str(group.name))
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
        return render(request, template, {'active_menu' : exception, "data" : data, 'groups': groups})
    elif request.method == 'POST':
        function_mapping = {
            'customer' : get_customer_info,
            'recover' : recover_coupon_info
        }
        try:
            data = function_mapping[exception](request)
            return HttpResponse(content=json.dumps(data),  content_type='application/json')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    
@login_required(login_url='/user/login/')
def register_customer(request):
    if 'customer-name' not in request.POST:
        data = request.POST
        try:
            product_obj = common.ProductData.objects.get(vin=data['customer-vin'])
            product_obj.customer_phone_number.phone_number = data['customer-phone']
            product_obj.customer_phone_number.save()
            return HttpResponse(json.dumps({'message': 'Updated customer details'}),  content_type='application/json')
        #TODO : will have to add more scenarios then we could give proper error messages for exception
        except Exception as ex:
            logger.info(ex)
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
        

SUCCESS_MESSAGE = 'Registration is complete'
EXCEPTION_INVALID_DEALER = 'The dealer-id provided is not registered'
ALREADY_REGISTERED = 'Already Registered Number'
def save_asc_registeration(data, groups=[], brand='bajaj'):
    #TODO: Remove the brand parameter and pass it inside request.POST
    if not ('dealers' in groups or 'self' in groups):
        raise
    if common.RegisteredASC.objects.filter(phone_number=data['phone-number'])\
        or common.ASCSaveForm.objects.filter(phone_number=data['phone-number']):
        return json.dumps({'message': ALREADY_REGISTERED})

    try:
        dealer_data = None
        if "dealer_id" in data:
            dealer_data = common.RegisteredDealer.objects.\
                                            get(dealer_id=data["dealer_id"])
            dealer_data = dealer_data.dealer_id if dealer_data else None
        
        asc_obj = common.ASCSaveForm(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone-number'], email=data['email'],
                 pincode=data['pincode'], status=1, dealer_id=dealer_data)
        
        asc_obj.save()
        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("export_asc_registeration_to_sap", \
               {"phone_number": data['phone-number'], "brand": brand})
        else:
            export_asc_registeration_to_sap.delay(phone_number=data[
                                        'phone-number'], brand=brand)

    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": EXCEPTION_INVALID_DEALER})
    return json.dumps({"message": SUCCESS_MESSAGE})

def save_sa_registration(data, groups):
    if not ('dealers' in groups or 'ascs' in groups):
        raise
    data= {key: val for key, val in data.iteritems()}
    try:
        asc_obj = common.SASaveForm(name=data['name'],
                 phone_number=data['phone-number'], status=data['status'])
        asc_obj.save()

    except KeyError:
        return HttpResponseBadRequest()
    return {"message": SUCCESS_MESSAGE}
