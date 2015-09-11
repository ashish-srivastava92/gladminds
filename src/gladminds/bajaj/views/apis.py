'''
author: araskumar.a
date: 31-08-2015
'''
import json

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.settings import api_settings

from gladminds.bajaj.models import DistributorSalesRep, Retailer, SparePartMasterData

@api_view(['POST'])
def authentication(request):
    '''
    This method is an api gets username and password, authenticates it and sends
    a token as response
    '''
    user = authenticate(username = request.POST["username"], password = request.POST["password"])
    if user:
        if user.is_active:
            dsr = DistributorSalesRep.objects.get(user = user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            return Response({'Id': dsr.id, 'token': jwt_encode_handler(payload), 'status': 1 })
        else:
            return Response({'message': 'your user is inactive.. \
                             Please contact your distributor', 'status':0})
    else:
        return Response({'message': 'you are not a registered user', 'status':0})
    
@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_retailers(request, dsr_id):
    '''
    This method returns all the retailers given the dsr id 
    '''
    # distributor = DistributorSalesRep.objects.get(id = dsr_id)
    # retailers = Retailer.objects.filter(distributor = distributor.distributor)
    retailers = Retailer.objects.all()
    retailer_list = []
    for retailer in retailers:
        retailer_dict = {}
        retailer_dict.update({"retailer_name":retailer.retailer_name})
        retailer_dict.update({"retailer_mobile":retailer.mobile})
        retailer_dict.update({"retailer_email":retailer.email})
        retailer_list.append(retailer_dict)
    return Response(retailer_list)

@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_parts(request):
    parts = SparePartMasterData.objects.all()
    parts_list =[]
    for part in parts:
        parts_dict = {}
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_model":part.part_model})
        parts_dict.update({"category":part.category})
        parts_list.append(parts_dict)
    return Response(parts_list)

    

