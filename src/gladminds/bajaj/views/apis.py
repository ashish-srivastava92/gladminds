'''
author: araskumar.a
date: 31-08-2015
'''

from django.contrib.auth.models import User
from rest_framework.response import Response
from gladminds.bajaj.models import DistributorSalesRep, Retailer
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_retailers(request, dsr_id):
    '''
    This method returns all the retailers given the distributor id
    '''
    distributor = DistributorSalesRep.objects.get(id = dsr_id)
    retailers = Retailer.objects.filter(distributor = distributor.distributor)
    retailer_list = []
    for retailer in retailers:
        retailer_dict = {}
        retailer_dict.update({"retailer_name":retailer.retailer_name})
        retailer_dict.update({"retailer_mobile":retailer.mobile})
        retailer_list.append(retailer_dict)
    return Response(retailer_list)