from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from gladminds.models import common,afterbuy_models
from gladminds import utils
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.context import RequestContext

@csrf_exempt
def home(request):
#     c = {}
#     c.update(csrf(request))
    return render_to_response('afterbuy/index.html')

'''
 method for login
'''
@csrf_exempt
def my_login(request):
#     c = {}
#     c.update(csrf(request))
    if request.POST.get('action')=='checkLogin':
        return check_login(request)
    elif request.POST.get('action')=='editSettings' :
        return HttpResponse(update_user_details(request))
    elif request.POST.get('action')=='feedback' :
        return send_feedback_response(request)
    else:
        return HttpResponse()
    

@csrf_exempt
def check_login(request):
    username = request.POST.get('txtUsername')
    password = request.POST.get('txtPassword')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_obj=User.objects.get(username=username)
            user_name=user_obj.username
            user_profile=common.GladMindUsers.objects.get(user=user)
            unique_id=user_profile.gladmind_customer_id
            id=user_profile.user_id
            response=HttpResponse(json.dumps({'status': 1,'id':id,'username':user_name,'unique_id':unique_id}))
        else:
            response=HttpResponse(json.dumps({'status': 0}))
    else:
       response=HttpResponse(json.dumps({'status': 0}))
    return response

@csrf_exempt
def update_user_details(request):
    user_id=request.POST.get('userID')
    if user_id:
        user_name=request.POST.get('txt_name', None)
        user_email=request.POST.get('txt_email', None)
        user_country=request.POST.get('txt_country', None)
        user_state=request.POST.get('txt_state', None)
        user_mobile_number=request.POST.get('txt_mob', None)
        user_dob=request.POST.get('txt_dob', None)
        user_interest=request.POST.get('txt_interest', None)
        user_address=request.POST.get('txt_address', None)
        user_gender=request.POST.get('txt_gender', None)
        try:
#             user_object=common.GladMindUsers.objects.get(user_id=user_id)
#             print "user_object is",user_object
# #                         update(customer_name=user_name,
# #                         email_id=user_email,
# #                         phone_number=user_mobile_number,
# #                         address=user_address,
# #                         country=user_country,
# #                         state=user_state,
# #                         dob=user_dob,
# #                         gender=user_gender)
#             user_object.user.username=user_name
#             user_object.user.email=user_email
#             unique_id=user_object.gladmind_customer_id
#             user_object.save()
            response=json.dumps({'status':" 1",'thumbURL':'','sourceURL':''})
        except:
            response=json.dumps({'status': 0})
    else:
        response=json.dumps({'status': 0})
    return response
        
@csrf_exempt
def send_feedback_response(request):
    #FIXME not saving feed back just sending the response
    user_id=request.POST.get('userID')
    return HttpResponse(json.dumps({"status":"1","message":"Success!","id":user_id}))   
    
    
@csrf_exempt
def app_logout(request):
    logout(request)
    return HttpResponse('logged out')

@csrf_exempt
def get_data(request):
    action= request.GET.get('action')
    if action=='getProfile':
        unique_id=request.GET.get('unique_id')
        user_profile=common.GladMindUsers.objects.get(gladmind_customer_id=unique_id)
        name=user_profile.user.username
        email=user_profile.user.email
        mobile=user_profile.phone_number
        address=user_profile.address
        country=user_profile.country
        state=user_profile.state
        return HttpResponse(json.dumps({'name':name,'email':email,'mobile':mobile,'address':address,
                                        'country':country,'state':state,'dob':'','gender':'',
                                        'Interests':''}))
        
    elif action=='getProducts':
        pass    
    

'''
method for creating new user and checking user 
is already exists or not
'''
from datetime import datetime
@csrf_exempt
def create_account(request):
    user_name=request.POST.get('txtName', None)
    user_email=request.POST.get('txtEmail', None)
    user_password= request.POST.get('txtPassword', None)
    user_country=request.POST.get('txtCountry', None)
    user_state=request.POST.get('txtState', None)
    user_mobile_number=request.POST.get('txtMobile', None)
    unique_id=''
    if check_email_id_exists(user_email):
        response= HttpResponse(json.dumps({'status': 2,'message':'Email already exists'}))
    else:
        try:
            unique_id='GMS17_'+str(utils.generate_unique_customer_id())
            gladmind_user=common.GladMindUsers(user=User.objects.create_user(user_name,user_email,user_password),
                                               country=user_country,
                                               state=user_state,
                                               gladmind_customer_id=unique_id,
                                               customer_name=user_name,
                                               email_id=user_email,
                                               phone_number=user_mobile_number,
                                               registration_date=datetime.now())
            gladmind_user.save();
            response=HttpResponse(json.dumps({'status': 1,'message':'Success!','unique_id':unique_id,
                                              'username':user_name,'id':'',
                                              'sourceURL':'','thumbURL':''}))
            return HttpResponse(json.dumps({'status': 1,'message':'Success!','unique_id':unique_id,
                                              'username':user_name,'id':'',
                                              'sourceURL':'','thumbURL':''}))
        except :
            pass
    return response


'''
update the details of existing account
'''
def update_account():
    pass
@csrf_exempt
def check_email_id_exists(email_id):
    try:
        user=User.objects.get(email=email_id)
        if user:
            email_exists=True
        else:
            email_exists=False
    except:
        email_exists=False
    return email_exists
        


