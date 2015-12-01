'''
author: araskumar.a
date: 31-08-2015
'''
import json, datetime, time

from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.settings import api_settings

from gladminds.bajaj.models import DistributorSalesRep, Retailer,PartModels, Categories, \
                            PartPricing, OrderPart, Distributor, OrderPartDetails, Invoices, \
                           DSRWorkAllocation ,Collection,CollectionDetails,PartsStock

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
def get_retailer_profile(request, retailer_id):
    retailer = Retailer.objects.filter(retailer_code = retailer_id, \
                                is_active = True)
    if not retailer:
        return Response('The given retailer id is invalid or your login may be inactive. Please \
                                    contact your distributor')
    else:
        retailer_dict = {}
        retailer_dict.update({"retailer_name":retailer.retailer_name})
        retailer_dict.update({"retailer_mobile":retailer.mobile})
        retailer_dict.update({"retailer_email":retailer.email})
        retailer_dict.update({"retailer_address":retailer.user.address})
        retailer_dict.update({"latitude":retailer.latitude})
        retailer_dict.update({"longitude":retailer.longitude})
        return Response(retailer_dict)


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
        available_quantity = PartsStock.objects.get(part_number_id = part.id ).available_quantity
        parts_dict = {}
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_sub_category":part.subcategory.name})
        parts_dict.update({"part_products":part.products})
        parts_dict.update({"part_available_quantity":available_quantity})
        parts_dict.update({"mrp":part.mrp})
        parts_list.append(parts_dict)
    return Response(parts_list)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_alternateparts(request):
    '''
    This method returns all the spare parts details
    '''
    parts = AlternateParts.objects.filter(active = True)
    parts_list =[]
    for part in parts:
        parts_dict = {}
        parts_dict.update({"part_name":part.name})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_model":part.model_name})
        parts_list.append(parts_dict)
    return Response(parts_list)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_schedule(request, dsr_id, date):
    '''
    This method gets the schedule(the retailers he has to visit) for today, given the dsr id
    '''
    schedule_date = split_date(date)
    dsr = DistributorSalesRep.objects.filter(distributor_sales_code = dsr_id)
    schedules = DSRWorkAllocation.objects.filter(date__startswith = \
                    datetime.date(int(schedule_date[2]),int(schedule_date[1]),int(schedule_date[0])), dsr=dsr)
                       
    schedules_list = []
    for schedule in schedules:
        schedule_dict = {}
        schedule_dict.update({"retailer_code" : schedule.retailer.retailer_code})
        schedule_dict.update({"retailer_name" : schedule.retailer.retailer_name})
        tm = time.strptime(str(schedule.date.time()), "%H:%M:%S")
        schedule_dict.update({"Time" : time.strftime("%I:%M %p", tm)})
        schedule_dict.update({"retailer_address":schedule.retailer.user.address})
        schedule_dict.update({"latitude":schedule.retailer.latitude})
        schedule_dict.update({"longitude":schedule.retailer.longitude})
        schedules_list.append(schedule_dict)
    return Response(schedules_list)


def split_date(date):
    date_array = date.split('-')
    dd = date_array[2]
    mm = date_array[1]
    yyyy = date_array[0]
    return dd, mm, yyyy

@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def place_order(request, dsr_id):
    '''
    This method gets the orders placed by the dsr on behalf of the retailer and puts
    it in the database
    '''
    parts = json.loads(request.body)
    
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    if dsr:
        for order in parts :
            orderpart = OrderPart()
            orderpart.dsr = dsr
            retailer = Retailer.objects.get(retailer_code = order['retailer_id'])
            orderpart.retailer = retailer
            orderpart.order_date = order['date']
            orderpart.order_placed_by = order['order_placed_by']
            orderpart.save()
            #push all the items into the orderpart details
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                orderpart_details.part_number = PartPricing.objects.\
                                                get(part_number = item['part_number'])
                orderpart_details.quantity = item['qty']
                orderpart_details.order = orderpart
                orderpart_details.line_total = item['line_total']
                print orderpart_details.line_total
                orderpart_details.save()
    return Response({'message': 'Order updated successfully', 'status':1})

@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def retailer_place_order(request, retailer_id):
    '''
    This method gets the orders placed by the retailer and puts
    it in the database
    '''
    parts = json.loads(request.body)
    for order in parts :
            orderpart = OrderPart()
            retailer = Retailer.objects.get(retailer_code = retailer_id)
            orderpart.retailer = retailer
            orderpart.distributor = Distributor.objects.get(distributor_id = order['distributor_id'])
            orderpart.order_date = order['date']
            orderpart.order_placed_by = order['order_placed_by']
            orderpart.save()
            #push all the items into the orderpart details
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                orderpart_details.part_number = PartPricing.objects.\
                                                get(part_number = item['part_number'])
                orderpart_details.quantity = item['qty']
                orderpart_details.order = orderpart
                orderpart_details.line_total = item['line_total']
                orderpart_details.save()
    return Response({'message': 'Order updated successfully', 'status':1})


@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_outstanding(request, dsr_id):
    '''
    This method returns the outstanding amount of all the retailers under the distributor pertaining
    to the dsr '''
    
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    retailers = Retailer.objects.filter(distributor = dsr.distributor)
    retailer_list = []
    
    #for a particular retailer, get all the invoices and total the invoice amount
    for retailer in retailers:
        invoices = Invoices.objects.filter(retailer = retailer)
        if invoices:
            for invoice in invoices:
                retailer_dict = {}
                total_amount = 0
                collection = 0
                total_amount = total_amount + invoice.invoice_amount
                retailer_dict.update({'retailer_id':retailer.retailer_code})
                retailer_dict.update({'invoice_id': invoice.invoice_id})
                retailer_dict.update({'total_amount': total_amount})
                retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
                
                #get the collections for that invoice
                collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                for each in collection_objs:
                    collections = CollectionDetails.objects.filter(collection_id = each.id)
                    if collections:
                        for each_collections in collections:
                            collection = collection + each_collections.collected_amount
                retailer_dict.update({'collected_amount': collection})
                retailer_list.append(retailer_dict)
    return Response(retailer_list)

# @api_view(['GET'])
# # # @authentication_classes((JSONWebTokenAuthentication,))
# # # @permission_classes((IsAuthenticated,))
# def get_retailer_outstanding(request, retailer_id):
#     '''
#     This method returns the outstanding amount of particular retailer with all the distributor '''
#     
#     retailers = Retailer.objects.filter(retailer_code = retailer_id)
#     # get the distributor list for that retailer
#     distributors = []
#     for retailer in retailers:
#         distributors.append(retailer.distributor)
#     
#     #for the particular retailer, get all the invoices and total the invoice amount
#     
#         invoices = Invoices.objects.filter(retailer = retailer)
#         if invoices:
#             for invoice in invoices:
#                 retailer_dict = {}
#                 outstanding = 0
#                 collection = 0
#                 outstanding = outstanding + invoice.invoice_amount
#                 retailer_dict.update({'retailer_id':retailer.retailer_code})
#                 retailer_dict.update({'invoice_id': invoice.id})
#                 retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
#                 # tm = time.strptime(str(invoice.invoice_date.time()), "%H:%M:%S")
#                 # retailer_dict.update({"Time" : time.strftime("%I:%M %p", tm)})
#                 #get the collections for that invoice
#                 collection_objs = Collection.objects.filter(invoice_id = invoice.id)
#                 for each in collection_objs:
#                     collections = CollectionDetails.objects.filter(collection_id = each.id)
#                     if collections:
#                         for each_collections in collections:
#                             collection = collection + each_collections.collected_amount
#                     outstanding = outstanding - collection
#                     retailer_dict.update({'outstanding':outstanding})
#                     retailer_list.append(retailer_dict)
#     return Response(retailer_list)

@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_distributor_for_retailer(request, retailer_id):
    '''
    This method returns all the retailers of the distributor given the dsr id 
    '''
    
    # distributor = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    retailers_list = Retailer.objects.filter(retailer_code = retailer_id)
    distributor_list = []
    distributor_dict = {}
    for retailer in retailers_list:
        #distributor_dict = {}
        distributor_of_retailer  = Distributor.objects.filter(id =retailer.distributor_id )
        for distributor in distributor_of_retailer:
            distributor_dict ={
                    'distributor_name':distributor.name,
                    'distributor_id':distributor.distributor_id,
                    'distributor_phone_number':distributor.phone_number,
                    'distributor_mobile1':distributor.mobile1,
                    'distributor_email':distributor.email
                }
            distributor_list.append(distributor_dict)
        
    return Response(distributor_list)

@api_view(['POST'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def uploadcollection(request):
    '''
    This method gets the collection of payment by dsr and puts it into the collection and collection
    details table
    '''
    collection_body = json.loads(request.POST['uploadcollection'])
    collection = Collection()
    collection.invoice = Invoices.objects.get(invoice_id = collection_body['invoice_id'])
    collection.payment_date = collection_body['payment_date']
    collection.dsr = DistributorSalesRep.objects.get(distributor_sales_code = \
                                                      collection_body['dsr_id'])
    #retailer = Retailer.objects.get(retailer_code = collection_body['retailer_id'])
    # print retailer
    # collection.retailer = retailer
    collection.save()
    #put data into collection details table
    payment_mode = 1
    for mode in constants.PAYMENT_MODES:
        if mode[0][1] == collection_body['payment_mode']:
            payment_mode = mode[0][0]
        else:
            continue
    for cheque in collection_body['cheque_details']:
        collectiondetails = CollectionDetails()
        collectiondetails.collection = collection
        collectiondetails.mode = payment_mode
        collectiondetails.collected_amount = collection_body['collected_amount']
        collectiondetails.cheque_bank = cheque['cheque_bank']
        collectiondetails.cheque_number = cheque['cheque_number']
        collectiondetails.cheque_amount = cheque['cheque_amount']
        collectiondetails.img_url = cheque['cheque_image_url']
        collectiondetails.save()
    
    return Response({'message': 'Retailer Collection is updated successfully', 'status':1})


    
    
    


    

    


