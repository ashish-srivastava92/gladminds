'''
author: araskumar.a
date: 31-08-2015
'''
import json, datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.settings import api_settings

from gladminds.bajaj.models import DistributorSalesRep, Retailer,PartModels, Categories, \
                            SubCategories, PartPricing, OrderPart
from gladminds.core import constants

@api_view(['POST'])
def authentication(request):
    '''
    This method is an api gets username and password, authenticates it and sends
    a token as response
    '''
    #load the json input of username and password as json
    load = json.loads(request.body)
    user = authenticate(username = load.get("username"), password = load.get("password"))
    #user = authenticate(username = request.POST["username"], password = request.POST["password"])
    if user:
        if user.is_active:
            #the user is active.He should be a dsr or retailer 
            authenticated_user = DistributorSalesRep.objects.filter(user = user)
            if authenticated_user:
                login_type = "dsr"
                role_id = authenticated_user[0].distributor_sales_code
            else:
                authenticated_user = Retailer.objects.filter(user = user, \
                                                approved = constants.STATUS['APPROVED'])
                if authenticated_user:
                    login_type = "retailer"
                    role_id = authenticated_user[0].retailer_code
                else:
                    return Response({'message': 'you are not \
                                 a DSR or retailer. Please contact your distributor', 'status':0})
            # now, he is a valid user, generate token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            data = {"Id": role_id,
                    "token": jwt_encode_handler(payload), "status":1, "login_type":login_type}
            return Response(data, content_type="application/json")
        else:
         return Response({'message': 'you are not active. Please contact your distributor', 'status':0})   
    else:
        return Response({'message': 'you are not a registered user', 'status':0})
    
@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_retailers(request, dsr_id):
    '''
    This method returns all the retailers of the distributor given the dsr id 
    '''
    distributor = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    retailers = Retailer.objects.filter(distributor = distributor.distributor, \
                                approved = constants.STATUS['APPROVED'] )
    #retailers = Retailer.objects.all()
    retailer_list = []
    for retailer in retailers:
        retailer_dict = {}
        retailer_dict.update({"retailer_Id":retailer.retailer_code})
        retailer_dict.update({"retailer_name":retailer.retailer_name})
        retailer_dict.update({"retailer_mobile":retailer.mobile})
        retailer_dict.update({"retailer_email":retailer.email})
        retailer_dict.update({"retailer_address":retailer.user.address})
        retailer_dict.update({"latitude":retailer.latitude})
        retailer_dict.update({"longitude":retailer.longitude})
        retailer_list.append(retailer_dict)
    return Response(retailer_list)

@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_parts(request):
    '''
    This method returns all the spare parts details
    '''
    parts = PartPricing.objects.filter(active = True)
    parts_list =[]
    for part in parts:
        # today = datetime.date.today()
        # # price = SparePartPoint.objects.filter(part_number = part, valid_from__gt = today, \
        # #                             valid_till__lt = today)
        parts_dict = {}
        parts_dict.update({"part_id":part.id})
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_model":part.part_model})
        parts_dict.update({"category":part.category.category_name})
        parts_dict.update({"subcategory":part.subcategory.subcategory_name})
        parts_dict.update({"mrp":part.mrp})
        parts_list.append(parts_dict)
    return Response(parts_list)
    
@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def dsr_order(request, dsr_id, retailer_id):
    '''
    This method gets the orders placed by the dsr on behalf of the retailer and puts
    it in the database
    '''
    parts = json.loads(request.body)
    
    date = parts['date']
    items = parts['order_items']
    for item in items:
        orderpart = OrderPart()
        dd, mm, yyyy = split_date(parts['date'])
        orderpart.order_date = parts['date']
        orderpart.order_id = retailer_id + dd + mm + yyyy
        orderpart.quantity = item['qty']
        orderpart.price = item['unit_price']
        orderpart.total_price = item['sub_total']
        orderpart.part = PartPricing.objects.filter(description = item['name'])[0]
        orderpart.dsr = DistributorSalesRep.objects.get(id = dsr_id)
        orderpart.retailer = Retailer.objects.get(id = retailer_id)
        #orderpart.save()
    return Response({'message': 'Order(s) has been placed successfully', 'status':1})
    

@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def retailer_order(request, retailer_id):
    '''
    This method gets the orders placed by the retailer and puts it in the database
    '''
    parts = json.loads(request.body)
    date = parts['date']
    items = parts['order_items']
    for item in items:
        orderpart = OrderPart()
        dd, mm, yyyy = split_date(parts['date'])
        orderpart.order_date = parts['date']
        orderpart.order_id = retailer_id + dd + mm + yyyy
        orderpart.quantity = item['qty']
        orderpart.price = item['unit_price']
        orderpart.total_price = item['sub_total']
        orderpart.part = PartPricing.objects.get(id = item['part_id'])
        orderpart.retailer = Retailer.objects.get(id = retailer_id)
        orderpart.save()
    return Response({'message': 'Order(s) has been placed successfully', 'status':1})

# @api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_schedule(request):
    '''
    This method gets the schedule(the retailers he has to visit) for today, given the dsr id
    '''
    
    return Response({'retailer': 'retailer id'})

# @api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_retailer_transaction(request):
    '''
    This method returns retailer transaction details like paid amount, outstanding, cheque number, etc
    given the retailer Id
    '''
    
    return Response({'retailer': 'retailer id'})

def split_date(date):
    date_array = date.split('-')
    dd = date_array[2]
    mm = date_array[1]
    yyyy = date_array[0]
    return dd, mm, yyyy
    
    
    
    


    

    

