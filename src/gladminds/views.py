from django.shortcuts import render_to_response, render
from django.contrib.auth.views import login_required
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from gladminds.models import common
import logging

logger = logging.getLogger('gladminds')


@login_required(login_url='/dealers/')
def action(request, params):
    if request.method == 'GET':
        try:
            dealer = common.RegisteredDealer.objects.filter(
                dealer_id=request.user)[0]
            service_advisors = common.ServiceAdvisorDealerRelationship.objects\
                                        .filter(dealer_id=dealer, status='Y')
            sa_phone_list = []
            for service_advisor in service_advisors:
                sa_phone_list.append(service_advisor.service_advisor_id)
            return render_to_response('dealer/advisor_actions.html',
                  {'phones': sa_phone_list},
                  context_instance=RequestContext(request))
        except:
            logger.info(
                'No service advisor for dealer %s found active' % request.user)
            raise

    elif request.method == 'POST':
        raise NotImplementedError()


@login_required(login_url='/dealers/')
def redirect(request):
    return HttpResponseRedirect('/dealers/' + str(request.user))


def register(request, user=None):
    template_mapping = {
        "asc": "portal/asc_registration.html",
    }
    return render(request, template_mapping[user])

PASSED_MESSAGE = "Registration is complete"


def save_asc_registeration(data):
    reject_keys = ['csrfmiddlewaretoken']
    data = {key: val for key, val in data.iteritems() \
                                    if key not in reject_keys}
    try:
        asc_obj = common.ASCSaveForm(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone_number'], email=data['email'],
                 pincode=data['pincode'])
        asc_obj.save()

    except KeyError:
        return {"message": "Key error"}
    return {"message": PASSED_MESSAGE}


def register_user(request, user=None):
    save_user = {
        'asc': save_asc_registeration
    }
    status = save_user[user](request.POST)
    return HttpResponseRedirect("/register/asc/")
    return HttpResponse({"status": status}, content_type="application/json")
