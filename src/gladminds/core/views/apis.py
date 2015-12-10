'''
author: araskumar.a
date: 31-08-2015
'''
import json, datetime, time, decimal
from datetime import timedelta
from collections import OrderedDict
from operator import itemgetter

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
            UserProfile
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
    parts = PartMasterCv.objects.filter(active = True)
    parts_list =[]
    for part in parts:
        parts_dict = {}
        parts_dict.update({"part_name":part.description})
        parts_dict.update({"part_number":part.part_number})
        parts_dict.update({"part_category":part.category.name})
        parts_dict.update({"part_available_quantity":part.available_quantity})
        parts_dict.update({"part_products":part.products})
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
    finaldate = datetime.datetime.strptime(date, '%Y-%m-%d')
    dsr = DistributorSalesRep.objects.get(distributor_sales_code = '500001')
    # schedules = DSRWorkAllocation.objects.filter(date__startswith = \
    #                 datetime.date(int(schedule_date[2]),int(schedule_date[1]), \
    #                               int(schedule_date[0])), dsr__distributor_sales_code=dsr_id)
    schedules = DSRWorkAllocation.objects.filter(date__year=finaldate.year,
                                                 date__month=finaldate.strftime("%m"),
                                                 date__day=finaldate.strftime("%e"))
    
    if schedules:                   
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
    else:
        return Response({'status':0, 'message':'There are no schedules for the given date'})


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
            orderpart.latitude = order['latitude']
            orderpart.longitude = order['longitude']
            orderpart.order_status = 0
            orderpart.save()
            #push all the items into the orderpart details
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                orderpart_details.part_number = PartMasterCv.objects.\
                                                get(part_number = item['part_number'])
                orderpart_details.quantity = int(item['qty'])
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
            orderpart.order_status = 0
            orderpart.save()
            #push all the items into the orderpart details
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                orderpart_details.part_number = PartMasterCv.objects.\
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
                total_amount = total_amount + invoice.invoice_amount
                retailer_dict.update({'retailer_id':retailer.retailer_code})
                retailer_dict.update({'invoice_id': invoice.invoice_id})
                retailer_dict.update({'total_amount': total_amount})
                retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
                #get the collections for that invoice
                collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                for each in collection_objs:
                    # collections = CollectionDetails.objects.filter(collection_id = each.id)
                    # if collections:
                    #     for each_collections in collections:
                    collection = collection + each.collected_amount
                retailer_dict.update({'collected_amount': collection})
                retailer_list.append(retailer_dict)
    return Response(retailer_list)

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
        user.password = constants.RETAILER_PASSWORD
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
    order_details = OrderPart.objects.filter(dsr__distributor_sales_code = dsr_id)
    
    orders_list = []
    for order in order_details:
        order_dict = OrderedDict()
        order_dict['order_id'] = order.id
        order_dict['retailer_id'] = order.retailer.retailer_code
        order_dict['order_date'] = order.order_date.date()
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
def get_retailer_orders(request, retailer_id):
    order_details = OrderPart.objects.filter(retailer__retailer_code = retailer_id)
    
    orders_list = []
    for order in order_details:
        order_dict = OrderedDict()
        order_dict['order_id'] = order.id
        order_dict['retailer_id'] = order.retailer.retailer_code
        order_dict['order_date'] = order.order_date.date()
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
   
    
    
    


    

    

