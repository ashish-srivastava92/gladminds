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
from django.conf import settings
from gladminds.sqs_tasks import export_asc_registeration_to_sap
logger = logging.getLogger('gladminds')


def generate_otp(request):
    if request.method == 'POST':
        try:
            phone_number = request.POST['mobile']
            email = request.POST.get('email', '')
            token = utils.get_token(phone_number, email=email)
            message = message_template.get_template('SEND_OTP').format(token)
            send_otp.delay(phone_number=phone_number, message=message)
            return render_to_response('portal/validate_otp.html', {'phone': phone_number}, context_instance=RequestContext(request))
        except:
            return HttpResponse('Invalid Details')
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
            return HttpResponse('Invalid Token')

def update_pass(request):
    try:
        otp=request.POST['otp']
        password=request.POST['password']
        utils.update_pass(otp, password)
        return HttpResponse('OK')
    except:
        return HttpResponse('Invalid Data')

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


def save_asc_registeration(data, brand='bajaj'):
    if common.RegisteredASC.objects.filter(phone_number=data['mobile_number'])\
        or common.ASCSaveForm.objects.filter(phone_number=data['mobile_number']):
        return {"message": "Already Registered Number"}

    try:
        dealer_data = common.RegisteredDealer.objects.\
                                            filter(dealer_id=data["dealer_id"])
        dealer_data = dealer_data if dealer_data else None
        print "###########",
        print data['name']
        asc_obj = common.ASCSaveForm(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['mobile_number'], email=data['email'],
                 pincode=data['pincode'], status=1, dealer_id=dealer_data)
        asc_obj.save()
        print "@@@@@@@"
        if settings.ENABLE_AMAZON_SQS:
            task_queue = utils.get_task_queue()
            task_queue.add("export_asc_registeration_to_sap", \
               {"phone_number": data['phone_number'], "brand": brand})
        else:
            export_asc_registeration_to_sap.delay(phone_number=data[
                                        'phone_number'], brand=brand)
        print "$$$$$$$$$$$$"
#     except KeyError:
#         return {"message": "Key error"}
    except Exception as ex:
        logger.info(ex)
    return {"message": PASSED_MESSAGE}


def register_user(request, user=None):
    save_user = {
        'asc': save_asc_registeration
    }
    status = save_user[user](request.POST)
    return HttpResponseRedirect("/register/asc/")
    return HttpResponse({"status": status}, content_type="application/json")
