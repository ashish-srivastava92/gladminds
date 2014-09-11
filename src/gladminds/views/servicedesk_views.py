import logging


from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings

from gladminds.utils import get_list_from_set
from gladminds.aftersell.models import common as aftersell_common
from gladminds.resource.resources import GladmindsResources
from gladminds.constants import FEEDBACK_STATUS, PRIORITY, FEEDBACK_TYPE,\
    ROOT_CAUSE
from gladminds.managers import get_feedbacks, get_feedback,\
    get_servicedesk_users, save_update_feedback
from django.views.decorators.http import require_http_methods
from django.contrib.sites.models import get_current_site

gladmindsResources = GladmindsResources()
logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX


@login_required()
@require_http_methods(["GET"])
def get_servicedesk_tickets(request):
    return render(request, 'service-desk/tickets.html',\
                  {"feedbacks": get_feedbacks(request.user)})


@login_required()
@require_http_methods(["GET", "POST"])
def modify_servicedesk_tickets(request, feedback_id):
    host = get_current_site(request)
    group_name = request.user.groups.all()
    status = get_list_from_set(FEEDBACK_STATUS)
    priority_types = get_list_from_set(PRIORITY)
    feedback_types = get_list_from_set(FEEDBACK_TYPE)
    root_cause = get_list_from_set(ROOT_CAUSE)
    feedback_obj = get_feedback(feedback_id, request.user)
    servicedesk_users = get_servicedesk_users(designation='SDO')
    if request.method == 'POST':
        host = request.get_host()
        save_update_feedback(feedback_obj[0], request.POST, request.user, host)
    if feedback_obj:
        return render(request, 'service-desk/ticket_modify.html',\
                  {"feedback": feedback_obj[0], "FEEDBACK_STATUS": status,\
                   "PRIORITY": priority_types,\
                    "FEEDBACK_TYPE": feedback_types,\
                    "ROOT_CAUSE" : root_cause,\
                   "group": group_name[0].name,\
                   'servicedeskuser': servicedesk_users,
                   })
    else:
        return HttpResponseNotFound()


@require_http_methods(["POST"])
def get_feedback_response(request, feedback_id):
        data = request.POST
        if data['feedbackresponse']:
            aftersell_common.Feedback.objects.filter(
                  id=feedback_id).update(ratings=str(data['feedbackresponse']))
            return render(request, 'service-desk/feedback_received.html')
        else:
            return HttpResponse()
