import logging
import json
import random
import datetime

from collections import OrderedDict
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect, HttpResponse,\
    HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from gladminds.core.service_handler import Services 
from gladminds.bajaj import models
from gladminds.bajaj.services import message_template
from gladminds.core import utils
from gladminds.sqs_tasks import send_otp
from gladminds.core.managers.mail import sent_otp_email,\
    send_recovery_email_to_admin, send_mail_when_vin_does_not_exist
from gladminds.bajaj.feeds.feed import SAPFeed
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.core.cron_jobs.scheduler import SqsTaskQueue
from gladminds.bajaj.services.free_service_coupon import GladmindsResources
from gladminds.core.constants import PROVIDER_MAPPING, PROVIDERS, GROUP_MAPPING,\
    USER_GROUPS, REDIRECT_USER, TEMPLATE_MAPPING, ACTIVE_MENU, MONTHS,\
    FEEDBACK_STATUS, FEEDBACK_TYPE, PRIORITY, ALL, DEALER, SDO, SDM,\
    BY_DEFAULT_RECORDS_PER_PAGE, PAGINATION_LINKS, RECORDS_PER_PAGE, ASC
    
from gladminds.core.decorator import log_time, check_service
from gladminds.core.utils import get_email_template, format_product_object
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.context import RequestContext

gladmindsResources = GladmindsResources()
logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX
TEMP_SA_ID_PREFIX = settings.TEMP_SA_ID_PREFIX


@check_service(Services.FREE_SERVICE_COUPON)
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

@check_service(Services.FREE_SERVICE_COUPON)
def redirect_user(request):
    user_groups = utils.get_user_groups(request.user)
    for group in USER_GROUPS:
        if group in user_groups:
            return HttpResponseRedirect(REDIRECT_USER.get(group))
    return HttpResponseBadRequest()

@check_service(Services.FREE_SERVICE_COUPON)
def user_logout(request):
    if request.method == 'GET':
        #TODO: Implement brand restrictions.
        user_groups = utils.get_user_groups(request.user)
        for group in USER_GROUPS:
            if group in user_groups:
                logout(request)
                return HttpResponseRedirect(GROUP_MAPPING.get(group))

        return HttpResponseBadRequest()
    return HttpResponseBadRequest('Not Allowed')

@check_service(Services.FREE_SERVICE_COUPON)
@login_required()
def change_password(request): 
    if request.method == 'GET':
        return render(request, 'portal/change_password.html')
    if request.method == 'POST':
        groups = utils.stringify_groups(request.user)
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

@check_service(Services.FREE_SERVICE_COUPON)
def generate_otp(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            user = User.objects.get(username=username)
            phone_number = ''            
            user_profile_obj = models.UserProfile.objects.filter(user=user) 
            if user_profile_obj:
                phone_number = (user_profile_obj[0]).phone_number
            logger.info('OTP request received . username: {0}'.format(username))
            token = utils.get_token(user, phone_number, email=user.email)
            message = message_template.get_template('SEND_OTP').format(token)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = utils.get_task_queue()
                task_queue.add('send_otp', {'phone_number':phone_number, 'message':message, 'sms_client':settings.SMS_CLIENT})
            else:
                send_otp.delay(phone_number=phone_number, message=message, sms_client=settings.SMS_CLIENT)  # @UndefinedVariable
            logger.info('OTP sent to mobile {0}'.format(phone_number))
            #Send email if email address exist
            if user.email:
                sent_otp_email(data=token, receiver=user.email, subject='Forgot Password')
            return HttpResponseRedirect('/aftersell/users/otp/validate?username='+username)
        except Exception as ex:
            logger.error('Invalid details, mobile {0}'.format(phone_number))
            return HttpResponseRedirect('/aftersell/users/otp/generate?details=invalid')
    elif request.method == 'GET':
        return render(request, 'portal/get_otp.html')

@check_service(Services.FREE_SERVICE_COUPON)
def validate_otp(request):
    if request.method == 'GET':
        return render(request, 'portal/validate_otp.html')
    elif request.method == 'POST':
        try:
            otp = request.POST['otp']
            username = request.POST['username']
            logger.info('OTP {0} recieved for validation. username {1}'.format(otp, username))
            utils.validate_otp(otp, username)
            logger.info('OTP validated for name {0}'.format(username))
            return render(request, 'portal/reset_pass.html', {'otp': otp})
        except:
            logger.error('OTP validation failed for name {0}'.format(username))
            return HttpResponseRedirect('/aftersell/users/otp/generate?token=invalid')

@check_service(Services.FREE_SERVICE_COUPON)
def update_pass(request):
    try:
        otp = request.POST['otp']
        password = request.POST['password']
        utils.update_pass(otp, password)
        logger.info('Password has been updated.')
        return HttpResponseRedirect('/aftersell/asc/login?update=true')
    except:
        logger.error('Password update failed.')
        return HttpResponseRedirect('/aftersell/asc/login?error=true')

@check_service(Services.FREE_SERVICE_COUPON)
@login_required()
def register(request, menu):
    groups = utils.stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        user_id = request.user
        return render(request, TEMPLATE_MAPPING.get(menu), {'active_menu' : ACTIVE_MENU.get(menu)\
                                                                    , 'groups': groups, 'user_id' : user_id})
    elif request.method == 'POST':
        save_user = {
            'asc': save_asc_registration,
            'sa': save_sa_registration,
            'customer': register_customer
        }
        try:
            response_object = save_user[menu](request, groups)
            return HttpResponse(response_object, content_type="application/json")
        except Exception as ex:
            logger.error('[registration failure {0}] : {1}'.format(menu, ex))
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

ASC_REGISTER_SUCCESS = 'ASC registration is complete.'
EXCEPTION_INVALID_DEALER = 'The dealer-id provided is not registered.'
ALREADY_REGISTERED = 'Already Registered Number.'
@check_service(Services.FREE_SERVICE_COUPON)
@log_time
def save_asc_registration(request, groups=None):
    if request.method == 'GET':
        return render(request, 'portal/asc_registration.html',
                      {'asc_registration': True})
    elif request.method == 'POST':
        data = request.POST
        try:
            asc_obj = models.ASCTempRegistration.objects.get(phone_number=data['phone-number'])
            return HttpResponse(json.dumps({'message': ALREADY_REGISTERED}),
                            content_type='application/json')
        except ObjectDoesNotExist as ex:
            
            dealer_data = data["dealer_id"] if data.has_key('dealer_id') else None  
            asc_obj = models.ASCTempRegistration(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone-number'], email=data['email'],
                 pincode=data['pincode'], dealer_id=dealer_data)
            asc_obj.save()
        return HttpResponse(json.dumps({'message': ASC_REGISTER_SUCCESS}),
                            content_type='application/json')

SA_UPDATE_SUCCESS = 'Service advisor status has been updated.'
SA_REGISTER_SUCCESS = 'Service advisor registration is complete.'
@log_time
def save_sa_registration(request, groups):
    data = request.POST
    existing_sa = False
    data_source = []
    phone_number = utils.mobile_format(str(data['phone-number']))
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

CUST_UPDATE_SUCCESS = 'Customer phone number has been updated.'
CUST_REGISTER_SUCCESS = 'Customer has been registered with ID: '
@log_time
def register_customer(request, group=None):
    post_data = request.POST
    data_source = []
    existing_customer = False
    product_obj = models.ProductData.objects.filter(product_id=post_data['customer-vin'])
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
            customer_obj = models.CustomerTempRegistration.objects.filter(temp_customer_id = temp_customer_id)
            if customer_obj:
                customer_obj = customer_obj[0]
                customer_obj.new_number = data_source[0]['customer_phone_number']
                customer_obj.sent_to_sap = False
            else:
                customer_obj = models.CustomerTempRegistration(product_data=product_obj[0], 
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

@check_service(Services.FREE_SERVICE_COUPON)
def recover_coupon_info(data):
    customer_id = data['customerId']
    logger.info('UCN for customer {0} requested by User {1}'.format(customer_id, data['current_user']))
    coupon_data = utils.get_coupon_info(data)
    if coupon_data:
        ucn_recovery_obj = utils.upload_file(data, coupon_data.unique_service_coupon)
        send_recovery_email_to_admin(ucn_recovery_obj, coupon_data)
        message = 'UCN for customer {0} is {1}.'.format(customer_id,
                                                    coupon_data.unique_service_coupon)
        return {'status': True, 'message': message}
    else:
        message = 'No coupon in progress for customerID {0}.'.format(customer_id) 
        return {'status': False, 'message': message}

def get_customer_info(data):
    try:
        product_obj = models.ProductData.objects.get(product_id=data['vin'])
    except Exception as ex:
        logger.info(ex)
        message = '''VIN '{0}' does not exist in our records. Please contact customer support: +91-9741775128.'''.format(data['vin'])
        if data['groups'][0] == "dealers":
            data['groups'][0] = "Dealer"
        else:
            data['groups'][0] = "ASC"
        template = get_email_template('VIN DOES NOT EXIST')['body'].format(data['current_user'], data['vin'], data['groups'][0])
        send_mail_when_vin_does_not_exist(data=template)
        return {'message': message, 'status': 'fail'}
    if product_obj.purchase_date:
        product_data = format_product_object(product_obj)
        return product_data
    else:
        message = '''VIN '{0}' has no associated customer. Please register the customer.'''.format(data['vin'])
        return {'message': message}


@login_required()
def exceptions(request, exception=None):
    groups = utils.stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        template = 'portal/exception.html'
        data = None
        if exception in ['close', 'check']:
            data = models.ServiceAdvisor.objects.active_under_dealer(request.user)
        return render(request, template, {'active_menu': exception,
                                           "data": data, 'groups': groups})
    elif request.method == 'POST':
        function_mapping = {
            'customer': get_customer_info,
            'recover': recover_coupon_info,
            'search': utils.search_details,
            'status': utils.services_search_details,
            'serviceadvisor': utils.service_advisor_search
        }
        try:
            post_data = request.POST.copy()
            post_data['current_user'] = request.user
            post_data['groups'] = groups
            if request.FILES:
                post_data['job_card']=request.FILES['jobCard']
            data = function_mapping[exception](post_data)
            return HttpResponse(content=json.dumps(data),  content_type='application/json')
        except Exception as ex:
            logger.error(ex)
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@check_service(Services.FREE_SERVICE_COUPON)
@login_required()
def users(request, users=None):
    groups = utils.stringify_groups(request.user)
    if not ('ascs' in groups or 'dealers' in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        template = 'portal/users.html'
        data=None
        data_mapping = {
            'sa': utils.get_sa_list_for_login_dealer,
            'asc': utils.get_asc_list_for_login_dealer
        }
        try:
            data = data_mapping[users](request.user)
        except:
            #It is acceptable if there is no data_mapping defined for a function
            pass
        return render(request, template, {'active_menu' : users, "data" : data, 'groups': groups})
    else:
        return HttpResponseBadRequest()

@check_service(Services.FREE_SERVICE_COUPON)
@login_required()
def get_sa_under_asc(request, id=None):
    template = 'portal/sa_list.html'
    data = None
    try:
        data = utils.get_sa_list_for_login_dealer(id)
    except:
            #It is acceptable if there is no data_mapping defined for a function
        pass
    return render(request, template, {'active_menu':'sa',"data": data})

def get_feedbacks(user, status, priority, type, search=None):
    group = user.groups.all()[0]
    feedbacks = []
    if type == ALL or type is None:
        type_filter = utils.get_list_from_set(FEEDBACK_TYPE)
    else:
        type_filter = [type]
    
    if priority == ALL or priority is None:
        priority_filter = utils.get_list_from_set(PRIORITY)
    else:
        priority_filter = [priority]
            
    if status is None or status == 'active':
        status_filter = ['Open', 'Pending', 'In Progress']
    else:
        if status == ALL:
            status_filter = utils.get_list_from_set(FEEDBACK_STATUS)
        else:
            status_filter = [status]

    if group.name == DEALER:
        sa_list = models.ServiceAdvisor.objects.active_under_dealer(user)
        if sa_list:
            sa_id_list = []
            for sa in sa_list:
                sa_id_list.append(sa.service_advisor_id)
            feedbacks = models.Feedback.objects.filter(reporter__name__in=sa_id_list, status__in=status_filter,
                                                       priority__in=priority_filter, type__in=type_filter
                                                    ).order_by('-created_date')
    if group.name == ASC:
        sa_list = models.ServiceAdvisor.objects.active_under_asc(user)
        if sa_list:
            sa_id_list = []
            for sa in sa_list:
                sa_id_list.append(sa.service_advisor_id)
            feedbacks = models.Feedback.objects.filter(reporter__name__in=sa_id_list, status__in=status_filter,
                                                       priority__in=priority_filter, type__in=type_filter
                                                    ).order_by('-created_date')
    if group.name == SDM:
        feedbacks = models.Feedback.objects.filter(status__in=status_filter, priority__in=priority_filter,
                                                   type__in=type_filter).order_by('-created_date')
    if group.name == SDO:
        user_profile = models.UserProfile.objects.filter(user=user)
        servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile=user_profile[0])
        feedbacks = models.Feedback.objects.filter(assignee=servicedesk_user[0], status__in=status_filter,
                                                   priority__in=priority_filter, type__in=type_filter).order_by('-created_date')
    
    return feedbacks


@check_service(Services.SERVICE_DESK)
@login_required()
def service_desk(request):
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    type = request.GET.get('type')
    search = request.GET.get('search')
    count = request.GET.get('count') or BY_DEFAULT_RECORDS_PER_PAGE
    page_details = {}
    feedback_obects = get_feedbacks(request.user, status, priority, type, search)
    paginator = Paginator(feedback_obects, count)
    page = request.GET.get('page', 1)
    feedbacks = paginator.page(page)
    page_details['total_objects'] = paginator.count
    page_details['from'] = feedbacks.start_index()
    page_details['to'] = feedbacks.end_index()
    groups = utils.stringify_groups(request.user)
    if request.method == 'GET':
        template = 'portal/feedback_details.html'
        data = None
        if request.user.groups.filter(name=DEALER).exists():
            data = models.ServiceAdvisor.objects.active_under_dealer(request.user)
        else:
            data = models.ServiceAdvisor.objects.active_under_asc(request.user)
        return render(request, template, {"feedbacks" : feedbacks,
                                          'active_menu': 'support',
                                          "data": data, 'groups': groups,
                                          "status": utils.get_list_from_set(FEEDBACK_STATUS),
                                          "pagination_links": PAGINATION_LINKS,
                                          "page_details": page_details,
                                          "record_showing_counts": RECORDS_PER_PAGE,
                                          "types": utils.get_list_from_set(FEEDBACK_TYPE),
                                          "priorities": utils.get_list_from_set(PRIORITY),
                                          "filter_params": {'status': status, 'priority': priority, 'type': type,
                                                            'count': str(count), 'search': search}},
                                          context_instance=RequestContext(request)
                                        )
    elif request.method == 'POST':
        try:
            data = save_help_desk_data(request)
            return HttpResponse(content=json.dumps(data),
                                content_type='application/json')
        except Exception as ex:
            logger.error('Exception while saving data : {0}'.format(ex))
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@login_required()
def enable_servicedesk(request, servicedesk=None):
    if settings.ENABLE_SERVICE_DESK:
        response = service_desk(request, servicedesk)
        return response
    else:
        return HttpResponseRedirect('http://support.gladminds.co/')

def save_help_desk_data(request):
    fields = ['description', 'advisorMobile', 'type', 'summary']
    sms_dict = {}
    for field in fields:
        sms_dict[field] = request.POST.get(field, None)
    service_advisor_obj = models.ServiceAdvisor.objects.get(user__phone_number=sms_dict['advisorMobile'])
    if request.user.groups.all()[0].name == DEALER:
        dealer_obj = models.Dealer.objects.get(dealer_id=request.user)
        email_id =  dealer_obj.user.user.email
    else:
        asc_obj = models.AuthorizedServiceCenter.objects.get(asc_id=request.user)
        email_id =  asc_obj.user.user.email
    return gladmindsResources.get_complain_data(sms_dict, service_advisor_obj.user.phone_number,
                                                service_advisor_obj.user.user.email,
                                                service_advisor_obj.user.user.username, email_id,
                                                with_detail=True)


def sqs_tasks_view(request):
    return render_to_response('trigger-sqs-tasks.html')


def trigger_sqs_tasks(request):
    sqs_tasks = {
        'send-feed-mail': 'send_report_mail_for_feed',
        'export-coupon-redeem': 'export_coupon_redeem_to_sap',
        'expire-service-coupon': 'expire_service_coupon',
        'send-reminder': 'send_reminder',
        'export-customer-registered': 'export_customer_reg_to_sap',
        'send_reminders_for_servicedesk': 'send_reminders_for_servicedesk'
    }

    taskqueue = SqsTaskQueue(settings.SQS_QUEUE_NAME)
    taskqueue.add(sqs_tasks[request.POST['task']])
    return HttpResponse()


def site_info(request):
    if request.method != 'GET':
        raise Http404
    brand = settings.BRAND
    return HttpResponse(json.dumps({'brand': brand}), content_type='application/json')


@check_service(Services.FREE_SERVICE_COUPON)
@login_required()
def reports(request):
    groups = utils.stringify_groups(request.user)
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
    user = models.Dealer.objects.filter(dealer_id=user)
    args = { Q(status=4) | Q(status=2) | Q(status=6)}
    status = query_params.get('status')
    from_date = query_params.get('from')
    to_date = query_params.get('to')
    filter['actual_service_date__range'] = (str(from_date) + ' 00:00:00', str(to_date) +' 23:59:59')
    if status:
        args = { Q(status=status) }
        if status=='2':
            args = { Q(status=2) | Q(status=6)}   
    all_coupon_data = models.CouponData.objects.filter(*args, **filter).order_by('-actual_service_date')
    map_status = {'6': 'Closed', '4': 'In Progress', '2':'Closed'}
    for coupon_data in all_coupon_data:
        coupon_data_dict = {}
        coupon_data_dict['vin'] = coupon_data.product.product_id
        user = coupon_data.service_advisor
        coupon_data_dict['sa_phone_name'] = user.user.phone_number
        coupon_data_dict['service_avil_date'] = coupon_data.actual_service_date
        coupon_data_dict['closed_date'] = coupon_data.closed_date
        coupon_data_dict['service_status'] = map_status[str(coupon_data.status)]
        if query_params['type']== 'credit':
            product_details = coupon_data.product
            coupon_data_dict['customer_name'] = product_details.customer_name
            coupon_data_dict['customer_number'] = product_details.customer_phone_number
            coupon_data_dict['credit_date'] = coupon_data.credit_date
            coupon_data_dict['credit_note'] = coupon_data.credit_note
        else:
            coupon_data_dict['customer_id'] = coupon_data.product.customer_id
            coupon_data_dict['product_type'] = coupon_data.product.product_type
            coupon_data_dict['coupon_no'] = coupon_data.unique_service_coupon
            coupon_data_dict['kms'] = coupon_data.actual_kms
            coupon_data_dict['service_type'] = coupon_data.service_type
            coupon_data_dict['special_case'] = coupon_data.special_case
        report_data.append(coupon_data_dict)
    return report_data

@check_service(Services.FREE_SERVICE_COUPON)
def brand_details(requests, role=None):
    data = requests.GET.copy()
    data_list = []
    data_dict = {}
    limit = data.get('limit', 20)
    offset = data.get('offset', 0)
    limit = int(limit)
    offset = int(offset)
    function_mapping = {
            'asc': get_asc_info,
            'sa': get_sa_info,
            'customers': get_customers_info,
            'active-asc': get_active_asc_info,
            'not-active-asc': get_not_active_asc_info
        }
    get_data = requests.GET
    data = function_mapping[role](data, limit, offset , data_dict, data_list)
    return HttpResponse(json.dumps(data), mimetype="application/json")

#FIXME: Fix this according to new model
def get_asc_info(data, limit, offset, data_dict, data_list):
    '''get city and state from parameter'''
    asc_details = {}
    if data.has_key('city') and data.has_key('state'):
        asc_details['address'] = ', '.join([data['city'].upper(), data['state'].upper()])
    asc_details['role'] = 'asc'
    asc_data = models.Dealer.objects.filter(**asc_details)
    data_dict['total_count'] = len(asc_data)
    for asc in asc_data[offset:limit]:
        asc_detail = OrderedDict();
        asc_detail['id'] = asc.dealer_id
        asc_detail['address'] = asc.address
        utils.get_state_city(asc_detail, asc.address)
        data_list.append(asc_detail)
    data_dict['asc'] = data_list
    return data_dict

#FIXME: Fix this according to new model
def get_sa_info(data, limit, offset, data_dict, data_list):
    sa_details = {}
    if data.has_key('phone_number'):
        sa_details['phone_number'] = utils.mobile_format(str(data['phone_number']))
    sa_data = models.ServiceAdvisor.objects.filter(**sa_details)
    data_dict['total_count'] = len(sa_data)
    for sa in sa_data[offset:limit]:
        sa_detail = OrderedDict();
        sa_detail['id'] = sa.service_advisor_id
        sa_detail['name'] = sa.name
        sa_detail['phone_number'] = sa.phone_number
        sa_detail = get_sa_details(sa_detail, sa)
        data_list.append(sa_detail)
    data_dict['sa'] = data_list
    return data_dict

#FIXME: Fix this according to new model
def get_customers_info(data, limit, offset, data_dict, data_list):
    kwargs = {}
    if data.has_key('sap_id'):
        kwargs['sap_customer_id'] = data['sap_id']
    args = {~Q(product_purchase_date=None)}
    customer_products = models.ProductData.objects.filter(*args, **kwargs)[offset:limit]
    for customer in customer_products:
        customer_detail = OrderedDict();
        customer_detail['sap_id'] = customer.sap_customer_id
        customer_detail['gcp_id'] = customer.customer_phone_number.gladmind_customer_id
        customer_detail['vin'] = customer.vin
        customer_detail['name'] = customer.customer_phone_number.customer_name
        customer_detail['phone_number'] = customer.customer_phone_number.phone_number
        customer_detail['email_id'] = customer.customer_phone_number.email_id
        customer_detail['address'] = customer.customer_phone_number.address
        customer_detail = utils.get_state_city(customer_detail, customer_detail['address'])
        data_list.append(customer_detail)
    data_dict['customers'] = data_list
    return data_dict


#FIXME: Fix this according to new model
def get_active_asc_info(data, limit, offset, data_dict, data_list):
    '''get city and state from parameter'''
    asc_details = utils.get_asc_data(data)
    active_asc_list = asc_details.filter(~Q(date_joined=F('last_login')))
    active_ascs = active_asc_list.values_list('username', flat=True)
    asc_obj = models.Dealer.objects.filter(dealer_id__in=active_ascs)
    for asc_data in asc_obj[offset:limit]:
        active_ascs = OrderedDict();
        active_ascs['id'] = asc_data.dealer_id
        active_ascs['address'] = asc_data.address
        active_ascs = utils.get_state_city(active_ascs, asc_data.address)
        active_ascs['coupon_closed'] = utils.asc_cuopon_data(asc_data, 2)
        active_ascs['coupon_inprogress'] = utils.asc_cuopon_data(asc_data, 4)
        active_ascs['coupon_closed_old_fsc'] = utils.asc_cuopon_data(asc_data, 6)
        data_list.append(active_ascs)
    data_dict['count'] = len(active_asc_list)
    data_dict['active-asc'] = data_list
    return data_dict

#FIXME: Fix this according to new model
@check_service(Services.FREE_SERVICE_COUPON)
def get_active_asc_report(request):
    '''get city and state from parameter'''
    data = request.GET.copy()
    if data.has_key('month') and data.has_key('month') :
        month = MONTHS.index(data['month']) + 1
        year = data['year']
    else:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
    data_list = []
    asc_details = utils.get_asc_data(data)
    active_asc_list = asc_details.filter(~Q(date_joined=F('last_login')))
    active_ascs = active_asc_list.values_list('username', flat=True)
    asc_obj = models.Dealer.objects.filter(dealer_id__in=active_ascs)
    for asc_data in asc_obj:
        active_ascs = OrderedDict();
        active_ascs['id'] = asc_data.dealer_id
        active_ascs['address'] = asc_data.address
        active_ascs = utils.get_state_city(active_ascs, asc_data.address)
        active_ascs['coupon_closed'] = utils.asc_cuopon_details(asc_data, 2, year, month)
        data_list.append(active_ascs)
    years = utils.gernate_years()

    return render(request, 'portal/asc_report.html',\
                  {"data": data_list,
                   "range": range(1,32),
                   "month": MONTHS,
                   "year": years,
                   "mon": MONTHS[month-1]
                   })
    
#FIXME: Fix this according to new model
def get_not_active_asc_info(data, limit, offset, data_dict, data_list):
    '''get city and state from parameter'''
    asc_details = utils.get_asc_data(data)
    not_active_asc_list = asc_details.filter(date_joined=F('last_login'))
    not_active_ascs = not_active_asc_list.values_list('username', flat=True)
    not_asc_obj = models.Dealer.objects.filter(dealer_id__in=not_active_ascs)
    for asc in not_asc_obj[offset:limit]:
        not_active_ascs = OrderedDict();
        not_active_ascs['id'] = asc.dealer_id
        not_active_ascs['address'] = asc.address
        not_active_ascs = utils.get_state_city(not_active_ascs, asc.address)
        data_list.append(not_active_ascs)
    data_dict['count'] = len( not_active_asc_list)
    data_dict['not-active-asc'] = data_list
    return data_dict

#FIXME: Fix this according to new model
def get_sa_details(sa_details, id):
    sa_detail = models.ServiceAdvisor.objects.filter(service_advisor_id=id)
    if sa_detail:
        sa_dealer_details = models.Dealer.objects.get(id=sa_detail[0].dealer_id.id)
        if sa_dealer_details.role == None:
            sa_details['dealer'] = sa_dealer_details.dealer_id
        else:
            sa_details['asc'] = sa_dealer_details.dealer_id
    else:
        sa_details['dealer/asc'] = 'Null'
    return sa_details
