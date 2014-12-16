import logging
import datetime

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.sites.models import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gladminds.core import utils
from gladminds.core.utils import get_list_from_set, convert_utc_to_local_time
from gladminds.bajaj import models as models
from gladminds.bajaj.services.free_service_coupon import GladmindsResources
from gladminds.core.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    ROOT_CAUSE, SDM, SDO, DEALER, PAGINATION_LINKS, BY_DEFAULT_RECORDS_PER_PAGE, RECORDS_PER_PAGE,\
    ASC
from gladminds.managers import get_feedback,\
    get_servicedesk_users, save_update_feedback, get_comments
from gladminds.core.managers.audit_manager import sms_log
from gladminds.bajaj.services import message_template as templates
from gladminds.sqs_tasks import send_coupon
from gladminds.core.decorator import check_service
from gladminds.core.service_handler import Services

from gladminds.core.views.views import get_feedbacks
from django.template.context import RequestContext


gladmindsResources = GladmindsResources()
logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX



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
                                                            'count': str(count), 'search': search}},
                                         context_instance=RequestContext(request)
                                        )

@check_service(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["GET", "POST"])
def modify_servicedesk_tickets(request, feedback_id):
    host = get_current_site(request)
    group_name = request.user.groups.filter(name__in=[SDM, SDO, DEALER, ASC])
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
