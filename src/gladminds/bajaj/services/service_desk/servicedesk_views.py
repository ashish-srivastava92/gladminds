import logging
import json
from django.http.response import HttpResponse, HttpResponseBadRequest,\
    HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.sites.models import get_current_site
from gladminds.core.constants import BY_DEFAULT_RECORDS_PER_PAGE,\
    FEEDBACK_STATUS, PAGINATION_LINKS, RECORDS_PER_PAGE, FEEDBACK_TYPE, PRIORITY,\
    ROOT_CAUSE
from gladminds.core.auth.service_handler import check_service_active, Services
from gladminds.core import utils
from gladminds.core.auth_helper import Roles
from gladminds.bajaj import models
from gladminds.core.utils import get_list_from_set
import datetime
from gladminds.bajaj.services.service_desk.servicedesk_manager import get_feedbacks,\
    get_complain_data, get_feedback, get_servicedesk_users, get_comments,\
    save_update_feedback, update_feedback_activities, SDActions

LOG = logging.getLogger('gladminds')

@check_service_active(Services.SERVICE_DESK)
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
        if request.user.groups.filter(name=Roles.DEALERS).exists():
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
                                                            'count': str(count), 'search': search}}
                                        )
    elif request.method == 'POST':
        try:
            data = save_help_desk_data(request)
            return HttpResponse(content=json.dumps(data),
                                content_type='application/json')
        except Exception as ex:
            LOG.error('Exception while saving data : {0}'.format(ex))
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@login_required()
def enable_servicedesk(request):
    if settings.ENABLE_SERVICE_DESK:
        response = service_desk(request)
        return response
    else:
        return HttpResponseRedirect('http://support.gladminds.co/')

def save_help_desk_data(request):
    fields = ['description', 'advisorMobile', 'type', 'summary']
    sms_dict = {}
    for field in fields:
        sms_dict[field] = request.POST.get(field, None)
    if request.FILES:
        sms_dict['file_location'] =  request.FILES['sdFile']
    else:
        sms_dict['file_location'] = None
    service_advisor_obj = models.ServiceAdvisor.objects.get(user__phone_number=sms_dict['advisorMobile'])
    if request.user.groups.filter(name=Roles.DEALERS).exists():
        dealer_asc_obj = models.Dealer.objects.get(dealer_id=request.user)
    else:
        dealer_asc_obj = models.AuthorizedServiceCenter.objects.get(asc_id=request.user)
        
    if dealer_asc_obj.user.user.email:
        dealer_asc_email = dealer_asc_obj.user.user.email
    else:
        dealer_asc_email = None
    return get_complain_data(sms_dict, service_advisor_obj.user.phone_number,
                                                service_advisor_obj.user.user.email,
                                                service_advisor_obj.user.user.username, dealer_asc_email,
                                                with_detail=True)

@check_service_active(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["GET"])
def get_servicedesk_tickets(request):
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

@check_service_active(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["GET", "POST"])
def modify_servicedesk_tickets(request, feedback_id):
    host = get_current_site(request)
    group_name = request.user.groups.filter(name__in=[Roles.SDMANAGERS, Roles.SDOWNERS, Roles.DEALERS, Roles.ASCS])
    status = get_list_from_set(FEEDBACK_STATUS)
    priority_types = get_list_from_set(PRIORITY)
    feedback_types = get_list_from_set(FEEDBACK_TYPE)
    root_cause = get_list_from_set(ROOT_CAUSE)
    feedback_obj = get_feedback(feedback_id, request.user)
    servicedesk_users = get_servicedesk_users(designation=Roles.SDOWNERS)
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

@check_service_active(Services.SERVICE_DESK)
@login_required()
@require_http_methods(["POST"])
def modify_feedback_comments(request, feedback_id, comment_id):
    data = request.POST
    feedback_obj = models.Feedback.objects.get(id=feedback_id)
    try:
        comment = models.Comment.objects.get(feedback_object_id=feedback_id, id=comment_id)
        previous_comment = comment.comment
        comment.comment = data['commentDescription']
        comment.modified_date = datetime.datetime.now()
        comment.save()
        update_feedback_activities(feedback_obj, SDActions.COMMENT_UPDATE, previous_comment, data['commentDescription'])
        return HttpResponse("Success")

    except Exception as ex:
        LOG.info("[Exception comment not found]: {0}".format(ex))
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
