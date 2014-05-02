from django.shortcuts import render_to_response, render
from django.contrib.auth.views import login_required
from django.template import RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from gladminds.models import common
import logging
from gladminds.tasks import send_otp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from gladminds import utils, message_template
logger = logging.getLogger('gladminds')


def generate_otp(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST['mobile']
            email = request.POST.get('email', '')
            token = utils.get_token(phone_number, email=email)
            message = message_template.get_template('SEND_OTP').format(token)
            send_otp.delay(phone_number=phone_number, message=message)
            return HttpResponseRedirect('/users/otp/validate?phone='+phone_number)
        except:
            return HttpResponseRedirect('/users/otp/generate?details=invalid')
    elif request.method == 'GET':
        return render_to_response('portal/get_otp.html', context_instance=RequestContext(request))

def validate_otp(request):
    if request.method == 'GET':
        return render_to_response('portal/validate_otp.html', context_instance=RequestContext(request))
    elif request.method == 'POST':
        try:
            otp = request.POST['otp']
            phone_number = request.POST['phone']
            utils.validate_otp(otp, phone_number)
            return render_to_response('portal/reset_pass.html', {'otp': otp}, context_instance=RequestContext(request))
        except:
            return HttpResponseRedirect('/users/otp/generate?token=invalid')

def update_pass(request):
    try:
        otp=request.POST['otp']
        password=request.POST['password']
        utils.update_pass(otp, password)
        return HttpResponseRedirect('/dealers/?update=true')
    except:
        return HttpResponseRedirect('/dealers/?error=true')

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

