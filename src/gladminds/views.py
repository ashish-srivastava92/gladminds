import logging
import json
import random
import datetime

from datetime import datetime
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.db import transaction

from gladminds.models import common
from gladminds.sqs_tasks import send_otp
from gladminds import utils, message_template
from gladminds import mail
from gladminds.utils import get_task_queue, get_customer_info,\
    get_sa_list, recover_coupon_info, mobile_format, format_date_string, stringify_groups,\
    get_list_from_set, create_context, get_user_groups, search_details
from gladminds.sqs_tasks import export_asc_registeration_to_sap, send_sms
from gladminds.aftersell.models import common as aftersell_common
from gladminds.mail import sent_otp_email
from gladminds.feed import SAPFeed
from gladminds.aftersell.feed_log_remark import FeedLogWithRemark
from gladminds.aftersell.models import common as afterbuy_common
from gladminds.scheduler import SqsTaskQueue
from gladminds.resource.resources import GladmindsResources
from gladminds.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    USER_DESIGNATION, PROVIDER_MAPPING, PROVIDERS, GROUP_MAPPING,\
    USER_GROUPS, REDIRECT_USER, TEMPLATE_MAPPING, ACTIVE_MENU, TIME_FORMAT

gladmindsResources = GladmindsResources()
logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX

def auth_login(request, provider):
    if request.method == 'GET':
            if provider not in PROVIDERS:
                return HttpResponseBadRequest()
            return render(request, PROVIDER_MAPPING.get(provider,'asc/login.html'))
    
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
        user_groups = get_user_groups(request.user)
        for group in USER_GROUPS:
            if group in user_groups:
                logout(request)
                return HttpResponseRedirect(GROUP_MAPPING.get(group))
            
        return HttpResponseBadRequest()
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
                send_otp.delay(phone_number=phone_number, message=message)  # @UndefinedVariable
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
    user_groups = get_user_groups(request.user)
    for group in USER_GROUPS:
        if group in user_groups:
            return HttpResponseRedirect(REDIRECT_USER.get(group))
    return HttpResponseBadRequest()

@login_required()
def register(request, menu):
    groups = stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        user_id = request.user
        return render(request, TEMPLATE_MAPPING.get(menu), {'active_menu' : ACTIVE_MENU.get(menu)\
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
    if exception == 'report':
        report_data = create_report(request.method, request.POST, request.user)
        return render(request, 'portal/report.html', report_data)
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
            'recover' : recover_coupon_info,
            'search' : search_details
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

@login_required()
def reports(request, report=None):
    groups = stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if report == 'reconciliation':
        report_data = create_report(request.method, request.POST, request.user)
        return render(request, 'portal/report.html', report_data)
    else:
        return HttpResponseBadRequest()
    
def create_report(method, query_params, user):
    report_data = []
    filter = {}
    params = {}
    args = { Q(status=4) | Q(status=2) }
    status_options = {'4': 'In Progress', '2':'Closed'}
    user = afterbuy_common.RegisteredDealer.objects.filter(dealer_id=user)
    filter['servicing_dealer'] = user[0]
    params['min_date'], params['max_date'] = utils.get_min_and_max_filter_date() 
    if method == 'POST':
        message = "No coupon found."
        status = query_params.get('status')
        from_date = query_params.get('from')
        to_date = query_params.get('to')
        params['start_date'] = from_date
        params['to_date'] = to_date
        filter['actual_service_date__range'] = (str(from_date) + ' 00:00:00', str(to_date) +' 23:59:59')
        if status:
            params['status'] = status
            filter['status'] = status
        all_coupon_data = common.CouponData.objects.filter(*args, **filter)
    elif method == 'GET':
        message = "" 
        all_coupon_data = []
    else:
        return HttpResponseBadRequest()
    
    for coupon_data in all_coupon_data:
        coupon_data_dict = {}
        coupon_data_dict['customer_id'] = coupon_data.vin.sap_customer_id
        coupon_data_dict['product_type'] = coupon_data.vin.product_type
        coupon_data_dict['service_avil_date'] = coupon_data.actual_service_date
        coupon_data_dict['vin'] = coupon_data.vin.vin
        coupon_data_dict['coupon_no'] = coupon_data.unique_service_coupon
        coupon_data_dict['sa_phone_name'] = coupon_data.sa_phone_number
        coupon_data_dict['kms'] = coupon_data.actual_kms
        coupon_data_dict['service_type'] = coupon_data.service_type
        coupon_data_dict['service_status'] = status_options[str(coupon_data.status)]
        coupon_data_dict['special_case'] = ''
        report_data.append(coupon_data_dict)
    return {"records": report_data, 'status_options': status_options, 'params': params, 
            "message": message}
    

UPDATE_FAIL = 'Some error occurred, try again later.'
UPDATE_SUCCESS = 'Customer phone number has been updated '
REGISTER_SUCCESS = 'Customer has been registered with ID: '
def register_customer(request, group=None):
    post_data = request.POST
    data_source = []
    existing_customer = False
    product_obj = common.ProductData.objects.filter(vin=post_data['customer-vin'])
    if not post_data['customer-id']:
        temp_customer_id = TEMP_ID_PREFIX + str(random.randint(10**5, 10**6))
    else:
        temp_customer_id = post_data['customer-id']
        existing_customer = True
    data_source.append(utils.create_feed_data(post_data, product_obj[0], temp_customer_id))
    check_with_invoice_date = utils.subtract_dates(data_source[0]['product_purchase_date'], product_obj[0].invoice_date)
    check_with_today_date = utils.subtract_dates(data_source[0]['product_purchase_date'], datetime.now())
    if not existing_customer and check_with_invoice_date.days < 0 or check_with_today_date.days > 0:
        message = "Product purchase date should be between {0} and {1}".\
                format((product_obj[0].invoice_date).strftime("%d-%m-%Y"),(datetime.now()).strftime("%d-%m-%Y"))
        logger.info('{0} Entered date is: {1}'.format(message, str(data_source[0]['product_purchase_date'])))
        return json.dumps({"message": message})
    
    try:    
        with transaction.atomic():
            customer_obj = common.CustomerTempRegistration.objects.filter(temp_customer_id = temp_customer_id)
            if customer_obj:
                customer_obj = customer_obj[0]
                customer_obj.new_number = data_source[0]['customer_phone_number']
                customer_obj.sent_to_sap = False
            else:
                customer_obj = common.CustomerTempRegistration(product_data=product_obj[0], 
                                                               new_customer_name = data_source[0]['customer_name'],
                                                               new_number = data_source[0]['customer_phone_number'],
                                                               product_purchase_date = data_source[0]['product_purchase_date'],
                                                               temp_customer_id = temp_customer_id)
            customer_obj.save()
            
            feed_remark = FeedLogWithRemark(len(data_source),
                                                feed_type='Purchase Feed',
                                                action='Received', status=True)
            sap_obj = SAPFeed()
            feed_response = sap_obj.import_to_db(feed_type='purchase', data_source=data_source, feed_remark=feed_remark)
            if feed_response.failed_feeds > 0:
                logger.info(json.dumps(feed_response.remarks))
                raise 
    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": UPDATE_FAIL})
    if existing_customer:
        return json.dumps({'message': UPDATE_SUCCESS})
    return json.dumps({'message': REGISTER_SUCCESS + temp_customer_id})
      
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
        'export-coupon-redeem' : 'export_coupon_redeem_to_sap',
        'expire-service-coupon': 'expire_service_coupon',
        'send-reminder': 'send_reminder',
        'export-customer-registered' : 'export_customer_reg_to_sap',
    }

    taskqueue = SqsTaskQueue(settings.SQS_QUEUE_NAME)
    taskqueue.add(sqs_tasks[request.POST['task']])
    return HttpResponse()

#TODO Function needs to be refactored
def set_wait_time(feedback_data,feedbackid):
    start_date = feedback_data.pending_from
    end_date = datetime.now()
    start_date = start_date.strftime(TIME_FORMAT)
    end_date = end_date.strftime(TIME_FORMAT)
    start_date = datetime.strptime(start_date, TIME_FORMAT)
    end_date = datetime.strptime(end_date, TIME_FORMAT)
    wait = end_date - start_date
    wait_time = float(wait.days) + float(wait.seconds) / float(86400)
    previous_wait = feedback_data.wait_time
    aftersell_common.Feedback.objects.filter(id = feedbackid).update(wait_time=wait_time+previous_wait)

@login_required()
def get_servicedesk_tickets(request):
    group_name =  request.user.groups.all()
    user_obj = request.user
    if group_name[0].name == 'SDM':
        feedbacks = aftersell_common.Feedback.objects.order_by('-created_date')
    if group_name[0].name == 'SDO':
        servicedesk_obj = aftersell_common.ServiceDeskUser.objects.filter(user=user_obj)
        feedbacks = aftersell_common.Feedback.objects.filter(assign_to=servicedesk_obj[0]).order_by('-created_date') 
    return render(request,'service-desk/tickets.html',{"feedbacks":feedbacks})

@login_required() 
def modify_servicedesk_tickets(request,feedbackid):
    group_name =  request.user.groups.all()
    status = get_list_from_set(FEEDBACK_STATUS)
    priority = get_list_from_set(PRIORITY)
    type = get_list_from_set(FEEDBACK_TYPE)
    user_obj = request.user
    assign_status = False
    pending_status=False
    feedbacks = aftersell_common.Feedback.objects.filter(id = feedbackid)
    previous_status = feedbacks[0].status
    if feedbacks[0].status == 'Pending':
        pending_status = True
    servicedesk_obj_all = aftersell_common.ServiceDeskUser.objects.filter(designation = 'SDO')
    if request.method == 'GET':
        feedbacks = aftersell_common.Feedback.objects.filter(id = feedbackid)
    if request.method == 'POST':
        feedbacks = aftersell_common.Feedback.objects.filter(id = feedbackid)
        if feedbacks[0].assign_to:
            assign_number = feedbacks[0].assign_to.phone_number
        else:
            assign_number = None   
        assign = feedbacks[0].assign_to
        if assign is None:
            assign_status = True

        data = request.POST
        if data['Assign_To'] == 'None': 
            aftersell_common.Feedback.objects.filter(id = feedbackid).update( status = data['status'], priority = data['Priority'], modified_date = datetime.now())
        else:    
            servicedesk_assign_obj = aftersell_common.ServiceDeskUser.objects.filter(phone_number = data['Assign_To'])
            aftersell_common.Feedback.objects.filter(id = feedbackid).update(assign_to = servicedesk_assign_obj[0] , status = data['status'], priority = data['Priority'], modified_date = datetime.now())
        if data['status'] == 'Pending':
            feedbacks = aftersell_common.Feedback.objects.filter(id = feedbackid)
            aftersell_common.Feedback.objects.filter(id = feedbackid).update(pending_from = datetime.now(), modified_date = datetime.now())
                
        if data['status'] == 'Closed':
            aftersell_common.Feedback.objects.filter(id = feedbackid).update(closed_date = datetime.now(), modified_date = datetime.now())
             
        feedback_data = feedbacks[0]
        if assign_status and feedback_data.assign_to : 
            context = create_context('INITIATOR_FEEDBACK_MAIL_DETAIL', feedbacks[0]) 
            mail.send_email_to_initiator_after_issue_assigned(context, feedbacks[0])
            send_sms('INITIATOR_FEEDBACK_DETAILS',feedback_data.reporter, feedback_data)
             
        if feedback_data.status == 'Resolved':
            host = request.get_host()
            servicedesk_obj_all = aftersell_common.ServiceDeskUser.objects.filter(designation = 'SDM')
            aftersell_common.Feedback.objects.filter(id = feedbackid).update(resolved_date = datetime.now(),root_cause = data['rootcause'],resolution = data['resolution'])
            context = create_context('INITIATOR_FEEDBACK_RESOLVED_MAIL_DETAIL', feedbacks[0])
            mail.send_email_to_initiator_after_issue_resolved(context,feedbacks[0],host)
            context = create_context('TICKET_RESOLVED_DETAIL_TO_BAJAJ', feedbacks[0]) 
            mail.send_email_to_bajaj_after_issue_resolved(context) 
            context = create_context('TICKET_RESOLVED_DETAIL_TO_MANAGER', feedbacks[0])
            mail.send_email_to_manager_after_issue_resolved(context, servicedesk_obj_all[0])
            send_sms('INITIATOR_FEEDBACK_STATUS', feedback_data.reporter, feedback_data)
        if pending_status :
            set_wait_time(feedback_data,feedbackid)
                
        if feedback_data.assign_to:   
            if assign_number != feedback_data.assign_to.phone_number: 
                context = create_context('ASSIGNEE_FEEDBACK_MAIL_DETAIL', feedbacks[0])   
                mail.send_email_to_assignee(context, feedbacks[0])
                send_sms('SEND_MSG_TO_ASSIGNEE', feedback_data.assign_to.phone_number, feedback_data)
                
        if feedbacks[0].resolved_date:
            start_date = feedbacks[0].created_date
            end_date = feedbacks[0].resolved_date
            if start_date > end_date:
                raise ValueError('Invalid resolved date. Resolved date should be after the created date')
            else:
                start_date = start_date.strftime(TIME_FORMAT)
                end_date = end_date.strftime(TIME_FORMAT)
                start_date = datetime.strptime(start_date, TIME_FORMAT)
                end_date = datetime.strptime(end_date, TIME_FORMAT)
                wait = end_date - start_date
                wait_time = float(wait.days) + float(wait.seconds) / float(86400)
                feedbacks = aftersell_common.Feedback.objects.filter(id = feedbackid)
                wait_final = float(wait_time) - feedbacks[0].wait_time
                aftersell_common.Feedback.objects.filter(id = feedbackid).update(wait_time=wait_final)
    return render(request,'service-desk/ticket_modify.html',{"feedbacks":feedbacks,"FEEDBACK_STATUS": status,"PRIORITY":priority,"FEEDBACK_TYPE":type,"group":group_name[0].name,'servicedeskuser':servicedesk_obj_all, "status_sdo" : ['Open','Progress','Resolved'] })

def get_feedback_response(request,feedbackid):
    if request.method == 'POST':
        data = request.POST
        if data['feedbackresponse']:
            aftersell_common.Feedback.objects.filter(id = feedbackid).update( ratings = str(data['feedbackresponse'])) 
            return render(request,'service-desk/feedback_received.html')
        else:
            return HttpResponse()
        
