# from django.shortcuts import render_to_response
# from django.core.files import File
# from django.http.response import HttpResponse
# from django.core.context_processors import csrf
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate ,login
# from gladminds.models import common
# from gladminds import utils,mail
# from django.template import Context, Template
# from django.contrib.auth import logout
# from django.views.decorators.csrf import csrf_exempt
# import json
# from django.conf import settings
# from django.template.context import RequestContext
# from django.contrib.auth.models import User 
# from datetime import datetime
# from gladminds import mail
# import logging
# import uuid
# 
# logger = logging.getLogger("gladminds")
# GLADMINDS_ADMIN_MAIL = 'admin@gladminds.co'
# 
# _get_unique_id = lambda: str(uuid.uuid4())
# 
# @csrf_exempt
# def main(request):
#     action_to_method = {
#           'checkLogin':fnc_check_login,
#           'editSettings':fnc_update_user_details,
#           'feedback':fnc_feedback,
#           'addingItem':fnc_create_item,
#           'itemPurchaseInterest':fnc_item_purchase_interest,
#           'waranteeExtend':fnc_warranty_extend,
#           'insuranceExtend':fnc_insurance_extend,
#           'getStates':fnc_get_states,
#           'getProfile':fnc_get_profile,
#           'getProducts':fnc_get_products,
#           'getmyItems':fnc_get_user_items,
#           'getWarantee':fnc_get_warrenty,
#           'getInsurance':fnc_get_insurance,
#           'deleteRec':fnc_delete_record,
#           'fetchRec':fnc_get_record,
#           'newRegister':fnc_create_new_user,
#     }
#     
#     action = request.POST.get('action', None) or request.GET.get('action', None)
#     if action and action in action_to_method.keys():
#         method = action_to_method[action]
#         data =  method(request)
#         resp_str = json.dumps(data)
#         return HttpResponse(resp_str)
#     
#     return HttpResponse()
#     
# 
# @csrf_exempt      
# def fnc_create_item(request):
#     data = None
#     try:
#         post_data = request.POST
#         user_id = post_data['addnewitem_userID']
#         product_name = post_data['ai_txtProduct']
#         brand_id = post_data['ai_txtManufacturer']
#         product_id = post_data['ai_txtitem-no']
#         purchase_date = post_data.get('ai_txtpur-date', None)
#         purchased_from = post_data.get('ai_txtpurchased-from', None)
#         seller_email = post_data.get('ai_txtseller-email', None)
#         seller_phone = post_data.get('ai_txtseller-phone', None)
#         warranty_yrs = post_data.get('ai_txtwarranty', None)
#         insurance_yrs = post_data.get('ai_txtinsurance', None)
#         invoice_file = request.FILES.get('invoice_file', None)
#         warranty_file = request.FILES.get('warranty_file', None)
#         insurance_file = request.FILES.get('insurance_file', None)
#         user_obj = common.GladMindUsers.objects.get(user = User.objects.get(id=user_id))
#         brand_obj = common.BrandData.objects.get(brand_id = brand_id)
#         product_type_obj = common.ProductTypeData(brand_id = brand_obj, product_name = product_name, product_type = _get_unique_id())
#         product_type_obj.save()
#         item_obj = common.ProductData(customer_product_number = product_id, customer_phone_number = user_obj,
#                                       product_purchase_date = purchase_date, purchased_from = purchased_from, 
#                                       seller_email = seller_email, warranty_yrs = warranty_yrs,
#                                       insurance_yrs = insurance_yrs, invoice_loc = File(insurance_file),
#                                       warranty_loc = File(warranty_file), insurance_loc = File(warranty_file),
#                                       product_type = product_type_obj, seller_phone = seller_phone)
#         item_obj.save()
#         
#         data = {"status": "1","message":"Success!","id":item_obj.customer_product_number}
#     except Exception as ex:
#         logger.info('[Exception fnc_create_item]: {0}'.format(ex))
#         data = {"status": "1","message":"Success!","id":1}
#     return data
# 
# @csrf_exempt
# def fnc_item_purchase_interest(request):
#     resp = {}
#     data = {}
#     unique_id = request.GET.get('unique_id')
#     subject = '"Item Purchase Interest'
#     try:
#         user = common.GladMindUsers.objects.get(gladmind_customer_id = unique_id)
#         data['item'] = request.GET.get('item')
#         data['email_id'] = user.email_id
#         data['user_name'] =user.customer_name
#         data['phone_number'] = user.phone_number
#         data['address'] = user.address
#         data['country'] = user.country
#         data['state'] = user.state
#         data['timestamp'] = datetime.now()
#         resp['status'] = '1'
#         mail.item_purchase_interest(data = data, receiver = GLADMINDS_ADMIN_MAIL, subject = subject)
#     except Exception as ex:
#         resp['status'] = '0'
#         logger.info("[Exception: fnc_item_purchase_interest]: {0}".format(ex))
#     return resp
# 
# @csrf_exempt
# def fnc_warranty_extend(request):
#     resp = {}
#     data = {}
#     unique_id = request.GET.get('unique_id')
#     data['item'] = request.GET.get('item')
#     subject = 'Warranty Extend Request'
#     try:
#         user = common.GladMindUsers.objects.get(gladmind_customer_id = unique_id)
#         data['email_id'] = user.email_id
#         data['user_name'] =user.customer_name
#         data['phone_number'] = user.phone_number
#         data['timestamp'] = datetime.now()
#         resp['status'] = '1'
#         mail.warrenty_extend(data = data, receiver = GLADMINDS_ADMIN_MAIL, subject = subject)
#     except Exception as ex:
#         resp['status'] = '0'
#         logger.info("[Exception: fnc_item_purchase_interest]: {0}".format(ex))
#     return resp
# 
# @csrf_exempt
# def fnc_insurance_extend(request):
#     data = {}
#     resp = {}
#     unique_id = request.GET.get('unique_id')
#     data['item'] = request.GET.get('item')
#     subject = 'Insurance Purchase Request'
#     try:
#         user = common.GladMindUsers.objects.get(gladmind_customer_id = unique_id)
#         data['email_id'] = user.email_id
#         data['user_name'] =user.customer_name
#         data['phone_number'] = user.phone_number
#         data['timestamp'] = datetime.now()
#         resp['status'] = '1'
#         mail.insurance_extend(data = data, receiver = GLADMINDS_ADMIN_MAIL, subject = subject)
#     except Exception as ex:
#         resp['status'] = '0'
#         logger.info("[Exception: fnc_item_purchase_interest]: {0}".format(ex))
#     return resp
# 
# @csrf_exempt
# def fnc_get_states(request):
#     state_list=[
#                 "Uttar Pradesh", "Maharashtra", "Bihar", "West Bengal", "Andhra Pradesh", "Madhya Pradesh",
#                 "Tamil Nadu", "Rajasthan", "Karnataka", "Gujarat", "Odisha", "Kerala", "Jharkhand", "Assam", "Punjab",
#                 "Haryana","Chhattisgarh", "Jammu and Kashmir","Uttarakhand","Himachal Pradesh", "Tripura", "Meghalaya", 
#                 "Manipur", "Nagaland", "Goa", "Arunachal Pradesh", "Mizoram","Sikkim", "Delhi", "Puducherry", 
#                 "Chandigarh", "Andaman and Nicobar Islands", "Dadra and Nagar Haveli", "Daman and Diu", 
#                 "Lakshadweep"]
#     states= {}
#     if request.GET.get('cID',None)=='india':
#         states=','.join(state_list)
#     return states
# 
# @csrf_exempt
# def fnc_get_profile(request):
#     resp = {}
#     unique_id=request.GET.get('unique_id')
#     try:
#         user_profile=common.GladMindUsers.objects.get(gladmind_customer_id=unique_id)
#         resp['name']=user_profile.user.username
#         resp['email']=user_profile.user.email
#         resp['mobile']=user_profile.phone_number
#         resp['address']=user_profile.address
#         resp['country']=user_profile.country
#         resp['state']=user_profile.state
#         resp['dob'] = user_profile.date_of_birth
#         resp['gender'] = user_profile.gender
#     except Exception as ex:
#         resp['status'] = '0'
#         logger.info("[Exception fnc_get_profile]: {0}".format(ex))
#     return resp
# 
# @csrf_exempt
# def fnc_get_products(request):
#     resp = {}
#     resp_product_type = []
#     resp_brand = []
#     try:
#         product_types = common.ProductTypeData.objects.filter(isActive = True)
#         product_name = []
#         for product_type in product_types:
#             product_name.append(product_type.product_name)
#         resp_product_type = {"Products":','.join(product_name)}
#         brands = common.BrandData.objects.filter(isActive = True)
#         
#         for brand in brands:
#             brand_data = {'id': brand.brand_id, 'manufacturer': brand.brand_name}
#             resp_brand.append(brand_data)
#         resp = {'manufacturers':resp_brand, "Products": ','.join(product_name)}
#     
#     except Exception as ex:
#         logger.info("[Exception fnc_get_products]:{0}".format(ex))
#     return resp
#         
# @csrf_exempt
# def fnc_get_user_items(request):
#     unique_id = request.GET.get('unique_id')
#     user_data = common.GladMindUsers.objects.get(gladmind_customer_id = unique_id)
# 
#     items = common.ProductData.objects.filter(customer_phone_number__user_id = user_data.user, isActive=True)
#     myitems = []
#     for item in items:
#         product_type = item.product_type.product_type
#         brand_image_loc = "images/default.png"
#         brand_name = item.product_type.brand_id.brand_name
#         item_id = item.customer_product_number
#         myitems.append({"id": item_id, "manufacturer": brand_name, "Product":item_id, "image":'brand_image_loc'})
#     return {'myitems':myitems}
# 
# @csrf_exempt
# def fnc_get_warrenty(request):
#     item_id = request.GET.get('itemID')
#     data = None
#     try:
#         product = common.ProductData.objects.get(customer_product_number = item_id)
#         data = {'status':'1', 'purchaseDate':str(product.product_purchase_date), 'waranteeYear':product.warranty_yrs}
#     except Exception as ex:
#         data = {'status':'0'}
#     
#     return data
#     
#     
# @csrf_exempt
# def fnc_get_insurance(request):
#     item_id = request.GET.get('itemID')
#     data = None
#     try:
#         product = common.ProductData.objects.get(customer_product_number = item_id)
#         data = {'status':1, 'purchaseDate':str(product.product_purchase_date), 'insuranceYear':product.insurance_yrs}
#     except Exception as ex:
#         data = {'status':0}
#     return data
# 
# @csrf_exempt
# def fnc_delete_record(request):
#     item_id = request.GET.get('itemID')
#     data = None
#     try:
#         result = common.ProductData.objects.get(customer_product_number = item_id).delete()
#         data = {'status':1}
#     except Exception as ex:
#         data = {'status':0}
#     return data
# 
# @csrf_exempt
# def fnc_get_record(request):
#     item_id = request.GET.get('itemID')
#     data = None
#     try:
#         product = common.ProductData.objects.get(customer_product_number = item_id)
#         print product.__dict__
#         data = {'status': '1', "userid":product.customer_phone_number.user_id,"pr_name" :'',"m_id":'', 'item_num':product.product_id, 'pur_date':str(product.product_purchase_date), 'purchased_from':product.purchased_from,
#                 'seller_email':product.seller_email, 'seller_phone':product.seller_phone, 'warranty_yrs':product.warranty_yrs, 'insurance_yrs':product.insurance_yrs, 'invoice_URL':'product.invoice_loc', 
#                 'warranty_URL':'product.warranty_loc', 'insurance_URL':'', 
#                 }
#     except Exception as ex:
#         logger.info("[Exception fnc_get_record]: {0}".format(ex))
#         data = {'status':'0'}
#     return data
#     
# @csrf_exempt
# def test(request):
#     return render_to_response('afterbuy/test.html')
# 
# @csrf_exempt
# def home(request):
#     return render_to_response('afterbuy/index.html')
#         
# @csrf_exempt
# def fnc_check_login(request):
#     data = None
#     username = request.POST.get('txtUsername')
#     password = request.POST.get('txtPassword')
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             user_obj=User.objects.get(username=username)
#             user_name=user_obj.username
#             user_profile=common.GladMindUsers.objects.get(user=user)
#             unique_id=user_profile.gladmind_customer_id
#             id=user_profile.user_id
#             data = {'status': '1','id':id,'username':user_name,'unique_id':unique_id}
#         else:
#             data = {'status': '0'}
#     else:
#        data = {'status': '0'}
#     return data
# 
# @csrf_exempt
# def fnc_update_user_details(request):
#     data = None
#     user_id=request.POST.get('userID')
#     if user_id:
#         user_name=request.POST.get('txt_name', None)
#         user_email=request.POST.get('txt_email', None)
#         user_country=request.POST.get('txt_country', None)
#         user_state=request.POST.get('txt_state', None)
#         user_mobile_number=request.POST.get('txt_mob', None)
#         user_dob=request.POST.get('txt_dob', None)
#         user_interest=request.POST.get('txt_interest', None)
#         user_address=request.POST.get('txt_address', None)
#         user_gender=request.POST.get('txt_gender', None)
#         try:
#             user_object=common.GladMindUsers.objects.get(user_id=user_id)
#             user_object.customer_name=user_name
#             user_object.email_id=user_email
#             user_object.phone_number=user_mobile_number
#             user_object.address=user_address
#             user_object.country=user_country
#             user_object .state=user_state
#             user_object.dob=user_dob
#             user_object.gender=user_gender
#             user_object.user.username=user_name
#             user_object.user.email=user_email
#             unique_id=user_object.gladmind_customer_id
#             user_object.save()
#             data = {'status':" 1",'thumbURL':'','sourceURL':''}
#         except:
#             data = {'status': 0}
#     else:
#         data = {'status': 0}
#     return data
#         
# @csrf_exempt
# def fnc_feedback(request):
#     #FIXME not saving feed back just sending the response
#     user_id=request.POST.get('userID')
#     return {"status":"1","message":"Success!","id":user_id} 
#     
# 
# 
# '''
# method for creating new user and checking user 
# is already exists or not
# '''
# from datetime import datetime
# @csrf_exempt
# def fnc_create_new_user(request):
#     data = {}
#     user_name=request.POST.get('txtName', None)
#     user_email=request.POST.get('txtEmail', None)
#     user_password= request.POST.get('txtPassword', None)
#     user_country=request.POST.get('txtCountry', None)
#     user_state=request.POST.get('txtState', None)
#     user_mobile_number=request.POST.get('txtMobile', None)
#     user_address=request.POST.get('txtAddress',None)
#     unique_id=''
#     if check_email_id_exists(user_email):
#         data = {'status': 2,'message':'Email already exists'}
#     else:
#         try:
#             unique_id='GMS17_'+str(utils.generate_unique_customer_id())
#             gladmind_user=common.GladMindUsers(user=User.objects.create_user(user_name,user_email,user_password),
#                                                country=user_country,
#                                                state=user_state,
#                                                gladmind_customer_id=unique_id,
#                                                customer_name=user_name,
#                                                email_id=user_email,
#                                                phone_number=user_mobile_number,
#                                                registration_date=datetime.now(),
#                                                address=user_address)
#             gladmind_user.save();
#             user_obj=common.GladMindUsers.objects.get(gladmind_customer_id=unique_id)
#             send_registration_mail(gladmind_user)
#             data = {'status': 1,'message':'Success!','unique_id':unique_id,
#                                               'username':user_name,'id':user_obj.user_id,
#                                               'sourceURL':'','thumbURL':''}
#         except :
#             data={'status':0}
#     return data
# 
# 
# def send_registration_mail(user_detail):
#     unique_id= user_detail.gladmind_customer_id
#     user_name=user_detail.customer_name
#     user_mobile=user_detail.phone_number
#     user_email=user_detail.email_id
#     user_state=user_detail.state
#     user_country=user_detail.country
#     user_address=user_detail.address
#     file_stream = open(settings.TEMPLATE_DIR+'/registration_mail.html')
#     reg_mail_temp = file_stream.read()
#     template = Template(reg_mail_temp)
#     context = Context({'unique_id':unique_id,
#                        'user_name':user_name,
#                        'user_mobile':user_mobile,
#                        'user_email':user_email,
#                        'user_state':user_state,
#                        'user_country':user_country,
#                        'user_address':'test_address'})
#     body = template.render(context)
#     try:
#         mail.send_email('info@gladminds.com',user_email, 'AfterBuy Registration details - GladMinds', body)
#     except Exception as ex:
#         logger.info("[Exception Registration mail: {0}".format(ex))
# 
# @csrf_exempt
# def check_email_id_exists(email_id):
#     try:
#         user=User.objects.get(email=email_id)
#         if user:
#             email_exists=True
#         else:
#             email_exists=False
#     except:
#         email_exists=False
#     return email_exists
# 
# def save_image(profile_pic):
#     import os
#     image_name = profile_pic._get_name()
#     image_directory = os.path.join(settings.STATIC_DIR,
#                                    "img/afterbuy/user")
#     if os.path.isdir(image_directory):
#         pass
#     else:
#         os.makedirs(image_directory)
#         fd = open('%s/%s' % (image_directory, str(image_name)), 'wb')
#         for chunk in profile_pic.chunks():
#             fd.write(chunk)
#         fd.close()
#     return image_name
# 
# 
# 
# @csrf_exempt
# def app_logout(request):
#     logout(request)
#     return HttpResponse('logged out')
# 
# 
# 
# @csrf_exempt
# def home(request):
#     return render_to_response('afterbuy/index.html')
