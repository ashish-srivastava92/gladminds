import logging
import json
import random
from datetime import datetime

from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models.query_utils import Q

from gladminds.bajaj import models as common
from gladminds.core import utils
from gladminds.bajaj.services import message_template
from gladminds.core.utils import get_task_queue, get_customer_info,\
    get_sa_list, recover_coupon_info, mobile_format, stringify_groups,\
    get_list_from_set,  get_user_groups, search_details
from gladminds.core.cron_jobs.sqs_tasks import export_asc_registeration_to_sap, send_otp
from gladminds.core.managers.mail import sent_otp_email
from gladminds.bajaj.feeds.feed import SAPFeed
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.core.cron_jobs.scheduler import SqsTaskQueue
from gladminds.bajaj.services.free_service_coupon import GladmindsResources
from gladminds.core.constants import PROVIDER_MAPPING, PROVIDERS, GROUP_MAPPING,\
    USER_GROUPS, REDIRECT_USER, TEMPLATE_MAPPING, ACTIVE_MENU

gladmindsResources = GladmindsResources()
logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX


def auth_login(request, provider):
    if request.method == 'GET':
            if provider not in PROVIDERS:
                return HttpResponseBadRequest()
            return render(request, PROVIDER_MAPPING.get(provider, 'asc/login.html'))

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

@login_required()
def change_password(request): 
    if request.method == 'GET':
        return render(request, 'portal/change_password.html')
    if request.method == 'POST':
        groups = stringify_groups(request.user)
        if 'dealers' in groups or 'ascs' in groups:
            user = User.objects.get(username=request.user)
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
            check_pass = user.check_password(str(old_password))
            if check_pass:
                user.set_password(str(new_password))
                user.save()
                data = {'message': 'Password Changed successfully', 'status': True}
            else:
                data = {'message': 'Old password wrong', 'status': False}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponseBadRequest('Not Allowed')

def generate_otp(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST['mobile']
            email = request.POST.get('email', '')
            logger.info('OTP request received. Mobile: {0}'.format(phone_number))
            user = common.AuthorizedServiceCenter.objects.filter(phone_number=mobile_format(phone_number))[0].user
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
            user = common.AuthorizedServiceCenter.objects.filter(phone_number=mobile_format(phone_number))[0].user
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
        return render(request, 'portal/asc_registration.html',
                      {'asc_registration': True})
    elif request.method == 'POST':
#        save_user = {
#            'asc': save_asc_registeration,
#        }
#        response_object = save_user['asc'](request, ['self'])
#        return HttpResponse(response_object, content_type="application/json")
        data = request.POST
        try:
            asc_obj = common.ASCTempRegistration(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone-number'], email=data['email'],
                 pincode=data['pincode'], status=1)
            asc_obj.save()
        except:
            return HttpResponse(json.dumps({'message': 'Already Registered'}),
                                content_type='application/json')
        return HttpResponse(json.dumps({'message': 'Registration is complete'}),
                            content_type='application/json')


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
            'close': get_sa_list,
            'check': get_sa_list
        }
        try:
            data = data_mapping[exception](request)
        except:
            #It is acceptable if there is no
            #data_mapping defined for a function
            pass
        return render(request, template, {'active_menu': exception,
                                           "data": data, 'groups': groups})
    elif request.method == 'POST':
        function_mapping = {
            'customer': get_customer_info,
            'recover': recover_coupon_info,
            'search': search_details
        }
        try:
            data = function_mapping[exception](request)
            return HttpResponse(content=json.dumps(data), content_type='application/json')
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@login_required()
def users(request, users=None):
    groups = stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        template = 'portal/users.html'
        data=None
        data_mapping = {
            'sa': get_sa_list_for_login_dealer,
            'asc': get_asc_list_for_login_dealer
        }
        try:
            data = data_mapping[users](request.user)
        except:
            #It is acceptable if there is no data_mapping defined for a function
            pass
        return render(request, template, {'active_menu' : users, "data" : data, 'groups': groups})
    else:
        return HttpResponseBadRequest()

@login_required()
def get_sa_under_asc(request, id=None):
    template = 'portal/sa_list.html'
    data = None
    try:
            data = get_sa_list_for_login_dealer(id)
    except:
            #It is acceptable if there is no data_mapping defined for a function
        pass
    return render(request, template, {'active_menu':'sa',"data": data})

@login_required()
def servicedesk(request, servicedesk=None):
    groups = stringify_groups(request.user)
    if request.method == 'GET':
        template = 'portal/help_desk.html'
        data = None
        data_mapping = {
            'helpdesk': get_sa_list
            }
        try:
            data = data_mapping[servicedesk](request)
        except:
            #It is acceptable if there is no data_mapping defined for a function
            pass
        return render(request, template, {'active_menu': servicedesk,
                                          "data": data, 'groups': groups,
                     "types": get_list_from_set(common.FEEDBACK_TYPE),
                     "priorities": get_list_from_set(common.PRIORITY)})
    elif request.method == 'POST':
        function_mapping = {
            'helpdesk': save_help_desk_data
        }
        try:
            data = function_mapping[servicedesk](request)
            return HttpResponse(content=json.dumps(data),
                                content_type='application/json')
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
def reports(request):
    groups = stringify_groups(request.user)
    report_data=[]
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    status_options = {'4': 'In Progress', '2':'Closed'}
    report_options = {'reconciliation': 'Reconciliation', 'credit':'Credit Note'}  
    min_date, max_date = utils.get_min_and_max_filter_date()
    template_rendered = 'portal/reconciliation_report.html'
    report_data =  {'status_options': status_options,
                    'report_options': report_options,
                    'min_date':min_date,
                    'max_date': max_date}
    if request.method == 'POST':
        report_data['params'] = request.POST.copy()
        if report_data['params']['type']== 'credit':
            report_data['params']['status']='2'
            template_rendered = 'portal/credit_note_report.html'
        report_data['records'] = create_reconciliation_report(report_data['params'], request.user)
    return render(request, template_rendered, report_data)

@log_time
def create_reconciliation_report(query_params, user):
    report_data = []
    filter = {}
    params = {}
    user = afterbuy_common.RegisteredDealer.objects.filter(dealer_id=user)
    filter['servicing_dealer'] = user[0]
    args = { Q(status=4) | Q(status=2) | Q(status=6)}
    status = query_params.get('status')
    from_date = query_params.get('from')
    to_date = query_params.get('to')
    filter['actual_service_date__range'] = (str(from_date) + ' 00:00:00', str(to_date) +' 23:59:59')
    if status:
        args = { Q(status=status) }
        if status=='2':
            args = { Q(status=2) | Q(status=6)}      
    all_coupon_data = common.CouponData.objects.filter(*args, **filter).order_by('-actual_service_date')
    map_status = {'6': 'Closed', '4': 'In Progress', '2':'Closed'}
    for coupon_data in all_coupon_data:
        coupon_data_dict = {}
        coupon_data_dict['vin'] = coupon_data.vin.vin
        coupon_data_dict['sa_phone_name'] = coupon_data.sa_phone_number
        coupon_data_dict['service_avil_date'] = coupon_data.actual_service_date
        coupon_data_dict['closed_date'] = coupon_data.closed_date
        coupon_data_dict['service_status'] = map_status[str(coupon_data.status)]
        if query_params['type']== 'credit':
            customer_details = coupon_data.vin.customer_phone_number
            coupon_data_dict['customer_name'] = customer_details.customer_name
            coupon_data_dict['customer_number'] = customer_details.phone_number
            coupon_data_dict['credit_date'] = coupon_data.credit_date
            coupon_data_dict['credit_note'] = coupon_data.credit_note
        else:
            coupon_data_dict['customer_id'] = coupon_data.vin.sap_customer_id
            coupon_data_dict['product_type'] = coupon_data.vin.product_type
            coupon_data_dict['coupon_no'] = coupon_data.unique_service_coupon
            coupon_data_dict['kms'] = coupon_data.actual_kms
            coupon_data_dict['service_type'] = coupon_data.service_type
            coupon_data_dict['special_case'] = coupon_data.special_case
        report_data.append(coupon_data_dict)
    return report_data
    

CUST_UPDATE_SUCCESS = 'Customer phone number has been updated.'
CUST_REGISTER_SUCCESS = 'Customer has been registered with ID: '
@log_time
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
    check_with_today_date = utils.subtract_dates(data_source[0]['product_purchase_date'], datetime.datetime.now())

    if not existing_customer and check_with_invoice_date.days < 0 or check_with_today_date.days > 0:
        message = "Product purchase date should be between {0} and {1}".\
                format((product_obj[0].invoice_date).strftime("%d-%m-%Y"),(datetime.datetime.now()).strftime("%d-%m-%Y"))
        logger.info('[Temporary_cust_registration]:: {0} Entered date is: {1}'.format(message, str(data_source[0]['product_purchase_date'])))
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
            logger.info('[Temporary_cust_registration]:: Initiating purchase feed')
            feed_remark = FeedLogWithRemark(len(data_source),
                                                feed_type='Purchase Feed',
                                                action='Received', status=True)
            sap_obj = SAPFeed()
            feed_response = sap_obj.import_to_db(feed_type='purchase', data_source=data_source, feed_remark=feed_remark)
            if feed_response.failed_feeds > 0:
                logger.info('[Temporary_cust_registration]:: ' + json.dumps(feed_response.remarks))
                raise ValueError('purchase feed failed!')
            logger.info('[Temporary_cust_registration]:: purchase feed completed')
    except Exception as ex:
        logger.info(ex)
        return HttpResponseBadRequest()
    if existing_customer:
        return json.dumps({'message': CUST_UPDATE_SUCCESS})
    return json.dumps({'message': CUST_REGISTER_SUCCESS + temp_customer_id})
      

ASC_REGISTER_SUCCESS = 'ASC registration is complete.'
EXCEPTION_INVALID_DEALER = 'The dealer-id provided is not registered.'
ALREADY_REGISTERED = 'Already Registered Number.'
@log_time
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
               {"phone_number": phone_number, "brand": brand, "sms_client":settings.SMS_CLIENT})
        else:
            export_asc_registeration_to_sap.delay(phone_number=data[
                                        'phone-number'], brand=brand,
                                        sms_client=settings.SMS_CLIENT)

    except Exception as ex:
        logger.info(ex)
        return json.dumps({"message": EXCEPTION_INVALID_DEALER})
    return json.dumps({"message": ASC_REGISTER_SUCCESS})

SA_UPDATE_SUCCESS = 'Service advisor status has been updated.'
SA_REGISTER_SUCCESS = 'Service advisor registration is complete.'
@log_time
def save_sa_registration(request, groups):
    data = request.POST
    existing_sa = False
    data_source = []
    phone_number = mobile_format(str(data['phone-number']))
    if data['sa-id']:
        service_advisor_id = data['sa-id']
        existing_sa = True
    else:
        service_advisor_id = TEMP_SA_ID_PREFIX + str(random.randint(10**5, 10**6))
   
    data_source.append(utils.create_sa_feed_data(data, request.user, service_advisor_id))
    logger.info('[Temporary_sa_registration]:: Initiating dealer-sa feed for ID' + service_advisor_id)
    feed_remark = FeedLogWithRemark(len(data_source),
                                                feed_type='Dealer Feed',
                                                action='Received', status=True)
    sap_obj = SAPFeed()
    
    feed_response = sap_obj.import_to_db(feed_type='dealer',
                        data_source=data_source, feed_remark=feed_remark)
    if feed_response.failed_feeds > 0:
        failure_msg = list(feed_response.remarks.elements())[0]
        logger.info('[Temporary_sa_registration]:: dealer-sa feed fialed ' + failure_msg)
        return json.dumps({"message": failure_msg})
    logger.info('[Temporary_sa_registration]:: dealer-sa feed completed')
    if existing_sa:
        return json.dumps({'message': SA_UPDATE_SUCCESS})
    return json.dumps({'message': SA_REGISTER_SUCCESS})

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
        'send-feed-mail': 'send_report_mail_for_feed',
        'export-coupon-redeem': 'export_coupon_redeem_to_sap',
        'expire-service-coupon': 'expire_service_coupon',
        'send-reminder': 'send_reminder',
        'export-customer-registered': 'export_customer_reg_to_sap',
    }

    taskqueue = SqsTaskQueue(settings.SQS_QUEUE_NAME)
    taskqueue.add(sqs_tasks[request.POST['task']])
    return HttpResponse()


def site_info(request):
    if request.method != 'GET':
        raise Http404
    brand = settings.BRAND
    return HttpResponse(json.dumps({'brand': brand}), content_type='application/json')

def brand_details(requests, role=None):
    data = requests.GET
    data_list = []
    data_dict = {}
    limit = data.get('limit', 20)
    offset = data.get('offset', 0)
    limit = int(limit)
    offset = int(offset)
    if role == 'asc':
        asc_data = aftersell_common.RegisteredDealer.objects.filter(role='asc')
        data_dict['total_count'] = len(asc_data)
        for asc in asc_data[offset:limit]:
            asc_detail = {}
            asc_detail['id'] = asc.dealer_id
            asc_detail['address'] = asc.address
            asc_details = get_state_city(asc_detail, asc.address)
            data_list.append(asc_detail)
        data_dict[role] = data_list
    elif role == 'sa':
        sa_data = aftersell_common.ServiceAdvisor.objects.all()
        data_dict['total_count'] = len(sa_data)
        for sa in sa_data[offset:limit]:
            sa_detail = {}
            sa_detail = get_sa_details(sa_detail, sa )
            sa_detail['id'] = sa.service_advisor_id
            sa_detail['name'] = sa.name
            sa_detail['phone_number'] = sa.phone_number
            data_list.append(sa_detail)
        data_dict[role] = data_list
    elif role == 'customers':
        customer_data = common.GladMindUsers.objects.all()
        data_dict['total_count'] = len(customer_data)
        for customer in customer_data[offset:limit]:
            customer_product = common.ProductData.objects.filter(customer_phone_number=customer)
            customer_detail = {}
            if  customer_product:
                customer_detail['vin'] = customer_product[0].vin
                customer_detail['sap_id'] = customer_product[0].sap_customer_id
            customer_detail['id'] = customer.gladmind_customer_id
            customer_detail['name'] = customer.customer_name
            customer_detail['phone_number'] = customer.phone_number
            customer_detail['email_id'] = customer.email_id
            customer_detail['address'] = customer.address
            customer_detail = get_state_city(customer_detail, customer.address)
            data_list.append(customer_detail)
        data_dict[role] = data_list
    elif role == 'active-asc':
        active_asc_count = 0
        asc_details = get_asc_data()
        for asc_detail in asc_details:
                active_ascs = {}
                if asc_detail.date_joined != asc_detail.last_login:
                    active_asc_count = active_asc_count + 1;
                    asc_data = aftersell_common.RegisteredDealer.objects.get(dealer_id=asc_detail.username)
                    active_ascs['id'] = asc_data.dealer_id
                    active_ascs['address'] = asc_data.address
                    active_ascs = get_state_city(active_ascs, asc_data.address)
                    active_ascs['cuopon_unused'] = asc_cuopon_details(asc_data.dealer_id, 1)
                    active_ascs['cuopon_closed'] = asc_cuopon_details(asc_data.dealer_id, 2)
                    active_ascs['cuopon_expired'] = asc_cuopon_details(asc_data.dealer_id, 3)
                    active_ascs['cuopon_inprogress'] = asc_cuopon_details(asc_data.dealer_id, 4)
                    active_ascs['cuopon_exceed_limit'] = asc_cuopon_details(asc_data.dealer_id, 5)
                    active_ascs['cuopon_closed_old_fsc'] = asc_cuopon_details(asc_data.dealer_id, 6)
                    data_list.append(active_ascs)
        data_dict['count'] = active_asc_count
        data_dict[role] = data_list
    elif role == 'not-active-asc':
        not_active_asc_count = 0
        asc_details = get_asc_data()
        for asc_detail in asc_details:
                not_active_ascs = {}
                if asc_detail.date_joined == asc_detail.last_login:
                    not_active_asc_count = not_active_asc_count + 1;
                    asc_data = aftersell_common.RegisteredDealer.objects.get(dealer_id=asc_detail.username)
                    not_active_ascs['id'] = asc_data.dealer_id
                    data_list.append(not_active_ascs)
        data_dict['count'] = not_active_asc_count
        data_dict[role] = data_list
    if data.get('city') or data.get('state') or data.get('sap_id'):
        filter_data_list = []
        filter_data_dict = {}
        count = 0
        for filter in data_dict[role]:
            if filter.get("city", None) == data.get('city') or filter.get('state', None) == data.get('state') or filter.get('sap_id', None) == data.get('sap_id'):
                count = count + 1
                filter_data_list.append(filter)
                filter_data_dict[role] = filter_data_list
                filter_data_dict['count'] = count
                return HttpResponse(json.dumps(filter_data_dict))
            else:
                return HttpResponse(json.dumps(filter_data_list))
    return HttpResponse(json.dumps(data_dict))


def get_sa_details(sa_details, id):
    sa_detail = aftersell_common.ServiceAdvisorDealerRelationship.objects.filter(service_advisor_id=id)
    if sa_detail:
        sa_dealer_details = aftersell_common.RegisteredDealer.objects.get(id=sa_detail[0].dealer_id.id)
        if sa_dealer_details.role == None:
            sa_details['dealer'] = sa_dealer_details.dealer_id
        else:
            sa_details['asc'] = sa_dealer_details.dealer_id
    else:
        sa_details['dealer/asc'] = 'Null'
    return sa_details