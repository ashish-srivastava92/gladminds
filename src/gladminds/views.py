from django.shortcuts import render_to_response
from django.contrib.auth.views import login_required
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect
from gladminds.models import common
from reportlab.graphics.shapes import NotImplementedError

@login_required(login_url='/dealers/')
def action(request, params):
    if request.method == 'GET':
        service_advisors = common.ServiceAdvisorDealerRelationship.objects.filter(dealer_id=request.user, status='Y')
        sa_phone_list = []
        for service_advisor in service_advisors:
            sa_phone_list.append(service_advisor.service_advisor_id)
        return render_to_response('dealer/advisor_actions.html', {'phones' : sa_phone_list}\
                                  , context_instance=RequestContext(request))
    elif request.method == 'POST':
        NotImplementedError()
    
@login_required(login_url='/dealers/')
def redirect(request):
    return HttpResponseRedirect('/dealers/' + str(request.user))