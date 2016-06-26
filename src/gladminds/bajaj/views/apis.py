import json, datetime, time
from datetime import timedelta
from collections import OrderedDict
from operator import itemgetter
from django.db import transaction
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count
from django.db.models import Max
import decimal
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.settings import api_settings

from gladminds.bajaj.models import DistributorSalesRep, Retailer,PartModel, Categories, \
                            PartPricing, Distributor,  Invoices, \
                            Collection,CollectionDetails,PartsStock,DSRWorkAllocation,DSRLocationDetails, \
			    NationalSparesManager,AreaSparesManager,OrderDeliveredHistory, MonthlyPartSalesHistory,\
    TransitStock
from gladminds.bajaj.models import OrderPart,OrderPartDetails, \
                        PartIndexDetails, PartIndexPlates, FocusedPart, \
                        AverageRetailerSalesHistory, AverageLocalitySalesHistory, AppInfo
from gladminds.core.auth_helper import Roles
from django.db.models import Sum

from gladminds.core import constants
import pytz

today = datetime.datetime.now()

@api_view(['POST'])
def authentication(request):
    '''
    This method is an api gets username and password, authenticates it and sends
    a token as response
    '''
    #load the json input of username and password as json
    load = json.loads(request.body)
    user = authenticate(username = load.get("username"), password = load.get("password"))
    registration_id = load.get("registration_id")
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
            if registration_id:
                from push_notifications.models import APNSDevice, GCMDevice
                gcm_obj_list = GCMDevice.objects.filter(registration_id=registration_id)
                if not gcm_obj_list:
                    gcm_obj = GCMDevice(registration_id=registration_id, user_id=user.id)
                else:
                    gcm_obj = gcm_obj_list[0]
                    gcm_obj.user_id = user.id
                gcm_obj.save()
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
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'
    distributor = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    retailers = Retailer.objects.filter(distributor = distributor.distributor, \
                                approved = constants.STATUS['APPROVED'], modified_date__gt=modified_since)
    retailer_list = []
    
    for retailer in retailers:
        retailer_dict = {}
        retailer_dict.update({"retailer_Id":retailer.retailer_code})
        retailer_dict.update({"retailer_name":retailer.retailer_name})
        retailer_dict.update({"retailer_mobile":retailer.mobile})
        retailer_dict.update({"retailer_email":retailer.email})
        retailer_dict.update({"retailer_address":retailer.user.address})
        retailer_dict.update({"locality":retailer.address_line_4})
        retailer_dict.update({"datetime":datetime.datetime.now()})
        if retailer.locality:
            retailer_dict["locality"] = retailer.locality.name
            retailer_dict.update({"city":retailer.locality.city.city})
            retailer_dict.update({"state":retailer.locality.city.state.state_name})
            retailer_dict.update({"locality_id":retailer.locality_id})
        else:
            retailer_dict.update({"city":''})
            retailer_dict.update({"state":''})
            retailer_dict.update({"locality_id":''})
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
def get_stock(request,dsr_id):
    '''
    This method returns all the stock details
    '''
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'
    #get the disributor id
    try:
        distributor_obj = DistributorSalesRep.objects.get(distributor_sales_code=dsr_id).distributor
    except:
       return Response([{"error":"Distributor not present"}])
    #get the parts with the distributor
    stocks = PartsStock.objects.filter(distributor=distributor_obj,modified_date__gt=modified_since)
    stock_list =[]
    for part in stocks:
        parts_dict = {}
	try:
            parts_dict["part_number"]=part.part_number.part_number
            parts_dict["part_available_quantity"]=part.available_quantity
            parts_dict["mrp"]=part.part_number.mrp
            parts_dict["datetime"] = datetime.datetime.now()

            transit_stock_list = TransitStock.objects.filter(part_number=part.part_number)
            # Check if transit stock exists then if it exists add the shipped quantity to parts_dict
            if not transit_stock_list:
                parts_dict["part_transit_quantity"] = 'N/A' # if transit stock doesnt exists
            else:
                parts_dict["part_transit_quantity"] = transit_stock_list[0].shipped_quantity # Added new field that shows the stock quantity available in transit
            
                  
	    stock_list.append(parts_dict)
	except:
	    # FIXME: Remove try except from here and confirm if exceptions are due to curropt data
	    pass
    return Response(stock_list)

@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_parts(request):
    '''
    This method returns all the spare parts details
    ''' 
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'    
    parts = PartPricing.objects.filter(active = True, modified_date__gt=modified_since)
    parts_list =[]
    for part in parts:
        part_stock_obj_list = PartsStock.objects.filter(part_number_id = part.id)
        if part_stock_obj_list:
            available_quantity = part_stock_obj_list[0].available_quantity
        else:
            available_quantity = 0
        parts_dict = {}
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_category":part.subcategory.name})
        associated_categories = part.associated_parts.all()
        parts_dict.update({"associated_categories_str": [i.part_number for i in associated_categories]})
        try:
            available_quantity = PartsStock.objects.get(part_number = part)
        except:
            available_quantity = 'NA'
        if available_quantity == 'NA':
            parts_dict.update({"part_available_quantity":'NA'})
        else:
            parts_dict.update({"part_available_quantity":available_quantity.available_quantity})
        applicable_models = ', '.join(list(part.applicable_models.values_list('model_name', flat=True)))        
        parts_dict.update({"part_products":applicable_models})
        parts_dict.update({"mrp":part.mrp})
        parts_dict.update({"datetime": datetime.datetime.now()})
        parts_list.append(parts_dict)
    return Response(parts_list)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_focused_parts(request):
    '''
    Returns all the focused parts along with locality
    '''
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'
    retailer_code = request.GET.get('retailer_code')
    dsr_code = request.GET.get('dsr_code')
    if retailer_code:
	   locality = Retailer.objects.get(retailer_code=retailer_code).locality
	   all_focused_parts = FocusedPart.objects.filter(locality=locality, modified_date__gt=modified_since)
    elif dsr_code:
	   retailer_objs = Retailer.objects.filter(dsr__distributor_sales_code=dsr_code)
	   localities = [i.locality for i in retailer_objs]
	   all_focused_parts = FocusedPart.objects.filter(locality__in=localities, modified_date__gt=modified_since)
    else:
    	all_focused_parts = FocusedPart.objects.filter(modified_date__gt=modified_since)

    parts_list = []
    for focused_part in all_focused_parts:
        parts_dict = {}
        parts_dict.update({"part_name":focused_part.part.description})
        parts_dict.update({"part_number":focused_part.part.part_number})
        parts_dict.update({"part_category":focused_part.part.subcategory.name})
        associated_categories = focused_part.part.associated_parts.all()
        parts_dict.update({"associated_categories_str": [i.part_number for i in associated_categories]})
        try:
            available_quantity = PartsStock.objects.get(part_number = focused_part.part)
        except:
            available_quantity = 'NA'
        if available_quantity == 'NA':
            parts_dict.update({"part_available_quantity":'NA'})
        else:
            parts_dict.update({"part_available_quantity":available_quantity.available_quantity})
        parts_dict.update({"part_products":focused_part.part.products})
        parts_dict.update({"mrp":focused_part.part.mrp})
        parts_dict.update({"locality_id": focused_part.locality_id})
        parts_dict.update({"city": focused_part.locality.city.city})
        parts_dict.update({"state": focused_part.locality.city.state.state_name})
        parts_dict.update({"locality": focused_part.locality.name})
        parts_dict.update({"datetime": datetime.datetime.now()})
        parts_list.append(parts_dict)
    return Response(parts_list)	



@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_parts_catalog(request):
    '''
    This method returns all the spare parts details based on the catalog
    '''
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'    
    parts = PartIndexDetails.objects.filter(plate__active = True, modified_date__gt=modified_since)
    parts_list =[]
    for part in parts:
        parts_dict = {}
        parts_dict.update({"quantity_variant1":part.quantity_variant1})
        parts_dict.update({"quantity_variant2":part.quantity_variant2})
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_model":part.plate.model.model_name})
        parts_dict.update({"part_plate":part.plate.plate_name})
        parts_dict.update({"plate_id":part.plate_id})
        parts_dict.update({"mrp":part.mrp})
        parts_dict.update({"datetime":datetime.datetime.now()})
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
def get_schedule(request, dsr_id):
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
@transaction.atomic
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
            orderpart.distributor = dsr.distributor
            orderpart.order_placed_by = order['order_placed_by']
            orderpart.order_number = order['order_id']
            orderpart.latitude = order['latitude']
            orderpart.longitude = order['longitude']
            orderpart.save()
            #push all the items into the orderpart details
            orderpart_details_list =  []
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                item_part_type = item.get('part_type')
                part_category = None
                part_number_catalog = None
                if item_part_type == 1:
                    '''Get the part details from Catalog Table'''
                    part_catalog = PartIndexDetails.objects.\
                                             get(part_number=item['part_number'], plate_id=item.get("plate_id"))
                    orderpart_details.part_number_catalog = part_catalog
                    orderpart_details.order_part_number = orderpart_details.part_number_catalog.part_number
                else:
                    '''Get the part details from PartPricing Table'''
                    part_category = PartPricing.objects.\
                                             get(part_number=item['part_number'])
                    orderpart_details.part_number = part_category
                    orderpart_details.order_part_number = orderpart_details.part_number.part_number

                orderpart_details.quantity = item['qty']
                orderpart_details.order = orderpart
                orderpart_details.line_total = item['line_total']
                orderpart_details_list.append(orderpart_details)
        try:
            OrderPartDetails.objects.bulk_create(orderpart_details_list)
        except:
            # TODO: Add logger here
            return Response({'message': 'Order could not be placed', 'status':0})

    try:
        send_msg_to_retailer_on_place_order(request,retailer.id,orderpart.order_number)
        send_email_to_retailer_on_place_order(orderpart, orderpart_details_list)
    except:
        pass
    return Response({'message': 'Order updated successfully', 'status':1})

@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
@transaction.atomic
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
            orderpart.order_number = order['order_id']
            orderpart.order_placed_by = order['order_placed_by']
            orderpart.save()
            #push all the items into the orderpart details
            orderpart_details_list =  []
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                item_part_type = item.get('part_type')
                part_category = None
                part_number_catalog = None
                if item_part_type == 1:
                    '''Get the part details from Catalog Table'''
                    part_catalog = PartIndexDetails.objects.\
                                             get(part_number=item['part_number'], plate_id=item.get("plate_id"))
                    orderpart_details.part_number_catalog = part_catalog
                    orderpart_details.order_part_number = orderpart_details.part_number_catalog.part_number
                else:
                    '''Get the part detailes from PartPricing Table'''
                    part_category = PartPricing.objects.\
                                             get(part_number=item['part_number'])
                    orderpart_details.part_number = part_category
                    orderpart_details.order_part_number = orderpart_details.part_number.part_number


                orderpart_details.quantity = item['qty']
                orderpart_details.order = orderpart
                orderpart_details.line_total = item['line_total']
                orderpart_details_list.append(orderpart_details)
    try:
        OrderPartDetails.objects.bulk_create(orderpart_details_list)
    except:
        # TODO: Add logger here
        return Response({'message': 'Order could not be placed', 'status':0})

    try:
        send_msg_to_retailer_on_place_order(request,retailer.id,orderpart.order_number)
        send_email_to_retailer_on_place_order(orderpart, orderpart_details_list)
    except:
        pass
    return Response({'message': 'Order updated successfully', 'status':1})


@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_outstanding(request, dsr_id):
    '''
    This method returns the outstanding amount of all the retailers under the distributor pertaining
    to the dsr '''
    
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    retailers = Retailer.objects.filter(distributor = dsr.distributor, \
                                        approved = constants.STATUS['APPROVED'])
    retailer_list = []
    
    #for a particular retailer, get all the invoices and total the invoice amount
    for retailer in retailers:
        invoices = Invoices.objects.filter(retailer = retailer)
        if invoices:
            for invoice in invoices:
                retailer_dict = {}
                total_amount = 0
                collection = 0
                if invoice.invoice_amount is None:
                    invoice.invoice_amount = 0.0
                if invoice.paid_amount is None:
                    invoice.paid_amount = 0.0
                total_amount = total_amount + (invoice.invoice_amount - invoice.paid_amount)
                retailer_dict.update({'retailer_id':retailer.retailer_code})
                retailer_dict.update({'invoice_id': invoice.invoice_id})
                retailer_dict.update({'total_amount': total_amount})
                retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
                #get the collections for that invoice
		diff = today.date() - invoice.invoice_date.date()
                collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                for each in collection_objs:
                    collections = CollectionDetails.objects.filter(collection_id = each.id)
                    if collections:
                        for each_collections in collections:
                            collection = collection + each_collections.collected_amount
                retailer_dict.update({'collected_amount': collection})
		retailer_dict.update({'period': diff.days})
                retailer_list.append(retailer_dict)
    return Response(retailer_list)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_dsr_outstanding(request, dsr_id):
    '''
    This method returns the outstanding amount of all the retailers under the distributor
    pertaining to the dsr '''    
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'    
    retailers = Retailer.objects.filter(distributor = dsr.distributor, \
                                        approved = constants.STATUS['APPROVED'])
    retailer_list = []
    #for a particular retailer, get all the invoices and total the invoice amount
    for retailer in retailers:
        invoices = Invoices.objects.filter(retailer = retailer, modified_date__gt=modified_since)
        if invoices:
            for invoice in invoices:
                if not invoice.invoice_amount:
                    invoice.invoice_amount = 0
                if not invoice.paid_amount:
                    invoice.paid_amount = 0
                retailer_dict = {}
                total_amount = 0
                collection = 0
                invoice.invoice_amount = invoice.invoice_amount if invoice.invoice_amount else 0
                invoice.paid_amount = invoice.paid_amount if invoice.paid_amount else 0
                total_amount = total_amount + (invoice.invoice_amount - invoice.paid_amount)
                retailer_dict.update({'retailer_id':retailer.retailer_code})
                retailer_dict.update({'invoice_id': invoice.invoice_id})
                retailer_dict.update({'total_amount': total_amount})
                retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
                diff = today.date() - invoice.invoice_date.date()
                #get the collections for that invoice
                collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                for each in collection_objs:
                    # collections = CollectionDetails.objects.filter(collection_id = each.id)
                    # if collections:
                    #     for each_collections in collections:
                    each.collected_amount = each.collected_amount if each.collected_amount else 0
                    collection = collection + each.collected_amount
                retailer_dict.update({'collected_amount': collection})
                retailer_dict.update({'period': diff.days})
                retailer_dict.update({'datetime': datetime.datetime.now()})
                retailer_list.append(retailer_dict)
        # else:
        #     retailer_dict = {}
        #     retailer_dict.update({'retailer_id':retailer.retailer_code})
        #     retailer_dict.update({'message': 'There are no invoices /outstanding \
        #                           for this retailer'})
        #     retailer_list.append(retailer_dict)
    return Response(retailer_list)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_retailer_outstanding(request, retailer_id):
    '''
    This method returns the outstanding amount of particular retailer
    '''
    retailer = Retailer.objects.get(retailer_code = retailer_id)
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'
    #for the particular retailer, get all the invoices and total the invoice amount
    invoices = Invoices.objects.filter(retailer__retailer_code = retailer_id, modified_date__gt=modified_since)
    retailer_list = []
    if invoices:
        for invoice in invoices:
            retailer_dict = {}
            outstanding = 0
            collection = 0

            #Checking if the paid amount / invoice amount is None if so then asssign 0.0
            if invoice.paid_amount is None:
                invoice.paid_amount = 0.0
            if invoice.invoice_amount is None:
                invoice.invoice_amount = 0.0

            outstanding = outstanding + (invoice.invoice_amount - invoice.paid_amount)
            retailer_dict.update({'retailer_id':retailer.retailer_code})
            retailer_dict.update({'invoice_id': invoice.id})
            retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
            #get the collections for that invoice
            collection_objs = Collection.objects.filter(invoice_id = invoice.id)
            for each in collection_objs:
                collections = CollectionDetails.objects.filter(collection_id = each.id)
                if collections:
                    for each_collections in collections:
                        collection = collection + each_collections.collected_amount
                    
            retailer_dict.update({'outstanding':outstanding})
            retailer_dict.update({'datetime':datetime.datetime.now()})
            retailer_list.append(retailer_dict)
    return Response(retailer_list)

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
            distributor_dict = {
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
@transaction.commit_manually
def uploadcollection(request):
    '''
    This method gets the collection of payment by dsr and puts it into the collection and collection
    details table
    '''
    collections_body = json.loads(request.POST['uploadcollection'])
    message = ''
    for collection_body in collections_body:
        # get the total order value of the invoice
        invoice = Invoices.objects.get(invoice_id = collection_body['invoice_id'])
        # get the so far collected_amount for that invoice
        coll_details = CollectionDetails.objects.filter(collection__invoice = invoice)
        existing_collection = 0
        for details in coll_details:
            existing_collection = existing_collection + details.collected_amount
        
        # check the collectedamount from the payload is less than or equal to the existing
        # collection for that invoice
        if (collection_body['collected_amount']) <= \
            decimal.Decimal(invoice.invoice_amount) - decimal.Decimal(existing_collection):
            # enter into teh collection table
            collection = Collection()
            collection.invoice = Invoices.objects.get(invoice_id = collection_body['invoice_id'])
            collection.payment_date = collection_body['payment_date']
            collection.dsr = DistributorSalesRep.objects.get(distributor_sales_code = \
                                                                            collection_body['dsr_id'])
            retailer = Retailer.objects.get(retailer_code = collection_body['retailer_id'])
            collection.retailer = retailer
            collection.latitude = collection_body['latitude']
            collection.longitude = collection_body['longitude']
            collection.collected_amount = collection_body['collected_amount']
            collection.save()
            #put data into collection details table
            collectiondetails = CollectionDetails()
            collectiondetails.collection = collection
            collectiondetails.mode = collection_body['payment_mode']
            collectiondetails.collected_amount = collection_body['collected_amount']
            collectiondetails.collected_cash = collection_body['collected_cash']
            for cheque in collection_body['cheque_details']:
                collectiondetails.cheque_bank = cheque['cheque_bank']
                collectiondetails.cheque_number = cheque['cheque_number']
                collectiondetails.cheque_amount = cheque['cheque_amount']
                collectiondetails.img_url = cheque['cheque_image_url']
            collectiondetails.save()
            message = message + '\n' + 'status : 1' + ' ' + \
                      'message : Retailer Collection(s) is updated successfully'
        else:
            message = message + '\n' + 'status : 0' + ' ' + \
                'message : Collection is greater than the invoice amount for the invoice id: ' + collection_body['invoice_id']
    try:
        transaction.commit()
        message = {'status': 1, 'message': 'Collection update successfully'}
    except:
        message = {'status': 0, 'message': 'Collection update failed'}
    send_msg_to_retailer_on_collection(request,retailer.id)
    return Response(message)

@api_view(['POST'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def add_retailer(request, dsr_id):
    ''' this method adds a retailer and his profile from the DSR. Adds data in three tables
    user, userprofile and retailer'''
    retailer_code = ''
    profiles = json.loads(request.POST['retailer'])
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    for profile in profiles:
        user = User()
        user.first_name = profile['first_name']
        user.last_name = profile['last_name']
        # get the latest retailer code and add sequence increment for the new retailer code,
        # if retailer is not there, get the first value in the sequence from the constansts file
        try:
            retailer = Retailer.objects.filter().order_by("-id")[0]
            retailer_code = str(int(retailer.retailer_code) + \
                                            constants.RETAILER_SEQUENCE_INCREMENT)
        except:
            retailer_code = str(constants.RETAILER_SEQUENCE)
        user.username = retailer_code
        user.set_password(constants.RETAILER_PASSWORD)
        user.date_joined = datetime.datetime.now()
        user.is_superuser = False
        user.is_staff = False
        user.is_active = True
        user.save()
        # initialize user profile class
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.date_of_birth = profile['date_of_birth']
        user_profile.state = profile['state']
        user_profile.pincode = profile['pincode']
        user_profile.image_url = profile['image_url']
        user_profile.save()
        # initialize retailer class
        retailer = Retailer()
        retailer.user = user_profile
        retailer.distributor = dsr.distributor
        retailer.retailer_code = retailer_code
        retailer.retailer_name = profile['shop_name']
        retailer.billing_code = profile['billing_code']
        retailer.email = profile['email']
        retailer.mobile = profile['mobile']
        retailer.profile = 'retailer'
        retailer.territory = profile['state']
        retailer.address_line_2 = profile['shop_name'] + ' ' + profile['shop_number']
        retailer.address_line_3 = profile['locality']
        retailer.address_line_4 = profile['tehsil_name'] + ' ' + profile['taluka']
        retailer.retailer_town = profile['town']
        retailer.latitude = profile['latitude']
        retailer.longitude = profile['longitude']
        retailer.district = profile['district']
        retailer.near_dealer_name = profile['near_dealer_name']
        retailer.total_counter_sale = profile['counter_sale']
        retailer.total_sale_parts = profile['total_sale']
        retailer.identification_no = profile['identification_no']
        retailer.image_url = profile['shop_photo']
        retailer.identity_url = profile['identity_url']
        retailer.signature_url = profile['signature_url']
        retailer.mechanic_1 = profile['mechanic_name_1']  + ' ' + profile['mechanic_number_1']
        retailer.mechanic_2 = profile['mechanic_name_2']  + ' ' + profile['mechanic_number_2']
        retailer.approved = constants.STATUS['APPROVED']
        retailer.save()
        send_msg_to_retailer_on_adding(request,retailer,user.username,user.set_password) 
    return Response({'message': 'New retailer(s) added successfully', 'status':1})


@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def dsr_dashboard_report(request, dsr_id):
    today = datetime.datetime.now()
    dsr =  DistributorSalesRep.objects.select_related('distributor').get(distributor_sales_code = dsr_id)
    distributor = dsr.distributor
    retailers_list = []
    retailer_dict = OrderedDict()
    
    # get the retailer objects for this distributor
    retailers = Retailer.objects.filter(distributor = distributor, \
                                        approved = constants.STATUS['APPROVED'])
    retailer_dict.update({"report_type":"month"})
    retailer_dict.update({"total_retailers": retailers.count()})
    
    # calculation of MTD
    achieved_list = []
    days = int(today.strftime("%e")) - 1
    if days == 0:
        retailer_dict.update({"MTD performance": 'NA'})
    else:
        for retailer in retailers:
            if retailer.actual is not None:
                achieved = (retailer.actual * days/ retailer.target) * 100
                achieved_list.append(achieved)
            else:
                achieved = 0
        total_achieved = 0
        for each in achieved_list:
            total_achieved = total_achieved + each
        if len(retailers):
            mtd = str(total_achieved/ len(retailers)) + '%'
            retailer_dict.update({"MTD performance": mtd})
    # calculation of total sales value
    total_sales_value = 0
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                                            created_date__month = today.strftime("%m"))
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
        # sum up the each retailer sales value to the total
        total_sales_value = total_sales_value + retailer_sales_value
    retailer_dict.update({"sales_value": total_sales_value})
    
    # calculation of collected amount
    total_collected_amount = 0
    for retailer in retailers:
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer)
        for collection in collections:    
            # get all the collection details for this collection
            collection.collected_amount = collection.collected_amount if collection.collected_amount else 0
            retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
        total_collected_amount = total_collected_amount + retailer_collected_amount
    retailer_dict.update({"collections": total_collected_amount})
    
    # calculation of zero-billed
    exist_retailers = []
    for retailer in retailers:
        exist_retailers.append(retailer.retailer_code)
    collected_retailers = []
    collection_details = CollectionDetails.objects.filter(created_date__month = \
                        today.strftime("%m")).values('collection__retailer__retailer_code')
    for collection in collection_details:
        collected_retailers.append(collection['collection__retailer__retailer_code'])
    uni = set(collected_retailers)
    zero_billed_retailers = [x for x in exist_retailers if x not in collected_retailers]
    retailer_dict.update({"zero billed retailers": zero_billed_retailers})
    
    # calculation of new retailers enrolled
    # find retailer objects created in the running month and year
    new_retailers = Retailer.objects.filter(Q(created_date__year=today.year),
                                            Q(created_date__month=today.strftime("%m")),
                                            approved = constants.STATUS['APPROVED'])
    new_retailers_list = []
    for new_retailer in new_retailers:
        new_retailers_list.append(new_retailer.retailer_code)
    retailer_dict.update({"new retailers": new_retailers_list})
    
    # calculation of top retailers
    total_sales_value = 0
    top_retailers_dict = {}
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                                            created_date__month = today.strftime("%m"))
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
                top_retailers_dict[retailer.retailer_code] = retailer_sales_value
              
        else:
            top_retailers_dict[retailer.retailer_code] = 0
    s = sorted(top_retailers_dict.items(), key=itemgetter(1), reverse=True)
    s = s[:10]
    top_retailer_name = Retailer.objects.get(retailer_code = s[0][0])
    top_list = []
    for each in s:
        top_dict = {}
        top_dict['id'] = each[0]
        top_dict['amount'] = each[1]
        top_list.append(top_dict)
    retailer_dict['top_retailer_name'] = top_retailer_name.retailer_name
    retailer_dict['top_retailers'] = top_list
    
    # calculation of billed parts count
    parts_count = OrderPartDetails.objects.filter(order__distributor = distributor,
    created_date__month = today.strftime("%m")).values('part_number__description').distinct()
    retailer_dict.update({"BilledPartsCount": len(parts_count)})
    parts = []
    # get what are the parts billed and make a list of that
    for each in parts_count:
        parts.append(each['part_number__description'])
    retailer_dict.update({"Billedparts": parts})
    # calculation of top selling part by quantity
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
                    created_date__month = today.strftime("%m")).order_by('-quantity')[0]
        retailer_dict.update({"top_selling_part_Qty": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_Qty": "NA"})
    
    # calculation of top selling part by order value
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
                    created_date__month = today.strftime("%m")).order_by('-line_total')[0]
        retailer_dict.update({"top_selling_part_value": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_value": 'NA'})
    
    retailers_list.append(retailer_dict)
    
    # loop thro each retailer and get sales value, collection, etc ...
    all_retailers_dict = {}
    all_retailers = []
    for retailer in retailers:
        each_retailer = OrderedDict()
        each_retailer['report_type'] = 'month'
        each_retailer['retailer_id'] = retailer.retailer_code
        # calculation of MTD
        if days == 0 or retailer.actual is None:
            each_retailer['MTD performance'] = 'NA'
        else:
            mtd = str((retailer.actual * days/retailer.target) * 100) + '%'
            each_retailer['MTD performance'] = mtd
        
        # calculation of sales value
        total_sales_value = 0
        orders = OrderPart.objects.filter(retailer = retailer, \
                                                created_date__month = today.strftime("%m"))
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
            # sum up the each retailer sales value to the total
            total_sales_value = total_sales_value + retailer_sales_value
        each_retailer['sales_value'] = total_sales_value
            
        total_collected_amount = 0
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer, \
                                                created_date__month = today.strftime("%m"))
        if collections:
            for collection in collections:    
            # get all the collection details for this collection
                collection.collected_amount = collection.collected_amount if collection.collected_amount else 0
                retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
            total_collected_amount = total_collected_amount + retailer_collected_amount
        each_retailer.update({"collections": total_collected_amount})
        
        #top selling part by quantity
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                    created_date__month = today.strftime("%m")).order_by('-quantity')[0]
            each_retailer.update({"top_selling_part_Qty": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_Qty": 'NA'})
    
        # calculation of top selling part by order value
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                        created_date__month = today.strftime("%m")).order_by('-line_total')[0]
            each_retailer.update({"top_selling_part_value": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_value": 'NA'})
            
        #billed parts count
        parts_count = OrderPartDetails.objects.filter(order__retailer = retailer, \
        created_date__month = today.strftime("%m")).values('part_number__description').distinct()
        each_retailer.update({"BilledPartsCount": len(parts_count)})
        parts = []
        # get what are the parts billed and make a list of that
        for each in parts_count:
            parts.append(each['part_number__description'])
        each_retailer.update({"Billedparts": parts})
        
        all_retailers.append(each_retailer)
        retailers_list.append(each_retailer)
    
    # X MONTHS OLD REPORT
    
    date_str =  str(today.year) + '/' + str(today.strftime('%m')) + '/' + '01'
    first_date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
    previous_date = first_date - timedelta(days=constants.DSR_REPORT_MONTHS_DATA * 30) 
    
    retailer_dict = OrderedDict()
    # get the retailer objects for this distributor
    retailers = Retailer.objects.filter(distributor = distributor, \
                                        approved = constants.STATUS['APPROVED'])
    months_data = str(constants.DSR_REPORT_MONTHS_DATA) + ' ' +'months'
    retailer_dict.update({"report_type": months_data})
    retailer_dict.update({"total_retailers": retailers.count()})
    
    # calculation of MTD
    achieved_list = []
    days = int(today.strftime("%e")) - 1
    if days == 0 or retailer.actual is None:
        retailer_dict.update({"MTD performance": 'NA'})
    else:
        for retailer in retailers:
            if retailer.actual is not None:
                achieved = (retailer.actual * days/ retailer.target) * 100
                achieved_list.append(achieved)
            else:
                achieved = 0
        total_achieved = 0
        for each in achieved_list:
            total_achieved = total_achieved + each
        mtd = str(total_achieved/ len(retailers)) + '%'
        retailer_dict.update({"MTD performance": mtd})
    # calculation of total sales value
    total_sales_value = 0
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                                created_date__gte = previous_date, \
                                created_date__lte = first_date)
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
        # sum up the each retailer sales value to the total
        total_sales_value = total_sales_value + retailer_sales_value
    retailer_dict.update({"sales_value": total_sales_value})
    
    # calculation of collected amount
    total_collected_amount = 0
    for retailer in retailers:
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer, \
                                    created_date__gte = previous_date, \
                                    created_date__lte = first_date)
        for collection in collections:    
            # get all the collection details for this collection
            collection_details = CollectionDetails.objects.filter(collection = collection)
            for collection_detail in collection_details:
                collection.collected_amount = collection.collected_amount if collection.collected_amount else 0
                retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
        total_collected_amount = total_collected_amount + retailer_collected_amount
    retailer_dict.update({"collections": total_collected_amount})
    
    # calculation of zero-billed
    exist_retailers = []
    for retailer in retailers:
        exist_retailers.append(retailer.retailer_code)
    collected_retailers = []
    collection_details = CollectionDetails.objects.filter(created_date__gte = \
                previous_date, created_date__lte = first_date).\
                values('collection__retailer__retailer_code')
    for collection in collection_details:
        collected_retailers.append(collection['collection__retailer__retailer_code'])
    uni = set(collected_retailers)
    zero_billed_retailers = [x for x in exist_retailers if x not in collected_retailers]
    retailer_dict.update({"zero billed retailers": zero_billed_retailers})
    
    # calculation of new retailers enrolled
    # find retailer objects created in the running month and year
    new_retailers = Retailer.objects.filter(Q(created_date__year=today.year),
                                            Q(created_date__month=today.strftime("%m")),
                                            approved = constants.STATUS['APPROVED'])
    new_retailers_list = []
    for new_retailer in new_retailers:
        new_retailers_list.append(new_retailer.retailer_code)
    retailer_dict.update({"new retailers": new_retailers_list})
    
    # calculation of top retailers
    total_sales_value = 0
    top_retailers_dict = {}
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                        created_date__gte = previous_date, created_date__lte = first_date)
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
                top_retailers_dict[retailer.retailer_code] = retailer_sales_value
              
        else:
            top_retailers_dict[retailer.retailer_code] = 0
    s = sorted(top_retailers_dict.items(), key=itemgetter(1), reverse=True)
    s = s[:10]
    top_retailer_name = Retailer.objects.get(retailer_code = s[0][0])
    top_list = []
    for each in s:
        top_dict = {}
        top_dict['id'] = each[0]
        top_dict['amount'] = each[1]
        top_list.append(top_dict)
    retailer_dict['top_retailer_name'] = top_retailer_name.retailer_name
    retailer_dict['top_retailers'] = top_list
    
    # calculation of billed parts count
    parts_count = OrderPartDetails.objects.filter(order__distributor = distributor,
                    created_date__gte = previous_date, created_date__lte = first_date).\
                    values('part_number__description').distinct()
    retailer_dict.update({"BilledPartsCount": len(parts_count)})
    parts = []
    # get what are the parts billed and make a list of that
    for each in parts_count:
        parts.append(each['part_number__description'])
    retailer_dict.update({"Billedparts": parts})
    # calculation of top selling part by quantity
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
                created_date__gte = previous_date, created_date__lte = first_date).\
                order_by('-quantity')[0]
        retailer_dict.update({"top_selling_part_Qty": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_Qty": "NA"})
    
    # calculation of top selling part by order value
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
             created_date__gte = previous_date, created_date__lte = first_date).order_by('-line_total')[0]
        retailer_dict.update({"top_selling_part_value": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_value": 'NA'})
    
    retailers_list.append(retailer_dict)
    
    # loop thro each retailer and get sales value, collection, etc ...
    all_retailers_dict = {}
    all_retailers = []
    for retailer in retailers:
        each_retailer = OrderedDict()
        each_retailer['report_type'] = months_data
        each_retailer['retailer_id'] = retailer.retailer_code
        # calculation of MTD
        if days == 0 or retailer.actual is None:
            each_retailer['MTD performance'] = 'NA'
        else:
            mtd = str((retailer.actual * days/retailer.target) * 100) + '%'
            each_retailer['MTD performance'] = mtd
        
        # calculation of sales value
        total_sales_value = 0
        orders = OrderPart.objects.filter(retailer = retailer, \
                            created_date__gte = previous_date, created_date__lte = first_date)
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
            # sum up the each retailer sales value to the total
            total_sales_value = total_sales_value + retailer_sales_value
        each_retailer['sales_value'] = total_sales_value
            
        total_collected_amount = 0
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer, \
                                created_date__gte = previous_date, created_date__lte = first_date)
        if collections:
            for collection in collections:    
            # get all the collection details for this collection
                collection_details = CollectionDetails.objects.filter(collection = collection)
                for collection_detail in collection_details:
                    retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
            total_collected_amount = total_collected_amount + retailer_collected_amount
        each_retailer.update({"collections": total_collected_amount})
        
        #top selling part by quantity
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                    created_date__gte = previous_date, created_date__lte = first_date).\
                    order_by('-quantity')[0]
            each_retailer.update({"top_selling_part_Qty": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_Qty": 'NA'})
    
        # calculation of top selling part by order value
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                    created_date__gte = previous_date, created_date__lte = first_date).\
                        order_by('-line_total')[0]
            each_retailer.update({"top_selling_part_value": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_value": 'NA'})
            
        #billed parts count
        parts_count = OrderPartDetails.objects.filter(order__retailer = retailer, \
                created_date__gte = previous_date, created_date__lte = first_date).\
                values('part_number__description').distinct()
        each_retailer.update({"BilledPartsCount": len(parts_count)})
        parts = []
        # get what are the parts billed and make a list of that
        for each in parts_count:
            parts.append(each['part_number__description'])
        each_retailer.update({"Billedparts": parts})
        
        all_retailers.append(each_retailer)
        retailers_list.append(each_retailer)
        
    # finally add the dictionary to the list which is sent as the response
    return Response(retailers_list)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_orders(request, dsr_id):
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'    
    order_details = OrderPart.objects.filter(dsr__distributor_sales_code = dsr_id, \
                                            modified_date__gt=modified_since)
    
    orders_list = []
    for order in order_details:
        order_dict = OrderedDict()
        order_dict['order_id'] = order.order_number
        order_dict['retailer_id'] = order.retailer.retailer_code
        order_dict['order_date'] = order.order_date.strftime('%d-%m-%Y')
        order_dict['datetime'] = datetime.datetime.now()
        # check the status of the order and get it from the constants
        for k,v in constants.ORDER_STATUS.iteritems():
            if v == order.order_status:
                order_dict['status'] = k
        amount = 0
        total_line_items = 0
        order_detail = OrderPartDetails.objects.filter(order = order)
        if order_detail:
            for each in order_detail:
                total_line_items = total_line_items + each.quantity
                amount = amount + each.line_total
            order_dict['amount'] = amount
            order_dict['total_quantity'] = total_line_items
            # order details dict
            order_details_list = []
            for each in order_detail:
                order_delivered_obj = OrderDeliveredHistory.objects.filter(part_number=each.part_number, order=each.order).aggregate(Sum('delivered_quantity'))
                order_details_dict = OrderedDict()
                if each.part_number:
                    part_obj = each.part_number
                else:
                    part_obj = each.part_number_catalog

                order_details_dict['part_id'] = part_obj.part_number
                order_details_dict['part_name'] = part_obj.description
                order_details_dict['quantity'] = each.quantity
                if order_delivered_obj.get('delivered_quantity__sum') == None:
                    order_details_dict['delivered_quantity'] = 0
                else:
                    order_details_dict['delivered_quantity'] = order_delivered_obj.get('delivered_quantity__sum')
                order_details_dict['mrp'] = part_obj.mrp
                order_details_dict['line_total'] = each.line_total
                order_details_list.append(order_details_dict)
            order_dict['order_details'] = order_details_list
        orders_list.append(order_dict)
    return Response(orders_list)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_retailer_orders(request, retailer_id):
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'    
    order_details = OrderPart.objects.filter(retailer__retailer_code = retailer_id, \
                                            modified_date__gt=modified_since)
    orders_list = []
    for order in order_details:
        order_dict = OrderedDict()
        order_dict['order_id'] = order.id
        order_dict['retailer_id'] = order.retailer.retailer_code
        order_dict['order_date'] = order.order_date.date()
       	order_dict['distributor_id'] = order.distributor.distributor_id
        order_dict['datetime'] = datetime.datetime.now()
	for k,v in constants.ORDER_STATUS.iteritems():
            if v == order.order_status:
                order_dict['status'] = k

        amount = 0
        order_detail = OrderPartDetails.objects.filter(order = order)
        
        if order_detail:
            for each in order_detail:
                amount = amount + each.line_total
            order_dict['amount'] = amount
            #order_dict['status'] = order.status
            # order details dict
            order_details_list = []
            for each in order_detail:
                order_details_dict = OrderedDict()
                if each.part_number:
                    part_obj = each.part_number
                else:
                    part_obj = each.part_number_catalog
                
                order_details_dict['part_id'] = part_obj.part_number
                order_details_dict['part_name'] = part_obj.description
                order_details_dict['quantity'] = each.quantity
                order_details_dict['mrp'] = part_obj.mrp
                order_details_dict['line_total'] = each.line_total
                order_details_list.append(order_details_dict)
            order_dict['order_details'] = order_details_list
        orders_list.append(order_dict)
    return Response(orders_list)



from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from django.conf import settings
from gladminds.core.services.message_template import get_template
from gladminds.core import utils
from gladminds.core.managers.audit_manager import sms_log
AUDIT_ACTION = 'SEND TO QUEUE'
from gladminds.sqs_tasks import send_loyalty_sms, send_mail_for_sfa_order_placed, send_sfa_order_placed_sms
def send_msg_to_retailer_on_adding(request,retailer_id,username,password):
    retailer_obj = Retailer.objects.get(id=retailer_id)
    phone_number=utils.get_phone_number_format(retailer_obj.mobile)
    message=get_template('SEND_RETAILER_REGISTRATION').format(
                        retailer_name=retailer_obj.user.user.first_name,username=username,password=password)
    sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_loyalty_sms, {'phone_number': phone_number,
                    'message': message, "sms_client": settings.SMS_CLIENT})


def send_msg_to_retailer_on_place_order(request,retailer_id,order_id):
    retailer_obj = Retailer.objects.get(id=retailer_id)
    phone_number=utils.get_phone_number_format(retailer_obj.mobile)
    message=get_template('SEND_RETAILER_ON_ORDER_PLACEMENT').format(
                        retailer_name=retailer_obj.user.user.first_name,order_id=order_id)
    sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_sfa_order_placed_sms, {'phone_number': phone_number,
                    'message': message, "sms_client": settings.SMS_CLIENT})


def send_email_to_retailer_on_place_order(orderpart, orderpart_details_list):
    retailer_obj = orderpart.retailer
    retailer_id = retailer_obj.retailer_code
    retailer_name = orderpart.retailer.retailer_name
    order_number = orderpart.order_number
    distributor_email = retailer_obj.distributor.email_bajaj
    send_job_to_queue(send_mail_for_sfa_order_placed, {'retailer_code': retailer_id,
                        'retailer_name': retailer_name,
                        'order_number': order_number,
                        'distributor_email': distributor_email,
                        'orderpart_details': orderpart_details_list
                    })


def send_msg_to_retailer_on_collection(request,retailer_id):
    print request
    retailer_obj = Retailer.objects.get(id=retailer_id)
    print retailer_obj.mobile
    phone_number=utils.get_phone_number_format(retailer_obj.mobile)
    message=get_template('SEND_RETAILER_ON_COLLECTION').format(
                        retailer_name=retailer_obj.user.user.first_name)
    sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_loyalty_sms, {'phone_number': phone_number,
                    'message': message, "sms_client": settings.SMS_CLIENT})

def get_retailer_dict(retailer):
	retailer_dict={}
	last_order_date = OrderPart.objects.filter(retailer=retailer).order_by('-order_date')
	retailer_dict['firstname'] = retailer.user.user.first_name
	retailer_dict['lastname'] = retailer.user.user.last_name
	retailer_dict['shopname'] = retailer.retailer_name
	if retailer.latitude and retailer.longitude:
	    retailer_dict['latitude'] = str(retailer.latitude)
	    retailer_dict['longitude'] = str(retailer.longitude)
	else:
	    return None
        #for the particular retailer, get all the invoices and total the invoice amount
        invoices = Invoices.objects.filter(retailer__retailer_code = retailer.id)
        if invoices:
            for invoice in invoices:
                retailer_dict = {}
                outstanding = 0
                collection = 0
                outstanding = outstanding + (invoice.invoice_amount - invoice.paid_amount)
                #get the collections for that invoice
                #collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                #for each in collection_objs:
                #    collections = CollectionDetails.objects.filter(collection_id = each.id)
                #    if collections:
                #        for each_collections in collections:
                #            collection = collection + each_collections.collected_amount
	    retailer_dict['outstanding'] = outstanding
	else:
	    retailer_dict['outstanding'] = 0
	if last_order_date:
	    retailer_dict['lastorderdate'] = last_order_date[0].order_date.date()
        else:
            retailer_dict['lastorderdate'] = ''
	retailer_dict['contact'] = retailer.mobile
	#dsr_work_allocation = DSRWorkAllocation.objects.filter(retailer__dsr_id=retailer.dsr_id).order_by('-date')
	dsr_work_allocation = DSRWorkAllocation.objects.filter(dsr=retailer.dsr).order_by('-date')
	##FIXME: Add for all days
	if dsr_work_allocation:
            retailer_dict['day'] = str(dsr_work_allocation[0].pjp_day).lower()
	else:
	    retailer_dict['day'] = 0 
	return retailer_dict

def get_retailer_unassigned_dict(retailer):
    retailer_unassigned_dict={}
    retailer_unassigned_dict['firstname'] = retailer.user.user.first_name
    retailer_unassigned_dict['lastname'] = retailer.user.user.last_name
    retailer_unassigned_dict['shopname'] = retailer.retailer_name
    if retailer.latitude and retailer.longitude:
	    retailer_unassigned_dict['latitude'] = str(retailer.latitude)
	    retailer_unassigned_dict['longitude'] = str(retailer.longitude)
    else:
	    #FIXME: check if object is collected
            return None
    retailer_unassigned_dict['outstanding'] = retailer.retailer_name
    retailer_unassigned_dict['nsm_id'] = retailer.distributor.asm.nsm.nsm_id
    retailer_unassigned_dict['dsr_id'] = retailer.dsr_id
    retailer_unassigned_dict['contact'] = retailer.mobile
    dsr_work_allocation = DSRWorkAllocation.objects.filter(retailer=retailer)
    if dsr_work_allocation:
	    retailer_unassigned_dict['day'] = dsr_work_allocation[0].pjp_day
    return retailer_unassigned_dict

@api_view(['GET'])
def get_associated_nsms(request):	
    nsms = NationalSparesManager.objects.all()
    response_dict = {}
    response_dict['role_id'] = 1
    response_dict['role_name'] = "SFAAdmins"
    response_dict['users'] = []
    response_dict['retailers'] = []
    for nsm in nsms:
        nsm_dict = {}
        nsm_dict['userid'] = nsm.nsm_id
        nsm_dict['firstname'] = nsm.user.user.first_name
        nsm_dict['lastname'] = nsm.user.user.last_name
        nsm_dict['retailers'] = []
	retailers = Retailer.objects.filter(distributor__asm__nsm__nsm_id=nsm.nsm_id).exclude(dsr_id__isnull=True)
	retailers_unassigned = Retailer.objects.filter(dsr_id__isnull=True,distributor__asm__nsm__nsm_id=nsm.nsm_id)
	##FIXME:move the for loops in side the function and update the dict
	for retailer in retailers:
            retailer_dict = get_retailer_dict(retailer)
	    if retailer_dict != None:
	        nsm_dict['retailers'].append(retailer_dict)
        for retailer in retailers_unassigned:
		retailer_unassigned_dict = get_retailer_unassigned_dict(retailer)
	        if retailer_unassigned_dict != None:
                    response_dict['retailers'].append(retailer_unassigned_dict)
	response_dict['users'].append(nsm_dict)
    return Response(response_dict)


@api_view(['GET'])
def get_associated_asms(request,nsm_id=None):
    if nsm_id == None:
        nsm_id=request.GET.__getitem__('nsm_id')
    asms = AreaSparesManager.objects.filter(nsm__nsm_id=nsm_id)
    response_dict = {}
    response_dict['role_id'] = 1
    response_dict['role_name'] = "NationalSparesManager"
    response_dict['users'] = []
    response_dict['retailers'] = []
    for asm in asms:
        asm_dict = {}
        asm_dict['userid'] = asm.asm_id
        asm_dict['firstname'] = asm.user.user.first_name
        asm_dict['lastname'] = asm.user.user.last_name
        asm_dict['retailers'] = []
	retailers = Retailer.objects.filter(distributor__asm__asm_id=asm.asm_id).exclude(dsr_id__isnull=True)
	retailers_unassigned = Retailer.objects.filter(dsr_id__isnull=True,distributor__asm__asm_id=asm.asm_id)
	for retailer in retailers:
             retailer_dict=get_retailer_dict(retailer)
	     if retailer_dict != None:
	         asm_dict['retailers'].append(retailer_dict)
        for retailer in retailers_unassigned:
             retailer_unassigned_dict=get_retailer_unassigned_dict(retailer)
             if retailer_unassigned_dict != None:
		response_dict['retailers'].append(retailer_unassigned_dict)
	response_dict['users'].append(asm_dict)
    return Response(response_dict)


@api_view(['GET'])
def get_associated_distributors(request,asm_id=None):
    if asm_id == None:
        asm_id = request.GET.__getitem__('asm_id')
    distributors = Distributor.objects.filter(asm__asm_id=asm_id)
    response_dict = {}
    response_dict['role_id'] = 1
    response_dict['role_name'] = "AreaSparesManager"
    response_dict['users'] = []
    response_dict['retailers'] = []
    for distributor in distributors:
        distributor_dict = {}
        distributor_dict['userid'] = distributor.distributor_id
        distributor_dict['firstname'] = distributor.user.user.first_name
        distributor_dict['lastname'] = distributor.user.user.last_name
        distributor_dict['retailers'] = []
	retailers = Retailer.objects.filter(distributor__distributor_id=distributor.distributor_id).exclude(dsr_id__isnull=True)
	retailers_unassigned = Retailer.objects.filter(dsr_id__isnull=True,distributor__distributor_id=distributor.distributor_id)
	for retailer in retailers:
             retailer_dict=get_retailer_dict(retailer)
             if retailer_dict != None:
		distributor_dict['retailers'].append(retailer_dict)
        for retailer in retailers_unassigned:
             retailer_unassigned_dict=get_retailer_unassigned_dict(retailer)
             if retailer_unassigned_dict != None:
		response_dict['retailers'].append(retailer_unassigned_dict)
	response_dict['users'].append(distributor_dict)
    return Response(response_dict)


@api_view(['GET'])
def get_associated_dsrs(request,distributor_id=None):
    if distributor_id == None:
        distributor_id = request.GET.__getitem__('distributor_id') #Handle the multivaluedictkey error
    dsrs = DistributorSalesRep.objects.filter(distributor__distributor_id=distributor_id)
    if not dsrs:
        dsrs = DistributorSalesRep.objects.filter(distributor_id=distributor_id)
    response_dict = {}
    response_dict['role_id'] = 1
    response_dict['role_name'] = "Distributor"
    response_dict['users'] = []
    response_dict['retailers'] = []
    for dsr in dsrs:
        dsr_dict = {}
        dsr_dict['userid'] = dsr.distributor_sales_code
        dsr_dict['firstname'] = dsr.user.user.first_name
        dsr_dict['lastname'] = dsr.user.user.last_name
        dsr_dict['retailers'] = []
	retailers = Retailer.objects.filter(dsr_id=dsr.id)#.exclude(dsr_id__isnull=True)
	for retailer in retailers:
             retailer_dict=get_retailer_dict(retailer)
             if retailer_dict != None:
		dsr_dict['retailers'].append(retailer_dict)
        response_dict['users'].append(dsr_dict)
    #Only distributor_id has to be checked for unassigned here
    retailers_unassigned = Retailer.objects.filter(dsr_id__isnull=True,distributor__distributor_id=distributor_id)
    for retailer in retailers_unassigned:
             retailer_unassigned_dict=get_retailer_unassigned_dict(retailer)
             if retailer_unassigned_dict != None:
		response_dict['retailers'].append(retailer_unassigned_dict)
    return Response(response_dict)

@api_view(['GET'])
def get_retailers_actual(request):
    dsr_id = request.GET.__getitem__('dsr_id')
    date_string = request.GET.__getitem__('date')
    date=datetime.datetime.strptime(date_string,'%m-%d-%Y')
    print date
    start_datetime=datetime.datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    retailers=set()
    dsr=DistributorSalesRep.objects.get(distributor_sales_code=dsr_id)
    end_datetime=start_datetime+timedelta(days=1)
    #FIXME:update end_datetime.seconds by -1 second since it is inclusive
    orders=OrderPart.objects.filter(dsr__distributor_sales_code=dsr_id,created_date__range=(start_datetime,end_datetime))
    collections=Collection.objects.filter(dsr__distributor_sales_code=dsr_id,payment_date__range=(start_datetime,end_datetime))
    for each in orders:
        retailers.add(each.retailer)
    for each in collections:
        retailers.add(each.retailer)
    response_dict = {}
    response_dict['date'] = date.date()
    response_dict['users'] = []
    for retailer in retailers:
        #FIXME:Try with order_date and instead of 2 queries use group_by in one query
        last_orders = OrderPart.objects.filter(retailer=retailer,dsr__distributor_sales_code=dsr_id,created_date__range=(start_datetime,end_datetime)).order_by('-created_date')
        retailer_dict = {}
        retailer_dict['userid'] = retailer.retailer_code
        retailer_dict['firstname'] = retailer.user.user.first_name
        retailer_dict['lastname'] = retailer.user.user.last_name
        retailer_dict['shopname'] = retailer.retailer_name
        retailer_dict['contact'] = retailer.mobile
        retailer_dict['outstanding'] = 0#outstanding
        if retailer.latitude and retailer.longitude:
            retailer_dict['latitude'] = retailer.latitude
            retailer_dict['longitude'] = retailer.longitude
        else:
            continue
        retailer_dict['data1'] = []
        order_dict={}
        order_dict['type1']='order'
        total_order=0
        if last_orders:
            order_dict['accepttime']='%s:%s'%(last_orders[0].created_date.hour,last_orders[0].created_date.minute)
            print order_dict['accepttime']
        for order in last_orders:
            order_detail=OrderPartDetails.objects.filter(order=order)
            for each in order_detail:
                total_order+=each.line_total
        order_dict['amount']=total_order
        retailer_dict['data1'].append(order_dict)
        #FIXME:Instead of 2 queries use group_by in one query
        collections_list=Collection.objects.filter(retailer=retailer,dsr__distributor_sales_code=dsr_id,payment_date__range=(start_datetime,end_datetime)).order_by('-payment_date')
        collection_dict={}
        collection_dict['type1'] = "collection"
        collection_value=0
        #FIXME:Displaying only the collected_amount column
        for collection in collections_list:
            collection_value+=collection.collected_amount
        if collections_list:
            collection_dict['accepttime'] = '%s:%s'%(collections_list[0].payment_date.hour,collections_list[0].payment_date.minute)
        collection_dict['amount'] = collection_value 
        retailer_dict['data1'].append(collection_dict)
        response_dict['users'].append(retailer_dict)
    return Response(response_dict)


@api_view(['GET'])
def get_users(request):
# FIXME: Return false other than all the known user roles
# FIXME: Move this method to a more generic location, may be auth_helper
    print request.user.groups.all()
    print request.user.id
    if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
        distributor_id = Distributor.objects.get(user_id=request.user.id).distributor_id
        return get_associated_dsrs(request, distributor_id)
    if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
	asm_id = AreaSparesManager.objects.get(user_id=request.user.id).asm_id
        return get_associated_distributors(request, asm_id)
    if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
	nsm_id = NationalSparesManager.objects.get(user_id=request.user.id).nsm_id
    	return get_associated_asms(request,nsm_id)
    if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
        return get_associated_nsms(request)
    else:
        return Response({'error':'Not an authorized user'}) 

@api_view(['GET'])
def get_collection(request):
    try:
        dsr_id = request.GET.get('dsr_id')
        date = request.GET.get('date')
    except:
        return Response({'error':'parameters missing'})
    collection_details = []
    if date:
        #FIXME:make >(current date-5months)
        collection_obj = Collection.objects.filter(dsr__distributor_sales_code=dsr_id,payment_date__gt=date)
    else:
        collection_obj = Collection.objects.filter(dsr__distributor_sales_code=dsr_id)#,payment_date__gt=datetime.datetime.now())
    for each in collection_obj:
        collection_details_dict = {}
        collection_details_dict['retailer_id'] = each.retailer_id
        collection_details_dict['collection_id'] = each.id
        collection_details_dict['invoice_id'] = each.invoice_id
        collection_details_dict['collected_amount'] = each.collected_amount
        collection_details_dict['date'] = str(each.payment_date)
        collection_details_dict['collection_details'] = []
        more_details_obj = CollectionDetails.objects.filter(collection_id=each.id)
        collected_by_cash=0
        for each_obj in more_details_obj:
            more_details_dict={}
            if each_obj.mode == 1:
                collection_details_dict['mode'] = 1 #'Cash'
                collection_details_dict['collected_by_cash'] = each_obj.collected_cash
                break
            elif each_obj.mode == 2:
                collection_details_dict['mode'] = 2  #'Cheque'
            elif each_obj.mode == 3:
                collection_details_dict['mode'] = 3  #'Cash/Cheque'
                #FIXME: Confirm if the collected_cash is same for all the filtered records
                collection_details_dict['collected_by_cash'] = each_obj.collected_cash
            more_details_dict['cheque_number'] = each_obj.cheque_number
            more_details_dict['cheque_bank'] = each_obj.cheque_bank
            more_details_dict['cheque_img_url'] = str(each_obj.img_url)
            more_details_dict['cheque_amount'] = each_obj.cheque_amount
            collection_details_dict['collection_details'].append(more_details_dict)
        collection_details.append(collection_details_dict)

    return HttpResponse(json.dumps(collection_details), content_type='application/json')


@api_view(['POST'])
def check_updated_order(request):
    data = json.loads(request.body)
    try:
        order_part = OrderPart.objects.get(order_number=str(data["order_id"]))
        order_number = order_part.order_number
        return_data = {order_number:[]}
        for orderpart_detail in order_part.orderpartdetails_set.all():
            return_data[order_number].append(orderpart_detail.part_number.part_number)
        return Response({'order':return_data})
    except OrderPart.DoesNotExist:
        logger.error("order part doesnot exist - {0}".format(data["order_id"]))
    return Response({'order':{order_number:[]}})
    
    

@api_view(['GET'])
@transaction.commit_manually
def update_six_months_retailer_history(request):
    prev_month_list = []
    prev_year_list = []
    for i in range(6):
        prev_date = (datetime.date.today() - datetime.timedelta(i*365/12))
        prev_month_list.append(prev_date.month)
        prev_year_list.append(prev_date.year)
    last_six_months_parts_hist = MonthlyPartSalesHistory.objects.filter\
                            (month__in=prev_month_list, year__in=prev_year_list)
    retailer_part_wise_history = {}
    for obj in last_six_months_parts_hist:
        if not retailer_part_wise_history.get(obj.retailer_id):
            retailer_part_wise_history[obj.retailer_id] = {}
        if retailer_part_wise_history[obj.retailer_id].get(obj.part_id):
            retailer_part_wise_history[obj.retailer_id][obj.part_id] = \
                    retailer_part_wise_history[obj.retailer_id][obj.part_id] + obj.quantity
        else:
            retailer_part_wise_history[obj.retailer_id][obj.part_id] = obj.quantity
    for hist_retailer in retailer_part_wise_history:
        for hist_part in retailer_part_wise_history[hist_retailer]:
            avg_quantity = retailer_part_wise_history[hist_retailer][hist_part] / 6
            avg_retailer_sales_history_obj_list = \
                AverageRetailerSalesHistory.objects.filter(part_id=hist_part, \
                                                        retailer_id=hist_retailer)
            if avg_retailer_sales_history_obj_list:
                avg_retailer_sales_history_obj = avg_retailer_sales_history_obj_list[0]
                avg_retailer_sales_history_obj.quantity = avg_quantity
            else:
                avg_retailer_sales_history_obj = \
                    AverageRetailerSalesHistory(part_id=hist_part, quantity=avg_quantity, \
                                                            retailer_id=hist_retailer)
            avg_retailer_sales_history_obj.save()
    transaction.commit()
    return HttpResponse(json.dumps({'status': 'completed'}), content_type='application/json')


@api_view(['GET'])
@transaction.commit_manually
def update_six_months_location_history(request):
    retailer_avg_part_hist = AverageRetailerSalesHistory.objects.all()
    locality_part_wise_history = {}
    for hist_obj in retailer_avg_part_hist:
        locality_id = hist_obj.retailer.locality_id
        if not locality_part_wise_history.get(locality_id):
            locality_part_wise_history[locality_id] = {}
        if locality_part_wise_history[locality_id].get(hist_obj.part_id):
            locality_part_wise_history[locality_id][hist_obj.part_id] = \
                    locality_part_wise_history[locality_id][hist_obj.part_id] + hist_obj.quantity
        else:
            locality_part_wise_history[locality_id][hist_obj.part_id] = hist_obj.quantity
    for hist_locality in locality_part_wise_history:
        for hist_part in locality_part_wise_history[hist_locality]:
            avg_quantity = locality_part_wise_history[hist_locality][hist_part]
            average_locality_sales_history_list = \
                AverageLocalitySalesHistory.objects.filter(locality_id=hist_locality, part_id=hist_part)
            if average_locality_sales_history_list:
                average_locality_sales_history = average_locality_sales_history_list[0]
                average_locality_sales_history.quantity = avg_quantity
            else:
                average_locality_sales_history = \
                    AverageLocalitySalesHistory(part_id=hist_part, quantity=avg_quantity, \
                                                            locality_id=hist_locality)
            average_locality_sales_history.save()
    transaction.commit()
    return HttpResponse(json.dumps({'status': 'completed'}), content_type='application/json')


@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def dsr_average_orders(request, dsr_id):
    '''
    This method returns the sale average of last 6 months
    retailer wise
    '''
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))
    limit = limit + offset
    dsr =  DistributorSalesRep.objects.select_related('distributor').get(distributor_sales_code = dsr_id)
    distributor = dsr.distributor
    retailers_list = []
    # get the retailer objects for this distributor
    retailers = Retailer.objects.filter(distributor = distributor)
    average_retailer_history = AverageRetailerSalesHistory.objects.filter(retailer__in=retailers)[offset:limit]
    part_wise_average_dict = []
    for retailer_hist in average_retailer_history:
        average_dict = {}
        average_dict['retailer_id'] = retailer_hist.retailer.retailer_code
        average_dict['part_number'] = retailer_hist.part.part_number
        average_dict['retailer_average'] = retailer_hist.quantity
        locality_avg = AverageLocalitySalesHistory.objects.filter(locality=retailer_hist.retailer.locality)
        if locality_avg:
            average_dict['locality_average'] = locality_avg[0].quantity
        else:
            average_dict['locality_average'] = 0
        part_wise_average_dict.append(average_dict)
    return Response(part_wise_average_dict)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def pending_orders(request):
    retailer_code = request.GET.get('retailer_id')
    dsr_code = request.GET.get('dsr_id')
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'    
    if dsr_code:
        distributor = DistributorSalesRep.objects.get(distributor_sales_code = dsr_code)
        retailers = Retailer.objects.filter(distributor = distributor.distributor, \
                                      approved = constants.STATUS['APPROVED'] )
    else:
        retailers = Retailer.objects.filter(retailer_code=retailer_code, \
                                      approved = constants.STATUS['APPROVED'] )
    orderpart_details_obj_list = OrderPartDetails.objects.filter(\
                    order__retailer__in=retailers, modified_date__gt=modified_since).order_by('-id')
    delivered_order_obj_list = OrderDeliveredHistory.objects.filter(\
                    order__retailer__in=retailers, modified_date__gt=modified_since).order_by('-id')
    pending_orders_list = []
    counter = 0
    # Iterating only first 1000 order detail records, way too old orders should not be relevant
    iter_orderpart_details_obj_list = orderpart_details_obj_list[:1000]
    for orderpart_detail_obj in iter_orderpart_details_obj_list:
        # Tracking 20 back orders.
        if counter > 20:
            break
        pending_order_dict = {}
        order_obj = orderpart_detail_obj.order
        part_number = orderpart_detail_obj.part_number
        delivered_obj_list = delivered_order_obj_list.filter(order=order_obj, part_number=part_number)
        if not delivered_obj_list:
            pending_quantity = orderpart_detail_obj.quantity
        else:
            # Assuming unique part numbers per order. Take the first record in case of multiple values
            delivered_obj = delivered_obj_list[0]
            delivered_quantity = delivered_obj.delivered_quantity
            ordered_quantity = orderpart_detail_obj.quantity
            pending_quantity = int(ordered_quantity) - int(delivered_quantity)
        if pending_quantity > 0:
            pending_order_dict['retailer_id'] = order_obj.retailer.retailer_code
            pending_order_dict['part_number'] = orderpart_detail_obj.part_number.part_number
            pending_order_dict['part_quantity'] = orderpart_detail_obj.quantity
            pending_order_dict['part_description'] = orderpart_detail_obj.part_number.description
            pending_order_dict['datetime'] = datetime.datetime.now()
            ordered_date =  None
            if orderpart_detail_obj.order.order_date:
                ordered_date = orderpart_detail_obj.order.order_date.date()
            pending_order_dict['order_date'] = ordered_date
            pending_orders_list.append(pending_order_dict)
            counter = counter + 1 
    return Response(pending_orders_list)


@api_view(['GET'])
def dsr_dashboard_report_from_to(request, dsr_id, from_date, to_date):
    today = datetime.datetime.now()
    dsr =  DistributorSalesRep.objects.select_related('distributor').get(distributor_sales_code = dsr_id)
    distributor = dsr.distributor
    retailers_list = []
    retailer_dict = OrderedDict()
    
    # get the retailer objects for this distributor
    retailers = Retailer.objects.filter(distributor = distributor, \
                                        approved = constants.STATUS['APPROVED'])
    retailer_dict.update({"report_type":"month"})
    retailer_dict.update({"total_retailers": retailers.count()})
    
    # calculation of MTD
    achieved_list = []
    days = int(today.strftime("%e")) - 1
    if days == 0:
        retailer_dict.update({"MTD performance": 'NA'})
    else:
        for retailer in retailers:
            if retailer.actual is not None:
                achieved = (retailer.actual * days/ retailer.target) * 100
                achieved_list.append(achieved)
            else:
                achieved = 0
        total_achieved = 0
        for each in achieved_list:
            total_achieved = total_achieved + each
        if len(retailers):
            mtd = str(total_achieved/ len(retailers)) + '%'
            retailer_dict.update({"MTD performance": mtd})
    # calculation of total sales value
    total_sales_value = 0
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                                            created_date__month = today.strftime("%m"))
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
        # sum up the each retailer sales value to the total
        total_sales_value = total_sales_value + retailer_sales_value
    retailer_dict.update({"sales_value": total_sales_value})
    
    # calculation of collected amount
    total_collected_amount = 0
    for retailer in retailers:
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer)
        for collection in collections:    
            # get all the collection details for this collection
            collection.collected_amount = collection.collected_amount if collection.collected_amount else 0
            retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
        total_collected_amount = total_collected_amount + retailer_collected_amount
    retailer_dict.update({"collections": total_collected_amount})
    
    # calculation of zero-billed
    exist_retailers = []
    for retailer in retailers:
        exist_retailers.append(retailer.retailer_code)
    collected_retailers = []
    collection_details = CollectionDetails.objects.filter(created_date__month = \
                        today.strftime("%m")).values('collection__retailer__retailer_code')
    for collection in collection_details:
        collected_retailers.append(collection['collection__retailer__retailer_code'])
    uni = set(collected_retailers)
    zero_billed_retailers = [x for x in exist_retailers if x not in collected_retailers]
    retailer_dict.update({"zero billed retailers": zero_billed_retailers})
    
    # calculation of new retailers enrolled
    # find retailer objects created in the running month and year
    new_retailers = Retailer.objects.filter(Q(created_date__year=today.year),
                                            Q(created_date__month=today.strftime("%m")),
                                            approved = constants.STATUS['APPROVED'])
    new_retailers_list = []
    for new_retailer in new_retailers:
        new_retailers_list.append(new_retailer.retailer_code)
    retailer_dict.update({"new retailers": new_retailers_list})
    
    # calculation of top retailers
    total_sales_value = 0
    top_retailers_dict = {}
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                                            created_date__month = today.strftime("%m"))
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
                top_retailers_dict[retailer.retailer_code] = retailer_sales_value
              
        else:
            top_retailers_dict[retailer.retailer_code] = 0
    s = sorted(top_retailers_dict.items(), key=itemgetter(1), reverse=True)
    s = s[:10]
    top_retailer_name = Retailer.objects.get(retailer_code = s[0][0])
    top_list = []
    for each in s:
        top_dict = {}
        top_dict['id'] = each[0]
        top_dict['amount'] = each[1]
        top_list.append(top_dict)
    retailer_dict['top_retailer_name'] = top_retailer_name.retailer_name
    retailer_dict['top_retailers'] = top_list
    
    # calculation of billed parts count
    parts_count = OrderPartDetails.objects.filter(order__distributor = distributor,
    created_date__month = today.strftime("%m")).values('part_number__description').distinct()
    retailer_dict.update({"BilledPartsCount": len(parts_count)})
    parts = []
    # get what are the parts billed and make a list of that
    for each in parts_count:
        parts.append(each['part_number__description'])
    retailer_dict.update({"Billedparts": parts})
    # calculation of top selling part by quantity
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
                    created_date__month = today.strftime("%m")).order_by('-quantity')[0]
        retailer_dict.update({"top_selling_part_Qty": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_Qty": "NA"})
    
    # calculation of top selling part by order value
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
                    created_date__month = today.strftime("%m")).order_by('-line_total')[0]
        retailer_dict.update({"top_selling_part_value": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_value": 'NA'})
    
    retailers_list.append(retailer_dict)
    
    # loop thro each retailer and get sales value, collection, etc ...
    all_retailers_dict = {}
    all_retailers = []
    for retailer in retailers:
        each_retailer = OrderedDict()
        each_retailer['report_type'] = 'month'
        each_retailer['retailer_id'] = retailer.retailer_code
        # calculation of MTD
        if days == 0 or retailer.actual is None:
            each_retailer['MTD performance'] = 'NA'
        else:
            mtd = str((retailer.actual * days/retailer.target) * 100) + '%'
            each_retailer['MTD performance'] = mtd
        
        # calculation of sales value
        total_sales_value = 0
        orders = OrderPart.objects.filter(retailer = retailer, \
                                                created_date__month = today.strftime("%m"))
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
            # sum up the each retailer sales value to the total
            total_sales_value = total_sales_value + retailer_sales_value
        each_retailer['sales_value'] = total_sales_value
            
        total_collected_amount = 0
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer, \
                                                created_date__month = today.strftime("%m"))
        if collections:
            for collection in collections:    
            # get all the collection details for this collection
                collection.collected_amount = collection.collected_amount if collection.collected_amount else 0
                retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
            total_collected_amount = total_collected_amount + retailer_collected_amount
        each_retailer.update({"collections": total_collected_amount})
        
        #top selling part by quantity
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                    created_date__month = today.strftime("%m")).order_by('-quantity')[0]
            each_retailer.update({"top_selling_part_Qty": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_Qty": 'NA'})
    
        # calculation of top selling part by order value
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                        created_date__month = today.strftime("%m")).order_by('-line_total')[0]
            each_retailer.update({"top_selling_part_value": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_value": 'NA'})
            
        #billed parts count
        parts_count = OrderPartDetails.objects.filter(order__retailer = retailer, \
        created_date__month = today.strftime("%m")).values('part_number__description').distinct()
        each_retailer.update({"BilledPartsCount": len(parts_count)})
        parts = []
        # get what are the parts billed and make a list of that
        for each in parts_count:
            parts.append(each['part_number__description'])
        each_retailer.update({"Billedparts": parts})
        
        all_retailers.append(each_retailer)
        retailers_list.append(each_retailer)
    
    # X MONTHS OLD REPORT
    
    date_str =  str(today.year) + '/' + str(today.strftime('%m')) + '/' + '01'
    #first_date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
    #previous_date = first_date - timedelta(days=constants.DSR_REPORT_MONTHS_DATA * 30) 
    previous_date=datetime.datetime.strptime( from_date , "%d%m%Y").date()
    first_date=datetime.datetime.strptime( to_date , "%d%m%Y").date()
    
    retailer_dict = OrderedDict()
    # get the retailer objects for this distributor
    retailers = Retailer.objects.filter(distributor = distributor, \
                                        approved = constants.STATUS['APPROVED'])
    months_data = str(constants.DSR_REPORT_MONTHS_DATA) + ' ' +'months'
    retailer_dict.update({"report_type": months_data})
    retailer_dict.update({"total_retailers": retailers.count()})
    
    # calculation of MTD
    achieved_list = []
    days = int(today.strftime("%e")) - 1
    if days == 0 or retailer.actual is None:
        retailer_dict.update({"MTD performance": 'NA'})
    else:
        for retailer in retailers:
            if retailer.actual is not None:
                achieved = (retailer.actual * days/ retailer.target) * 100
                achieved_list.append(achieved)
            else:
                achieved = 0
        total_achieved = 0
        for each in achieved_list:
            total_achieved = total_achieved + each
        mtd = str(total_achieved/ len(retailers)) + '%'
        retailer_dict.update({"MTD performance": mtd})
    # calculation of total sales value
    total_sales_value = 0
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                                created_date__gte = previous_date, \
                                created_date__lte = first_date)
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
        # sum up the each retailer sales value to the total
        total_sales_value = total_sales_value + retailer_sales_value
    retailer_dict.update({"sales_value": total_sales_value})
    
    # calculation of collected amount
    total_collected_amount = 0
    for retailer in retailers:
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer, \
                                    created_date__gte = previous_date, \
                                    created_date__lte = first_date)
        for collection in collections:    
            # get all the collection details for this collection
            collection_details = CollectionDetails.objects.filter(collection = collection)
            for collection_detail in collection_details:
                collection.collected_amount = collection.collected_amount if collection.collected_amount else 0
                retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
        total_collected_amount = total_collected_amount + retailer_collected_amount
    retailer_dict.update({"collections": total_collected_amount})
    
    # calculation of zero-billed
    exist_retailers = []
    for retailer in retailers:
        exist_retailers.append(retailer.retailer_code)
    collected_retailers = []
    collection_details = CollectionDetails.objects.filter(created_date__gte = \
                previous_date, created_date__lte = first_date).\
                values('collection__retailer__retailer_code')
    for collection in collection_details:
        collected_retailers.append(collection['collection__retailer__retailer_code'])
    uni = set(collected_retailers)
    zero_billed_retailers = [x for x in exist_retailers if x not in collected_retailers]
    retailer_dict.update({"zero billed retailers": zero_billed_retailers})
    
    # calculation of new retailers enrolled
    # find retailer objects created in the running month and year
    new_retailers = Retailer.objects.filter(Q(created_date__year=today.year),
                                            Q(created_date__month=today.strftime("%m")),
                                            approved = constants.STATUS['APPROVED'])
    new_retailers_list = []
    for new_retailer in new_retailers:
        new_retailers_list.append(new_retailer.retailer_code)
    retailer_dict.update({"new retailers": new_retailers_list})
    
    # calculation of top retailers
    total_sales_value = 0
    top_retailers_dict = {}
    for retailer in retailers:
        orders = OrderPart.objects.filter(retailer = retailer, \
                        created_date__gte = previous_date, created_date__lte = first_date)
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
                top_retailers_dict[retailer.retailer_code] = retailer_sales_value
              
        else:
            top_retailers_dict[retailer.retailer_code] = 0
    s = sorted(top_retailers_dict.items(), key=itemgetter(1), reverse=True)
    s = s[:10]
    top_retailer_name = Retailer.objects.get(retailer_code = s[0][0])
    top_list = []
    for each in s:
        top_dict = {}
        top_dict['id'] = each[0]
        top_dict['amount'] = each[1]
        top_list.append(top_dict)
    retailer_dict['top_retailer_name'] = top_retailer_name.retailer_name
    retailer_dict['top_retailers'] = top_list
    
    # calculation of billed parts count
    parts_count = OrderPartDetails.objects.filter(order__distributor = distributor,
                    created_date__gte = previous_date, created_date__lte = first_date).\
                    values('part_number__description').distinct()
    retailer_dict.update({"BilledPartsCount": len(parts_count)})
    parts = []
    # get what are the parts billed and make a list of that
    for each in parts_count:
        parts.append(each['part_number__description'])
    retailer_dict.update({"Billedparts": parts})
    # calculation of top selling part by quantity
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
                created_date__gte = previous_date, created_date__lte = first_date).\
                order_by('-quantity')[0]
        retailer_dict.update({"top_selling_part_Qty": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_Qty": "NA"})
    
    # calculation of top selling part by order value
    try:
        tsp = OrderPartDetails.objects.filter(order__distributor = distributor, \
             created_date__gte = previous_date, created_date__lte = first_date).order_by('-line_total')[0]
        retailer_dict.update({"top_selling_part_value": tsp.part_number.description})
    except:
        retailer_dict.update({"top_selling_part_value": 'NA'})
    
    retailers_list.append(retailer_dict)
    
    # loop thro each retailer and get sales value, collection, etc ...
    all_retailers_dict = {}
    all_retailers = []
    for retailer in retailers:
        each_retailer = OrderedDict()
        each_retailer['report_type'] = months_data
        each_retailer['retailer_id'] = retailer.retailer_code
        # calculation of MTD
        if days == 0 or retailer.actual is None:
            each_retailer['MTD performance'] = 'NA'
        else:
            mtd = str((retailer.actual * days/retailer.target) * 100) + '%'
            each_retailer['MTD performance'] = mtd
        
        # calculation of sales value
        total_sales_value = 0
        orders = OrderPart.objects.filter(retailer = retailer, \
                            created_date__gte = previous_date, created_date__lte = first_date)
        retailer_sales_value = 0
        if orders:
            for order in orders:
                # get all the order details and sum up the line total
                order_details = OrderPartDetails.objects.filter(order = order)
                for order_detail in order_details:
                    retailer_sales_value = retailer_sales_value + order_detail.line_total
            # sum up the each retailer sales value to the total
            total_sales_value = total_sales_value + retailer_sales_value
        each_retailer['sales_value'] = total_sales_value
            
        total_collected_amount = 0
        # get all the invoices for this retailer
        retailer_collected_amount = 0
        collections = Collection.objects.filter(retailer = retailer, \
                                created_date__gte = previous_date, created_date__lte = first_date)
        if collections:
            for collection in collections:    
            # get all the collection details for this collection
                collection_details = CollectionDetails.objects.filter(collection = collection)
                for collection_detail in collection_details:
                    retailer_collected_amount = retailer_collected_amount + \
                                            collection.collected_amount
        # sum up the each retailer collected amount to the total
            total_collected_amount = total_collected_amount + retailer_collected_amount
        each_retailer.update({"collections": total_collected_amount})
        
        #top selling part by quantity
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                    created_date__gte = previous_date, created_date__lte = first_date).\
                    order_by('-quantity')[0]
            each_retailer.update({"top_selling_part_Qty": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_Qty": 'NA'})
    
        # calculation of top selling part by order value
        try:
            tsp = OrderPartDetails.objects.filter(order__retailer = retailer, \
                    created_date__gte = previous_date, created_date__lte = first_date).\
                        order_by('-line_total')[0]
            each_retailer.update({"top_selling_part_value": tsp.part_number.description})
        except:
            each_retailer.update({"top_selling_part_value": 'NA'})
            
        #billed parts count
        parts_count = OrderPartDetails.objects.filter(order__retailer = retailer, \
                created_date__gte = previous_date, created_date__lte = first_date).\
                values('part_number__description').distinct()
        each_retailer.update({"BilledPartsCount": len(parts_count)})
        parts = []
        # get what are the parts billed and make a list of that
        for each in parts_count:
            parts.append(each['part_number__description'])
        each_retailer.update({"Billedparts": parts})
        
        all_retailers.append(each_retailer)
        retailers_list.append(each_retailer)
        
    # finally add the dictionary to the list which is sent as the response
    return Response(retailers_list)

@api_view(['POST'])
def updateCreditLimit(request):
    data = request.body
    retailer_code = data.split('&')[1].split('=')[1]
    credit_limit = data.split('&')[2].split('=')[1]
    try:
        retailer = Retailer.objects.get(retailer_code=retailer_code)
        retailer.credit_limit = credit_limit
        retailer.save()
    except Retailer.DoesNotExist:
        logger.error("Retailer doesnot exist - {0}".format(retailer_code))
        return Response({"message":"Updated Not Sucessfull"})
    return Response({"message":"Updated Sucessfull"})
