import logging
import datetime

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.sites.models import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from tastypie.resources import Resource

from gladminds.core import utils
from gladminds.core.utils import get_list_from_set, convert_utc_to_local_time
from gladminds.bajaj import models as models
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    ROOT_CAUSE, SDM, SDO, DEALER, PAGINATION_LINKS, BY_DEFAULT_RECORDS_PER_PAGE, RECORDS_PER_PAGE
from gladminds.managers import get_feedback,\
    get_servicedesk_users, save_update_feedback, get_comments
from gladminds.core.managers.audit_manager import sms_log
from gladminds.bajaj.services import message_template as templates
from gladminds.bajaj.services.free_service_coupon import FSCResources
from gladminds.sqs_tasks import send_coupon
from gladminds.core.decorator import check_service
from gladminds.core.service_handler import Services
from gladminds.core.managers.mail import send_feedback_received,\
     send_servicedesk_feedback, send_dealer_feedback
from gladminds.managers import get_reporter_details
from gladminds.core.constants import PROVIDER_MAPPING, PROVIDERS, GROUP_MAPPING,\
    USER_GROUPS, REDIRECT_USER, TEMPLATE_MAPPING, ACTIVE_MENU, MONTHS,\
    FEEDBACK_STATUS, FEEDBACK_TYPE, PRIORITY, ALL, DEALER, SDO, SDM

logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX

def get_feedbacks(user, status, priority, type, search=""):
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
    
    if status is None:
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
    if group.name == SDM:
        feedbacks = models.Feedback.objects.filter(status__in=status_filter, priority__in=priority_filter,
                                                   type__in=type_filter).order_by('-created_date')
    if group.name == SDO:
        user_profile = models.UserProfile.objects.filter(user=user)
        servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile=user_profile[0])
        feedbacks = models.Feedback.objects.filter(assignee=servicedesk_user[0], status__in=status_filter,
                                                   priority__in=priority_filter,
                                                   type__in=type_filter).order_by('-created_date')

    return feedbacks

@check_service(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["GET"])
def get_servicedesk_tickets(request):
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    type = request.GET.get('type')
    search = request.GET.get('search')
    count = request.GET.get('count') or BY_DEFAULT_RECORDS_PER_PAGE
    page_details = {}
    if search:
        feedback_obects = get_feedbacks(request.user, status, priority, type, search)
    else:
        feedback_obects = get_feedbacks(request.user, status, priority, type)
    paginator = Paginator(feedback_obects, count)
    page = request.GET.get('page')
    try:
        feedbacks = paginator.page(page)
    except PageNotAnInteger:
        feedbacks = paginator.page(1)
    except EmptyPage:
        feedbacks = paginator.page(paginator.num_pages)
    
    page_details['total_objects'] = paginator.count
    page_details['from'] = feedbacks.start_index()
    page_details['to'] = feedbacks.end_index()
        
    return render(request, 'service-desk/tickets.html', {"feedbacks" : feedbacks,
                                          "status": utils.get_list_from_set(FEEDBACK_STATUS),
                                          "types": utils.get_list_from_set(FEEDBACK_TYPE),
                                          "priorities": utils.get_list_from_set(PRIORITY),
                                          "pagination_links": PAGINATION_LINKS,
                                          "page_details": page_details,
                                          "record_showing_counts": RECORDS_PER_PAGE,
                                          "filter_params": {'status': status, 'priority': priority, 'type': type,
                                                            'count': str(count), 'search': search}}
                                        )

@check_service(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["GET", "POST"])
def modify_servicedesk_tickets(request, feedback_id):
    host = get_current_site(request)
    group_name = request.user.groups.filter(name__in=[SDM, SDO, DEALER])
    status = get_list_from_set(FEEDBACK_STATUS)
    priority_types = get_list_from_set(PRIORITY)
    feedback_types = get_list_from_set(FEEDBACK_TYPE)
    root_cause = get_list_from_set(ROOT_CAUSE)
    feedback_obj = get_feedback(feedback_id, request.user)
    servicedesk_users = get_servicedesk_users(designation=SDO)
    comments = get_comments(feedback_id)
    
    if request.method == 'POST':
        host = request.get_host()
        save_update_feedback(feedback_obj, request.POST, request.user, host)
    if feedback_obj:
        return render(request, 'service-desk/ticket_modify.html',\
                  {"feedback": feedback_obj, "FEEDBACK_STATUS": status,\
                   "PRIORITY": priority_types,\
                    "FEEDBACK_TYPE": feedback_types,\
                    "ROOT_CAUSE" : root_cause,\
                   "group": group_name[0].name,\
                   'servicedeskuser': servicedesk_users,\
                   'comments': comments,\
                   'user':request.user 
                   })
    else:
        return HttpResponseNotFound()

@check_service(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["POST"])
def modify_feedback_comments(request, feedback_id, comment_id):
    data = request.POST
    try:
        comment = models.Comment.objects.get(feedback_object_id=feedback_id, id=comment_id)
        comment.comment = data['commentDescription']
        comment.modified_date = datetime.datetime.now() 
        comment.save()
        return HttpResponse("Success")

    except Exception as ex:
        logger.info("[Exception comment not found]: {0}".format(ex))
        return HttpResponseNotFound()
    
    
@require_http_methods(["POST"])
def get_feedback_response(request, feedback_id):
        data = request.POST
        if data['feedbackresponse']:
            models.Feedback.objects.filter(
                  id=feedback_id).update(ratings=str(data['feedbackresponse']))
            return render(request, 'service-desk/feedback_received.html')
        else:
            return HttpResponse()
        
def send_feedback_sms(template_name, phone_number, feedback_obj, comment_obj=None):
    created_date = feedback_obj.created_date
    try:
        message = templates.get_template(template_name).format(type=feedback_obj.type,
                                                               reporter=feedback_obj.reporter,
                                                               message=feedback_obj.message,
                                                               created_date=convert_utc_to_local_time(created_date),
                                                               assign_to=feedback_obj.assign_to,
                                                               priority=feedback_obj.priority)
        if comment_obj and template_name == 'SEND_MSG_TO_ASSIGNEE':
            message = message + 'Note :' + comment_obj.comments
    except Exception as ex:
        message = templates.get_template('SEND_INVALID_MESSAGE')
    finally:
        logger.info("Send complain message received successfully with %s" % message)
        phone_number = utils.get_phone_number_format(phone_number)
        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("send_coupon", {"phone_number":phone_number, "message": message})
        else:
            send_coupon.delay(phone_number=phone_number, message=message)
    sms_log(receiver=phone_number, action='SEND TO QUEUE', message=message)
    return {'status': True, 'message': message}


__all__ = ['GladmindsTaskManager']
AUDIT_ACTION = 'SEND TO QUEUE'
angular_format = lambda x: x.replace('{', '<').replace('}', '>')


class SDResources(Resource):

    class Meta:
        resource_name = 'handler'
        
    def get_complain_data(self, sms_dict, phone_number, email, name, dealer_email, with_detail=False):
        ''' Save the feedback or complain from SA and sends SMS for successfully receive '''
        manager_obj = User.objects.get(groups__name='SDM')
        try:
            role = self.check_role_of_initiator(phone_number)
            user_profile = models.UserProfile.objects.filter(phone_number=phone_number)
            if len(user_profile)>0:
                servicedesk_user = models.ServiceDeskUser.objects.filter(user_profile=user_profile[0])
                if servicedesk_user:
                    servicedesk_user = servicedesk_user[0]
                else:
                    servicedesk_user = models.ServiceDeskUser(user_profile=user_profile[0], name=name)
                    servicedesk_user.save()
            else:
                servicedesk_user = models.ServiceDeskUser(name=name, phone_number=phone_number, email=email)
                servicedesk_user.save()
            if with_detail:
                gladminds_feedback_object = models.Feedback(reporter=servicedesk_user,
                                                                type=sms_dict['type'], 
                                                                summary=sms_dict['summary'], description=sms_dict['description'],
                                                                status="Open", created_date=datetime.now(),
                                                                role=role
                                                                )
            else:
                gladminds_feedback_object = models.Feedback(reporter=servicedesk_user,
                                                                message=sms_dict['message'], status="Open",
                                                                created_date=datetime.datetime.now(),
                                                                role=role
                                                                )
            gladminds_feedback_object.save()
            message = templates.get_template('SEND_RCV_FEEDBACK').format(type=gladminds_feedback_object.type)
        except Exception as ex:
            logger.error(ex)
            message = templates.get_template('SEND_INVALID_MESSAGE')
        finally:
            logger.info("Send complain message received successfully with %s" % message)
            phone_number = utils.get_phone_number_format(phone_number)
            if settings.ENABLE_AMAZON_SQS:
                task_queue = utils.get_task_queue()
                task_queue.add("send_coupon", {"phone_number":phone_number, "message": message})
            else:
                send_coupon.delay(phone_number=phone_number, message=message)
            context = utils.create_context('FEEDBACK_DETAIL_TO_DEALER',  gladminds_feedback_object)
            send_dealer_feedback(context, dealer_email)
            context = utils.create_context('FEEDBACK_DETAIL_TO_ADIM',  gladminds_feedback_object)
            send_feedback_received(context, manager_obj.email)
            context = utils.create_context('FEEDBACK_CONFIRMATION',  gladminds_feedback_object)
            send_servicedesk_feedback(context, get_reporter_details(gladminds_feedback_object.reporter,"email"))
            sms_log(receiver=phone_number, action=AUDIT_ACTION, message = message)
        return {'status': True, 'message': message}

    def check_role_of_initiator(self, phone_number):
        fsc_resource = FSCResources()
        active_sa = fsc_resource.validate_service_advisor(phone_number)
        if  active_sa:
            return "SA"
        else:
            check_customer_obj = models.ProductData.objects.filter(
                                            customer_phone_number=phone_number)
            if check_customer_obj:
                return "Customer"
            else:
                return "other"
