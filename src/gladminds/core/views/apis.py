'''
author: araskumar.a
date: 31-08-2015
'''
import json, datetime, time, decimal,logging
from datetime import timedelta
from collections import OrderedDict
from operator import itemgetter
from django.db import transaction
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.db.models import Q, Count, Max

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.settings import api_settings

from gladminds.core.models import Distributor, DistributorSalesRep, Retailer, CvCategories, \
            OrderPart, OrderPartDetails,DSRWorkAllocation, AlternateParts, Collection, \
            CollectionDetails,PartMasterCv,RetailerCollection,PartsStock, Invoices, \
            UserProfile, PartIndexDetails, PartIndexPlates, PartPricing, FocusedPart, \
            SalesReturnHistory, Invoices
from gladminds.core import constants
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from django.conf import settings
from gladminds.core.services.message_template import get_template
from gladminds.core import utils
from gladminds.core.managers.audit_manager import sms_log
from gladminds.sqs_tasks import send_loyalty_sms, send_mail_for_sfa_order_placed, send_sfa_order_placed_sms
from dateutil.relativedelta import relativedelta
import math

AUDIT_ACTION = 'SEND TO QUEUE'

logger = logging.getLogger("gladminds")

today = datetime.datetime.now()
@api_view(['POST'])
def authentication(request):
    '''
    This method is an api gets username and password, authenticates it and sends
    a token as response
    '''
    #load the json input of username and password as json
    load = json.loads(request.body)
    load = request.data
    user = authenticate(username = load["username"], password = load["password"])
    
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

########### This API fetches all the retailers for the given distributor #####################
########### This API is called via the PJP routine by the change_list.html ################### 
@api_view(['GET'])
def get_retailers_for_distributor(request, dsr_id):
    dsr = DistributorSalesRep.objects.get(distributor_sales_code=dsr_id)
    if( dsr ): # check if the dsr is fetched / exists
        retailers = list(dsr.retailer_set.all())
        if( retailers ): # check if dsr has retailers
            return_retailer = []
            for retailer in retailers:
                return_retailer.append( retailer.retailer_name )
            return Response( return_retailer )
    return Response([]) # if the dsr doesnt have retialer return blank list
########### End of Get Retailer For Distributor ##############################################


########### MTD logic to get the number of parts ordered from 1 -> till date ##########
@api_view(['GET'])
def retailer_mtd_six_months_average(request, dsr_id):
    month_start_object = datetime.datetime.now().replace(day=1) # This is the object that holds the 1st of current month -> type:datetime used
    month_start_str = month_start_object.strftime("%Y-%m-%d") # this is the formatted object YYYY-MM-DD
    month_current = datetime.datetime.now().strftime("%Y-%m-%d")
    month_six_before = (month_start_object - relativedelta(months=6)).strftime("%Y-%m-%d")
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = dsr_id)
    retailers = dsr.distributor.retailer_set.all()
    output = []
    for retailer in retailers:
        line_total = 0.0
        six_month_total = 0.0
        retailer_dict = {}
        orderpart_set = retailer.orderpart_set.filter(  order_date__gt=month_six_before,\
                                                        order_date__lt=month_current)
        for orderpart in orderpart_set.filter( order_date__gt=month_start_str,\
                                                order_date__lt=month_current):
            for orderpart_detail in orderpart.orderpartdetails_set.all():
                line_total += orderpart_detail.line_total
        for orderpart in orderpart_set:
            for orderpart_detail in orderpart.orderpartdetails_set.all():
                six_month_total += orderpart_detail.line_total
        retailer_dict['retailer_code'] = retailer.retailer_code
        retailer_dict['retailer_mtd'] = line_total
        retailer_dict['retailer_avg'] = math.ceil(six_month_total/6)
        retailer_dict['mtd'] = part_number_to_quantity
        output.append( retailer_dict )
    return Response(output)

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
                                        approved = constants.STATUS['APPROVED'], \
                                        modified_date__gt=modified_since)
    retailer_list = []
    for retailer in retailers:
        retailer_dict = {}
        retailer_dict.update({"retailer_Id":retailer.retailer_code})
        retailer_dict.update({"retailer_name":retailer.retailer_name})
        retailer_dict.update({"retailer_mobile":retailer.mobile})
        retailer_dict.update({"retailer_email":retailer.email})
        retailer_dict.update({"retailer_address":retailer.user.address})
        retailer_dict.update({"locality":retailer.address_line_4})
        if retailer.locality:
            retailer_dict["locality"] = retailer.locality.name
            retailer_dict.update({"city":retailer.locality.city.city})
            retailer_dict.update({"state":retailer.locality.city.state.state_name})
            retailer_dict.update({"locality_id":retailer.locality_id})
        else:
            retailer_dict.update({"city":''})
            retailer_dict.update({"state":''})
            retailer_dict.update({"locality_id":''})
        if not retailer.latitude or not retailer.longitude:
            retailer.latitude=''
            retailer.longitude=''
        retailer_dict.update({"latitude":str(retailer.latitude)})
        retailer_dict.update({"longitude":str(retailer.longitude)})
        retailer_dict.update({"datetime": datetime.datetime.now()})
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
        if retailer.address_line_4 is not None:
            retailer_dict.update({"locality":retailer.address_line_4 + \
                              ' ' + retailer.retailer_town})
        else:
            retailer_dict.update({"locality": retailer.retailer_town})
        retailer_dict.update({"latitude":retailer.latitude})
        retailer_dict.update({"longitude":retailer.longitude})
        return Response(retailer_dict)


from django.conf import settings
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
            orderpart_details_list =  []
            #push all the items into the orderpart details
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

                    #return Response({'error': 'Part '+ item['part_number'] +' not found'})
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
            # TODO: Add logger to it
            pass 
    return Response({'message': 'Order updated successfully', 'status':1})
 

import copy
@api_view(['GET'])
def load_parts_temp(request):
    parts_list = [['24101900','AP101146','3100338','39121420','24130105','39100006','36244050','36244059','36244060','36244071'],
            ]
    for parts in parts_list:
        print '--------------PARTS LIST--------------------'
        print parts
        for part_number in parts:
            try:
                parts_modified = copy.copy(parts)
                parts_modified.remove(part_number)
                part = PartPricing.objects.get(part_number=part_number)
                print '------------------PART---------------------'
                print 'Part Number : ' , part.part_number
                associated_part = [ i.part_number for i in part.associated_parts.all() ]
                difference = list( set(parts_modified) - set(associated_part))
                print 'Missing Parts : ', difference
                print 'Associated Part : ', associated_part
                print '-------------------------------------------'
            except PartPricing.DoesNotExist:
                print 'This Part Doesnt exist : ', part_number

    return Response({"200":"done....."})


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
    parts = PartPricing.objects.filter(part_number='AP121073')
    #parts = PartPricing.objects.filter(active = True, modified_date__gt=modified_since)
    parts_list =[]
    for part in parts:
        #available_quantity = PartsStock.objects.get(part_number_id = part.id ).available_quantity
        available_quantity = 'NA'
        parts_dict = {}
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_category":part.subcategory.name})
        associated_part_list = associated_parts(part)
        #associated_part_list = [ associated_part.part_number for associated_part in part.associated_parts.all() if part.associated_parts.all()]
        parts_dict.update({"associated_categories_str": associated_part_list})
        try:
            available_quantity = PartsStock.objects.get(part_number = part)
        except:
            available_quantity = 'NA'
        if available_quantity == 'NA':
            parts_dict.update({"part_available_quantity":'NA'})
        else:
            parts_dict.update({"part_available_quantity":available_quantity.available_quantity})
        parts_dict.update({"part_products":part.products})
        parts_dict.update({"mrp":part.mrp})
        parts_dict.update({"datetime": datetime.datetime.now()})
        parts_list.append(parts_dict)
    return Response(parts_list)


def associated_parts(part):
    '''
    returns all the associated parts for a part object
    '''
    associated_parts_obj_list = part.associated_parts.all()
    associated_part_number_list = list(associated_parts_obj_list.values_list('part_number', flat=True))
    for associated_part in associated_parts_obj_list:
        associated_part_number_list.extend(associated_part.associated_parts.values_list('part_number', flat=True))
    return set(associated_part_number_list)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_associated_parts(request):
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
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_model":part.plate.model.model_name})
        parts_dict.update({"part_plate":part.plate.plate_name})
        parts_dict.update({"quantity":part.quantity})
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

@api_view(['POST'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def pjp_schedule(request):
    '''
    This method gets the schedule of the DSR from the payload/signature, and puts
    it into the database
    '''
    schedules= json.loads(request.body)
    pjp_creation_date = schedules['pjp_creation_date']#FIXME: Ignoring the creation date
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = schedules['dsr_id'])
    dsr_work_allocations = DSRWorkAllocation.objects.filter(dsr__distributor_sales_code = schedules['dsr_id'], is_active = True)
    for dsrwa in dsr_work_allocations:
        dsrwa.is_active = False
	dsrwa.save()
    for location_details in schedules['pjp_location_details']:
        dsrworkallocation = DSRWorkAllocation()
        dsrworkallocation.dsr = dsr
        dsrworkallocation.distributor = dsr.distributor
        dsrworkallocation.date = datetime.datetime.now()#schedules.get('pjp_creation_date')
        dsrworkallocation.locality_id = location_details['locality_id']
        dsrworkallocation.is_active = True
        dsrworkallocation.pjp_day = location_details.get('pjp_day')
        dsrworkallocation.save()
    return Response({'status':1, 'message':'DSR schedule has been submitted'})

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_schedule(request, dsr_id):
    '''
    This method gets the latest week-schedule(the retailers he has to visit) given the dsr id
    '''
    
    schedules = DSRWorkAllocation.objects.filter(dsr__distributor_sales_code = dsr_id, is_active = True)#__isnull = True)
    if schedules:                   
        schedules_list = []
        for schedule in schedules:
            schedule_dict = {}
            schedule_dict['locality_id'] = schedule.locality_id
            schedule_dict['pjp_day'] = schedule.pjp_day
            try:
                if schedule.locality:
                    schedule_dict['locality_name'] = schedule.locality.name
            except:
                schedule_dict['locality_name'] = 'Locality missing'
            #schedule_dict.update({"retailer_code" : schedule.retailer.retailer_code})
            #schedule_dict.update({"retailer_name" : schedule.retailer.retailer_name})
            #tm = time.strptime(str(schedule.date.time()), "%H:%M:%S")
            #schedule_dict.update({"Time" : time.strftime("%I:%M %p", tm)})
            #schedule_dict.update({"retailer_address":schedule.retailer.user.address})
            #schedule_dict.update({"latitude":schedule.retailer.latitude})
            #schedule_dict.update({"longitude":schedule.retailer.longitude})
            schedules_list.append(schedule_dict)
        return Response(schedules_list)
    else:
        return Response({'status':0, 'message':'There are no schedules for the DSR'})

@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_stock(request,dsr_id):
    '''
    This method returns all the stock details
    '''
    #get the disributor id
    modified_since = request.GET.get('modified_since', '1970-01-01')
    if not modified_since:
        modified_since = '1970-01-01'
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
            stock_list.append(parts_dict)
        except:
            # FIXME: Remove try except from here and confirm if exceptions are due to curropt data
            pass
    return Response(stock_list)


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
            orderpart_details_list = []
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
        # TODO: Add logger to it
        pass 
    return Response({'message': 'Order updated successfully', 'status':1})


@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_outstanding(request, dsr_id):
    '''
    This method returns retailer transaction details like paid amount, outstanding, cheque number, etc
    given the retailer Id
    '''
    retailer_detail = DSRWorkAllocation.objects.filter(dsr = dsr_id)
    payment_list = []
    payment_dict = {}
    for retailer in retailer_detail:
        collection_data  =Collection.objects.filter(retailer = retailer.retailer)
        
        for collection in collection_data:
            payment_dict ={
                'invoice_id':collection.invoice_number,
                'retailer_id':collection.retailer_id,
                'invoice_created_date':collection.created_date,
                'invoice_amount':collection.invoice_amount,
            }
            payment_list.append(payment_dict)
            
    return Response(payment_list)


@api_view(['POST'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def uploadcollection(request):
    '''
    This method gets the collection of payment by dsr and puts it into the collection and collection
    details table
    '''
    collection_body = json.loads(request.POST['uploadcollection'])
    collection_body['invoice_id']
    collection = Collection()
    collection.invoice = Invoices.objects.get(id = collection_body['invoice_id'])
    collection.payment_date = collection_body['payment_date']
    collection.dsr = DistributorSalesRep.objects.get(distributor_sales_code = \
                                                      collection_body['dsr_id'])
    #retailer = Retailer.objects.get(retailer_code = collection_body['retailer_id'])
    # print retailer
    # collection.retailer = retailer
    collection.save()
    #put data into collection details table
    for mode in constants.PAYMENT_MODES:
        if mode[0][1] == collection_body['payment_mode']:
            payment_mode = mode[0][0]
        else:
            continue
    for cheque in collection_body['cheque_details']:
        collectiondetails = CollectionDetails()
        collectiondetails.collection = collection
        collectiondetails.collected_amount = collection_body['collected_amount']
        collectiondetails.cheque_bank = cheque['cheque_bank']
        collectiondetails.cheque_number = cheque['cheque_number']
        collectiondetails.cheque_amount = cheque['cheque_amount']
        collectiondetails.img_url = collection_body['upload']
        collectiondetails.save()
    
    return Response({'message': 'Retailer Collection is updated successfully', 'status':1})
   


@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_retailer_outstanding(request, retailer_id):
    '''
    This method returns the outstanding amount of particular retailer
    '''
    retailer = Retailer.objects.get(retailer_code = retailer_id)
    #for the particular retailer, get all the invoices and total the invoice amount
    invoices = Invoices.objects.filter(retailer__retailer_code = retailer_id)
    retailer_list = []
    if invoices:
        for invoice in invoices:
            retailer_dict = {}
            outstanding = 0
            collection = 0
            outstanding = outstanding + invoice.invoice_amount
            #retailer_dict.update({'retailer_id':retailer.retailer_code})
            retailer_dict.update({'distributor_id': retailer.distributor.distributor_id})
            retailer_dict.update({'invoice_id': invoice.invoice_id})
            retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
            amount = Collection.objects.filter(invoice = invoice)
            total = 0
            for each in amount:
                total = total + each.collected_amount
            
            retailer_dict.update({'collected_amount': total})
            #get the collections for that invoice
            collection_objs = Collection.objects.filter(invoice_id = invoice.id)
            for each in collection_objs:
                collection = collection + each.collected_amount
            retailer_dict.update({'outstanding':outstanding})
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


@api_view(['POST'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def uploadcollection(request):
    '''
    This method gets the collection of payment by dsr and puts it into the collection and collection
    details table
    '''
    collections_body = json.loads(request.POST['uploadcollection'])
    response_list = []
    for collection_body in collections_body:
        message_dict = {}
        # get the total order value of the invoice
        invoice = Invoices.objects.get(invoice_id = collection_body['invoice_id'])
        # get the so far collected_amount for that invoice
        coll = Collection.objects.filter(invoice = invoice)
        existing_collection = 0
        for each in coll:
            existing_collection = existing_collection + each.collected_amount
        # check the collectedamount from the payload is less than or equal to the existing
        # collection for that invoice
        if (collection_body['collected_amount']) <= \
            invoice.invoice_amount - decimal.Decimal(existing_collection):
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
            payment_mode = 1
            for mode in constants.PAYMENT_MODES:
                if mode[0][1] == collection_body['payment_mode']:
                    payment_mode = mode[0][0]
                else:
                    continue
            for cheque in collection_body['cheque_details']:
                collectiondetails = CollectionDetails()
                collectiondetails.collected_cash = collection_body['collected_cash']
                collectiondetails.collection = collection
                collectiondetails.mode = payment_mode
                collectiondetails.cheque_bank = cheque['cheque_bank']
                collectiondetails.cheque_number = cheque['cheque_number']
                collectiondetails.cheque_amount = cheque['cheque_amount']
                collectiondetails.img_url = cheque['cheque_image_url']
                collectiondetails.save()
            message_dict['invoice_id'] = collection_body['invoice_id']
            message_dict['status'] = '1'
            message_dict['message'] = 'Retailer Collection(s) is updated successfully'
        else:
            message_dict['invoice_id'] = collection_body['invoice_id']
            message_dict['status'] = '0'
            message_dict['message'] = 'Collection is greater than the invoice amount'
        response_list.append(message_dict)
    return Response(response_list)

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
        retailer.approved = constants.STATUS['WAITING_FOR_APPROVAL']
        retailer.save()
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
        try:
            mtd = str(total_achieved/ len(retailers)) + '%'
        except:
            mtd = 0
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
        order_dict['order_id'] = order.id
        order_dict['retailer_id'] = order.retailer.retailer_code
        order_dict['order_date'] = order.order_date.date()
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
                order_details_dict = OrderedDict()
                order_details_dict['part_id'] = each.part_number.part_number
                order_details_dict['part_name'] = each.part_number.description
                order_details_dict['quantity'] = each.quantity
                order_details_dict['mrp'] = each.part_number.mrp
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
        # check the status of the order and get it from the constants
        for k,v in constants.ORDER_STATUS.iteritems():
            if v == order.order_status:
                order_dict['status'] = k
        order_dict['distributor_id'] = order.distributor.distributor_id
        amount = 0
        order_detail = OrderPartDetails.objects.filter(order = order)
        
        if order_detail:
            for each in order_detail:
                amount = amount + each.line_total
            order_dict['amount'] = amount
            #order_dict['status'] = order.order_status
            # order details dict
            order_details_list = []
            for each in order_detail:
                order_details_dict = OrderedDict()
                order_details_dict['part_id'] = each.part_number.part_number
                order_details_dict['part_name'] = each.part_number.description
                order_details_dict['quantity'] = each.quantity
                order_details_dict['mrp'] = each.part_number.mrp
                order_details_dict['line_total'] = each.line_total
                order_details_list.append(order_details_dict)
            order_dict['order_details'] = order_details_list
        orders_list.append(order_dict)
    return Response(orders_list)

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def dsr_average_orders(request, dsr_id):
    '''
    This method returns the sale average of last 6 months as well as the previous month
    retailer wise
    '''
    dsr =  DistributorSalesRep.objects.select_related('distributor').get(distributor_sales_code = dsr_id)
    distributor = dsr.distributor
    retailers_list = []

    month_start_object = datetime.datetime.now().replace(day=1) # This is the object that holds the 1st of current month -> type:datetime used
    month_start_str = month_start_object.strftime("%Y-%m-%d") # this is the formatted object YYYY-MM-DD
    month_current = datetime.datetime.now().strftime("%Y-%m-%d")

    # get the retailer objects for this distributor
    retailers = Retailer.objects.filter(distributor = distributor)
    # get the current month date object with the first day
    date_str =  str(today.year) + '/' + str(today.strftime('%m')) + '/' + '01 00:00:00'
    #first_date = datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    first_date = today
    # get the date object of the past six months with the first day
    previous_date = first_date - timedelta(days = constants.AVERAGE_API_TIME_MONTHS * 30)
    previous_date_str = str(previous_date.year) + '/' + str(previous_date.strftime('%m')) + \
                                                    '/' + '01'
    previous_date = datetime.datetime.strptime(previous_date_str, '%Y/%m/%d')
    retailer_parts_list = []
    for retailer in retailers:
        previous_date = datetime.datetime.strptime(previous_date_str, '%Y/%m/%d')
        # get all the unique parts ordered for the retailer
        retailer_parts = OrderPartDetails.objects.filter(order__retailer = retailer,
                        created_date__gte = previous_date, created_date__lte = first_date).\
                                    values('part_number__part_number').distinct()
        if retailer_parts:
            total_sale = 0
            for part in retailer_parts:
                # set the previous date to the last 6 months
                previous_date = datetime.datetime.strptime(previous_date_str, '%Y/%m/%d')
                retailer_dict = OrderedDict()
                # get all the orders of the part number
                part_orders = OrderPartDetails.objects.filter(order__retailer = retailer,
                        created_date__gte = previous_date, created_date__lte = first_date,
                            part_number__part_number = part['part_number__part_number'])
                # for each order sum up the quantity and divide it by 6 
                for part_order in part_orders:
                    total_sale = total_sale + part_order.quantity
                average_sale = total_sale / constants.AVERAGE_API_TIME_MONTHS
                retailer_dict['retailer_id'] = retailer.retailer_code
                retailer_dict['part_number'] = part['part_number__part_number']

                orderpart_detail_count = OrderPartDetails.objects.filter(   order__retailer=retailer, \
                                                                            created_date__gte=month_start_str, \
                                                                            created_date__lte=month_current, \
                                                                            part_number__part_number=part['part_number__part_number'] ).count()
                retailer_dict['average_sale_last_six_months'] = \
                                                average_sale
                retailer_dict['mtd'] = orderpart_detail_count
                # calculate area average (retailer area ) for the previous month
                # set the previous date to the last month
                previous_date = previous_date = first_date - timedelta(days = 30)
                part_orders = OrderPartDetails.objects.filter(order__retailer = retailer,
                        created_date__gte = previous_date, created_date__lte = first_date,
                            part_number__part_number = part['part_number__part_number'])
                # for this part add the quantity of all the orders
                total_sale = 0
                for part_order in part_orders:
                    total_sale = total_sale + part_order.quantity
                retailer_dict['total_sale_last_month'] = total_sale
                retailer_parts_list.append(retailer_dict)
    if retailer_parts_list == []:
        return Response({'message':'There are no parts ordered for any of the retailer', \
                         'status': 0})
    else:
        return Response(retailer_parts_list)

    
@api_view(['POST'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def salesreturn(request, dsr_id):
    '''
    This method gets the orders placed by the dsr on behalf of the retailer and puts
    it in the database
    '''
    try:
        load = json.loads(request.body)
        dsr=DistributorSalesRep.objects.get(distributor_sales_code=dsr_id)
        if dsr:
            for order in load:
                try:
                    retailer=Retailer.objects.get(retailer_code=order['retailer_id'])
                    invoice=Invoices.objects.get(invoice_id=order['invoice_id'])

                    salesreturn_obj = SalesReturnHistory.objects.get(invoice_number__invoice_id=str(invoice.invoice_id) \
                                                                        and part_number==order['part_number'])
                    if salesreturn_obj:
                            salesreturn_obj.retailer=retailer
                            salesreturn_obj.dsr=dsr

                            salesreturn_obj.part_number=order['part_number']
                            salesreturn_obj.description=order['part_description']
                            salesreturn_obj.quantity=order['part_quantity']
                            salesreturn_obj.reason=order['reason']
                            salesreturn_obj.required_part=order['required_part']
                            salesreturn_obj.excess_part=order['excess_quantity']
                            salesreturn_obj.short_part=order['shortage_quantity']
                            salesreturn_obj.save()

                except:
                    salesreturn = SalesReturnHistory()
                    retailer=Retailer.objects.get(retailer_code=order['retailer_id'])
                    invoice=Invoices.objects.get(invoice_id=order['invoice_id'])
                    salesreturn.dsr = dsr
                    salesreturn.retailer = retailer

                    salesreturn.invoice_number=invoice
                    salesreturn.part_number = order['part_number']
                    salesreturn.description = order['part_description']
                    salesreturn.quantity = order['part_quantity']
                    salesreturn.reason = order['reason']
                    salesreturn.required_part = order['required_part']
                    salesreturn.short_part = order['excess_quantity']
                    salesreturn.excess_part = order['shortage_quantity']
                    salesreturn.save()

            return Response({'message': 'Sales return request made successfully', 'status':1})

    except Exception as ex:
        logger.error("Exception placing sales return request - {0}".format(ex))

    return Response({'message': 'Save failed, Incorrect Details', 'status':0})
