import logging
import json
import random

from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout

from gladminds.models import common
from gladminds.sqs_tasks import send_otp
from gladminds import utils, message_template
from gladminds.utils import get_task_queue, get_customer_info,\
    get_sa_list, recover_coupon_info, mobile_format, format_date_string, stringify_groups,\
    get_list_from_set
from gladminds.sqs_tasks import export_asc_registeration_to_sap
from gladminds.aftersell.models import common as aftersell_common
from gladminds.mail import sent_otp_email
from gladminds.feed import SAPFeed
from gladminds.aftersell.feed_log_remark import FeedLogWithRemark
from gladminds.aftersell.models import common as afterbuy_common
from gladminds.scheduler import SqsTaskQueue
from gladminds.resource.resources import GladmindsResources

gladmindsResources = GladmindsResources()
logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX

def auth_login(request, provider):
    if request.method == 'GET':
        provider_mapping = {
                            'asc': {'template_name': 'asc/login.html'},
                            'dasc': {'template_name': 'asc/login.html'},
                            'dealer': {'template_name': 'dealer/login.html'},
                            'servicedesk': {'template_name': 'service-desk/login.html'}
                            }
        return render(request, provider_mapping[provider]['template_name'])
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/aftersell/provider/redirect')
    return HttpResponseRedirect(request.path_info+'?auth_error=true')

def user_logout(request):
    if request.method == 'GET':
        #TODO: Implement brand restrictions.
        groups = stringify_groups(request.user)
        if 'dealers' in groups:
            logout(request)
            return HttpResponseRedirect('/aftersell/dealer/login')
        elif 'ascs' in groups:
            logout(request)
            return HttpResponseRedirect('/aftersell/asc/login')
        #TODO: Implement Dependent ASCs
        elif 'dascs' in groups:
            logout(request)
            return HttpResponseRedirect('/aftersell/dasc/login')
        elif 'SDM' in groups:
            logout(request)
            return HttpResponseRedirect('/aftersell/servicedesk/login')
        elif 'SDO' in groups:
            logout(request)
            return HttpResponseRedirect('/aftersell/servicedesk/login')
    return HttpResponseBadRequest('Not Allowed')

def generate_otp(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST['mobile']
            email = request.POST.get('email', '')
            logger.info('OTP request received. Mobile: {0}'.format(phone_number))
            user = aftersell_common.RegisteredASC.objects.filter(phone_number=mobile_format(phone_number))[0].user
            token = utils.get_token(user, phone_number, email=email)
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
            return HttpResponseRedirect('/aftersell/users/otp/validate?phone='+phone_number)
        except:
            logger.error('Invalid details, mobile {0}'.format(request.POST.get('mobile', '')))
            return HttpResponseRedirect('/aftersell/users/otp/generate?details=invalid')
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
            user = aftersell_common.RegisteredASC.objects.filter(phone_number=mobile_format(phone_number))[0].user
            utils.validate_otp(user, otp, phone_number)
            logger.info('OTP validated for mobile number {0}'.format(phone_number))
            return render(request, 'portal/reset_pass.html', {'otp': otp})
        except:
            logger.error('OTP validation failed for mobile number {0}'.format(phone_number))
            return HttpResponseRedirect('/aftersell/users/otp/generate?token=invalid')

def update_pass(request):
    try:
        otp = request.POST['otp']
        password = request.POST['password']
        utils.update_pass(otp, password)
        logger.info('Password has been updated.')
        return HttpResponseRedirect('/aftersell/asc/login?update=true')
    except:
        logger.error('Password update failed.')
        return HttpResponseRedirect('/aftersell//asc/login?error=true')

def redirect_user(request):
    group_name =  request.user.groups.all()
    if group_name[0].name== 'dealers':
        return HttpResponseRedirect('/aftersell/register/sa')
    if group_name[0].name == 'ascs':
       return HttpResponseRedirect('/aftersell/register/asc')
    if group_name[0].name == 'SDM' or group_name[0].name == 'SDO':
       return HttpResponseRedirect('/aftersell/register/servi')
     

@login_required()
def register(request, menu):
    groups = stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        user_id = request.user
        template_mapping = {
            'asc': {'template': 'portal/asc_registration.html', 'active_menu': 'register_asc'},
            'sa': {'template': 'portal/sa_registration.html', 'active_menu': 'register_sa'},
            'customer': {'template': 'portal/customer_registration.html', 'active_menu': 'register_customer'},
        }
        return render(request, template_mapping[menu]['template'], {'active_menu' : template_mapping[menu]['active_menu']\
                                                                    , 'groups': groups, 'user_id' : user_id})
    elif request.method == 'POST':
        save_user = {
            'asc': save_asc_registeration,
            'sa': save_sa_registration,
            'customer': register_customer
        }
        try:
            response_object = save_user[menu](request, groups)
            return HttpResponse(response_object, content_type="application/json")
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

def asc_registration(request):
    if request.method == 'GET':
        return render(request, 'portal/asc_registration.html', {'asc_registration': True})
    elif request.method == 'POST':
#        save_user = {
#            'asc': save_asc_registeration,
#        }
#        response_object = save_user['asc'](request, ['self'])
#        return HttpResponse(response_object, content_type="application/json")
        data = request.POST
        try:
            asc_obj = afterbuy_common.ASCSaveForm(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone-number'], email=data['email'],
                 pincode=data['pincode'], status=1)
            asc_obj.save()
        except:
            return HttpResponse(json.dumps({'message': 'Already Registered'}), content_type='application/json')
        return HttpResponse(json.dumps({'message': 'Registration is complete'}), content_type='application/json')

@login_required()
def exceptions(request, exception=None):
    groups = stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        template = 'portal/exception.html'
        data = None
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
            return HttpResponse(content=json.dumps(data), content_type='application/json')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
@login_required()
def servicedesk(request, servicedesk=None):
    groups = stringify_groups(request.user)
    if request.method == 'GET':
        template = 'portal/help_desk.html'
        data = None
        data_mapping = {
            'helpdesk' : get_sa_list
            }
        try:
            data = data_mapping[servicedesk](request)
        except:
            #It is acceptable if there is no data_mapping defined for a function
            pass
        return render(request, template, {'active_menu' : servicedesk, "data" : data, 'groups': groups,
                     "types": get_list_from_set(aftersell_common.FEEDBACK_TYPE),
                     "priorities": get_list_from_set(aftersell_common.PRIORITY)})
    elif request.method == 'POST':
        function_mapping = {
            'helpdesk' : save_help_desk_data
        }
        try:
            data = function_mapping[servicedesk](request)
            return HttpResponse(content=json.dumps(data), content_type='application/json')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def save_help_desk_data(request):
    fields = ['message', 'priority', 'advisorMobile', 'type', 'subject']
    sms_dict = {}
    for field in fields:
        sms_dict[field] = request.POST.get(field, None)
    return gladmindsResources.get_complain_data(sms_dict, sms_dict['advisorMobile'], with_detail=True)

UPDATE_FAIL = 'Phone number already registered!'
UPDATE_SUCCESS = 'Customer has been registered with ID: '
def register_customer(request, group=None):
    post_data = request.POST
    data_source = []
    product_obj = common.ProductData.objects.filter(vin=post_data['customer-vin'])
    temp_customer_id = TEMP_ID_PREFIX + str(random.randint(10**5, 10**6))
    data_source.append(utils.create_feed_data(post_data, product_obj[0], temp_customer_id))
    try:
        customer_obj = common.CustomerTempRegistration(product_data=product_obj[0],
                                                       new_customer_name=data_source[0]['customer_name'],
                                                       new_number=data_source[0]['customer_phone_number'],
                                                       product_purchase_date=data_source[0]['product_purchase_date'],
                                                       temp_customer_id=temp_customer_id)
        customer_obj.save()
        feed_remark = FeedLogWithRemark(len(data_source),
                                        feed_type='Purchase Feed',
                                        action='Received', status=True)
        sap_obj = SAPFeed()
        sap_obj.import_to_db(feed_type='purchase', data_source=data_source, feed_remark=feed_remark)
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": UPDATE_FAIL})
    return json.dumps({'message': UPDATE_SUCCESS + temp_customer_id})

SUCCESS_MESSAGE = 'Registration is complete'
EXCEPTION_INVALID_DEALER = 'The dealer-id provided is not registered'
ALREADY_REGISTERED = 'Already Registered Number'
def save_asc_registeration(request, groups=[], brand='bajaj'):
    #TODO: Remove the brand parameter and pass it inside request.POST
    data = request.POST
    phone_number = mobile_format(str(data['phone-number']))
    if not ('dealers' in groups or 'self' in groups):
        raise
    if afterbuy_common.RegisteredASC.objects.filter(phone_number=phone_number)\
        or afterbuy_common.ASCSaveForm.objects.filter(phone_number=phone_number):
        return json.dumps({'message': ALREADY_REGISTERED})

    try:
        dealer_data = None
        if "dealer_id" in data:
            dealer_data = afterbuy_common.RegisteredDealer.objects.\
                                            get(dealer_id=data["dealer_id"])
            dealer_data = dealer_data.dealer_id if dealer_data else None

        asc_obj = afterbuy_common.ASCSaveForm(name=data['name'],
                  address=data['address'], password=data['password'],
                  phone_number=phone_number, email=data['email'],
                  pincode=data['pincode'], status=1, dealer_id=dealer_data)
        asc_obj.save()
        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("export_asc_registeration_to_sap", \
               {"phone_number": phone_number, "brand": brand})
        else:
            export_asc_registeration_to_sap.delay(phone_number=data[
                                        'phone-number'], brand=brand)

    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": EXCEPTION_INVALID_DEALER})
    return json.dumps({"message": SUCCESS_MESSAGE})


def save_sa_registration(request, groups):
    data = request.POST
    if not ('dealers' in groups or 'ascs' in groups):
        raise
    data = {key: val for key, val in data.iteritems()}
    phone_number = mobile_format(str(data['phone-number']))
    if common.SASaveForm.objects.filter(phone_number=phone_number):
        return json.dumps({'message': ALREADY_REGISTERED})
    asc_obj = common.SASaveForm(name=data['name'],
    phone_number=phone_number, status=data['status'])
    asc_obj.save()
    return json.dumps({'message': SUCCESS_MESSAGE})


def register_user(request, user=None):
    save_user = {
        'asc': save_asc_registeration
    }
    status = save_user[user](request.POST)

    return HttpResponse(json.dumps(status), mimetype="application/json")

def sqs_tasks_view(request):
    return render_to_response('trigger-sqs-tasks.html')

def trigger_sqs_tasks(request):
    sqs_tasks = {
        'send-feed-mail' : 'send_report_mail_for_feed',
        'export_coupon_redeem' : 'export_coupon_redeem_to_sap',
        'expire-service-coupon': 'expire_service_coupon',
        'send-reminder': 'send_reminder',
    }

    taskqueue = SqsTaskQueue(settings.SQS_QUEUE_NAME)
    taskqueue.add(sqs_tasks[request.POST['task']])
    return HttpResponse()

def get_all_tickets(request):
    feedback = aftersell_common.Feedback.objects.all()
    return render(request,'service-desk/tickets.html',{"feedback":feedback})
