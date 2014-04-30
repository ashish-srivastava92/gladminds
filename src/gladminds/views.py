from django.shortcuts import render_to_response, render
from django.contrib.auth.views import login_required
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from gladminds.models import common
import logging
from django.views.decorators.csrf import csrf_exempt
from django_otp.forms import OTPAuthenticationForm, OTPTokenForm
from functools import partial
from gladminds.tasks import send_otp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from gladminds.settings import TOTP_SECRET_KEY
from gladminds import utils
logger = logging.getLogger('gladminds')


def generate_otp(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST['mobile']
            email = request.POST.get('email', '')
            utils.get_token(phone_number, email)
        except:
            return HttpResponse('No')
    elif request.method == 'GET':
        return render_to_response('portal/get_otp.html', context_instance=RequestContext(request))


@login_required(login_url='/dealers/')
def action(request, params):
    if request.method == 'GET':
        try:
            dealer = common.RegisteredDealer.objects.filter(dealer_id=request.user)[0]
            service_advisors = common.ServiceAdvisorDealerRelationship.objects.filter(dealer_id=dealer, status='Y')
            sa_phone_list = []
            for service_advisor in service_advisors:
                sa_phone_list.append(service_advisor.service_advisor_id)
            return render_to_response('dealer/advisor_actions.html', {'phones' : sa_phone_list}\
                                      , context_instance=RequestContext(request))
        except:
            logger.info('No service advisor for dealer %s found active' % request.user)
            raise

    elif request.method == 'POST':
        raise NotImplementedError()

@login_required(login_url='/dealers/')
def redirect(request):
    return HttpResponseRedirect('/dealers/' + str(request.user))

def register(request, user=None):
    return render(request, 'portal/asc_registration.html')
#     return render_to_response('gladminds/asc_registration.html',\
#                               {}, context_instance=RequestContext(request))


def register_user(request, user=None):

    return HttpResponse("Do something")

def reset(request):
    if request.method=='GET':
        return render_to_response('reset_pass.html', context_instance=RequestContext(request))
    else:
        print "hello"


#def change_password(request):
#    old_password = request.POST.get('old_pwd')
#    new_password = request.POST.get('new_pwd')
#    user = User.objects.get(username=request.user)
#    if(check_password(old_password, user.password)):
#        user.set_password(new_password)
#        user.save()
#        return HttpResponse('success')
#    else:
#        return HttpResponse('password change failed')

