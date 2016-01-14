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

from gladminds.bajaj.models import DistributorSalesRep, Retailer,PartModels, Categories, \
                            PartPricing, Distributor,  Invoices, \
                            Collection,CollectionDetails,PartsStock,DSRWorkAllocation,DSRLocationDetails, \
			    NationalSparesManager,AreaSparesManager
from gladminds.bajaj.models import OrderPart,OrderPartDetails, \
                        PartIndexDetails, PartIndexPlates, FocusedPart
from gladminds.core.auth_helper import Roles


from gladminds.core import constants

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
    #get the disributor id
    try:
        distributor_obj = DistributorSalesRep.objects.get(distributor_sales_code=dsr_id).distributor
    except:
       return Response([{"error":"Distributor not present"}])
    #get the parts with the distributor
    stocks = PartsStock.objects.filter(distributor=distributor_obj)
    stock_list =[]
    for part in stocks:
        parts_dict = {}
	try:
            parts_dict["part_number"]=part.part_number.part_number
            parts_dict["part_available_quantity"]=part.available_quantity
            parts_dict["mrp"]=part.part_number.mrp
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
    parts = PartPricing.objects.filter(active = True)
    parts_list =[]
    for part in parts:
        available_quantity = PartsStock.objects.get(part_number_id = part.id ).available_quantity
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
        parts_dict.update({"part_products":part.products})
        parts_dict.update({"mrp":part.mrp})
        parts_list.append(parts_dict)
    return Response(parts_list)


@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_focused_parts(request):
    '''
    Returns all the focused parts along with locality
    '''
    retailer_code = request.GET.get('retailer_code')
    dsr_code = request.GET.get('dsr_code')
    if retailer_code:
	locality = Retailer.objects.get(retailer_code=retailer_code).locality
	all_focused_parts = FocusedPart.objects.filter(locality=locality)
    elif dsr_code:
	retailer_objs = Retailer.objects.filter(dsr__distributor_sales_code=dsr_code)
	localities = [i.locality for i in retailer_objs]
	all_focused_parts = FocusedPart.objects.filter(locality__in=localities)
    else:
    	all_focused_parts = FocusedPart.objects.all()

    all_focused_parts = FocusedPart.objects.all()
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
        parts_list.append(parts_dict)
    return Response(parts_list)	



@api_view(['GET'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
def get_parts_catalog(request):
    '''
    This method returns all the spare parts details based on the catalog
    '''
    parts = PartIndexDetails.objects.filter(plate__active = True)
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
@transaction.commit_manually
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
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
                try:
                    if item['part_type'] == 1:
                        '''Get the part details from Catalog Table'''
                        orderpart_details.part_number_catalog = PartIndexDetails.objects.\
                                                 get(part_number=item['part_number'], plate_id=item.get("plate_id"))
                    elif item['part_type'] == 2:
                        '''Get the part detailes from PartPricing Table'''
                        orderpart_details.part_number = PartPricing.objects.\
                                                 get(part_number=item['part_number'])
                except:
		    try:
			orderpart_details.part_number_catalog = PartIndexDetails.objects.\
                                                 get(part_number=item['part_number'])
		    except:
                        orderpart_details.part_number = PartPricing.objects.\
                                                 get(part_number=item['part_number'])

                    #return Response({'error': 'Part '+ item['part_number'] +' not found'})
                orderpart_details.quantity = item['qty']
                orderpart_details.order = orderpart
                orderpart_details.line_total = item['line_total']
                orderpart_details.save()
	    transaction.commit()
            send_msg_to_retailer_on_place_order(request,retailer.id,orderpart.order_number)
    return Response({'message': 'Order updated successfully', 'status':1})

@api_view(['POST'])
# @authentication_classes((JSONWebTokenAuthentication,))
# @permission_classes((IsAuthenticated,))
@transaction.commit_manually
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
            for item in order['order_items']:
                orderpart_details = OrderPartDetails()
		try:
                    if item['part_type'] == 1:
                        '''Get the part details from Catalog Table'''
                        orderpart_details.part_number_catalog = PartIndexDetails.objects.\
                                                 get(part_number = item['part_number'], plate_id=item.get('plate_id'))
                    elif item['part_type'] == 2:
                        '''Get the part detailes from PartPricing Table'''
                        orderpart_details.part_number = PartPricing.objects.\
                                                 get(part_number = item['part_number'])
                except:
                    #return Response({'error': 'Part '+ item['part_number'] +' not found'})
                    try:
                        orderpart_details.part_number_catalog = PartIndexDetails.objects.\
                                                 get(part_number=item['part_number'])
                    except:
                        orderpart_details.part_number = PartPricing.objects.\
                                                 get(part_number=item['part_number'])



                orderpart_details.quantity = item['qty']
                orderpart_details.order = orderpart
                orderpart_details.line_total = item['line_total']
                orderpart_details.save()
	    transaction.commit()
            send_msg_to_retailer_on_place_order(request,retailer.id,orderpart.order_number)
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
                    collection = collection + each.collected_amount
                retailer_dict.update({'collected_amount': collection})
                retailer_dict.update({'period': diff.days})
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
    #for the particular retailer, get all the invoices and total the invoice amount
    invoices = Invoices.objects.filter(retailer__retailer_code = retailer_id)
    retailer_list = []
    if invoices:
        for invoice in invoices:
            retailer_dict = {}
            outstanding = 0
            collection = 0
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
            collection.save()
            #put data into collection details table
            for cheque in collection_body['cheque_details']:
                collectiondetails = CollectionDetails()
                collectiondetails.collection = collection
                collectiondetails.mode = collection_body['payment_mode']
                collectiondetails.collected_amount = collection_body['collected_amount']
                collectiondetails.collected_cash = collection_body['collected_cash']
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
        retailer.approved = constants.STATUS['WAITING_FOR_APPROVAL']
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
            collection_details = CollectionDetails.objects.filter(collection = collection)
            for collection_detail in collection_details:
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
       	order_dict['distributor_id'] = order.distributor.distributor_id
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
                order_details_dict['part_id'] = each.part_number.part_number
                order_details_dict['part_name'] = each.part_number.description
                order_details_dict['quantity'] = each.quantity
                order_details_dict['mrp'] = each.part_number.mrp
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
from gladminds.sqs_tasks import send_loyalty_sms
def send_msg_to_retailer_on_adding(request,retailer_id,username,password):

    retailer_obj = Retailer.objects.get(id=retailer_id)
    print retailer_obj.mobile
    phone_number=utils.get_phone_number_format(retailer_obj.mobile)
    message=get_template('SEND_RETAILER_REGISTRATION').format(
                        retailer_name=retailer_obj.user.user.first_name,username=username,password=password)
    sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_loyalty_sms, {'phone_number': phone_number,
                    'message': message, "sms_client": settings.SMS_CLIENT})

def send_msg_to_retailer_on_place_order(request,retailer_id,order_id):
#     print retailer

    print request
    retailer_obj = Retailer.objects.get(id=retailer_id)
    print retailer_obj.mobile
    print order_id,"order"
    phone_number=utils.get_phone_number_format(retailer_obj.mobile)
    message=get_template('SEND_RETAILER_ON_ORDER_PLACEMENT').format(
                        retailer_name=retailer_obj.user.user.first_name,order_id=order_id)
    sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
    send_job_to_queue(send_loyalty_sms, {'phone_number': phone_number,
                    'message': message, "sms_client": settings.SMS_CLIENT})


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
                outstanding = outstanding + invoice.invoice_amount
                #get the collections for that invoice
                collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                for each in collection_objs:
                    collections = CollectionDetails.objects.filter(collection_id = each.id)
                    if collections:
                        for each_collections in collections:
                            collection = collection + each_collections.collected_amount
	    retailer_dict['outstanding'] = outstanding
	else:
	    retailer_dict['outstanding'] = 0
	if last_order_date:
	    retailer_dict['lastorderdate'] = last_order_date[0].order_date
	retailer_dict['contact'] = retailer.mobile
	dsr_work_allocation = DSRWorkAllocation.objects.filter(retailer=retailer).order_by('-date')
	##FIXME: Add for all days
	if dsr_work_allocation:
            retailer_dict['day'] = dsr_work_allocation[0].pjp_day
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
    date = request.GET.__getitem__('date')
    retailers = Retailer.objects.filter(dsr_id=dsr_id)#.count()
    response_dict = {}
    response_dict['date'] = date #FIXME: Confirm the field
    response_dict['users'] = []
    for retailer in retailers:
        last_order_date = OrderPart.objects.filter(retailer=retailer).order_by('-order_date')
	retailer_dict = {}
	retailer_dict['userid'] = retailer.id #FIXME: Could be retailer_id
        retailer_dict['firstname'] = retailer.user.user.first_name
        retailer_dict['lastname'] = retailer.user.user.last_name
	if retailer.latitude and retailer.longitude:
	    retailer_dict['latitude'] = str(retailer.latitude)
	    retailer_dict['longitude'] = str(retailer.longitude)
	else:
	    #Do not send the retailers if the retailer's gps-coordinates is not available
	    continue
	retailer_dict['data1'] = []
	###Get the retailer name 
        invoices = Invoices.objects.filter(retailer__retailer_code = retailer.id)
        if invoices:
            for invoice in invoices:
                retailer_dict = {}
                outstanding = 0
                collection = 0
                outstanding = outstanding + invoice.invoice_amount
                #get the collections for that invoice
                collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                for each in collection_objs:
                    collections = CollectionDetails.objects.filter(collection_id = each.id)
                    if collections:
                        for each_collections in collections:
                            collection = collection + each_collections.collected_amount
		collection_dict={}
		collection_dict['type1'] = "collection"
		collection_dict['amount'] = collection
		collection_dict['accepttime'] = ""
		retailer_dict['data1'].append(collection_dict)
	    retailer_dict['outstanding'] = outstanding
	else:
	    retailer_dict['outstanding'] = 0
	if last_order_date:
	    retailer_dict['lastorderdate'] = last_order_date[0].order_date
        retailer_dict['contact'] = retailer.mobile
        dsr_work_allocation = DSRWorkAllocation.objects.filter(retailer=retailer).order_by('-date')
	##FIXME: Add for all days
	if dsr_work_allocation:
	    retailer_dict['day'] = dsr_work_allocation[0].pjp_day
	else:
	    retailer_dict['day'] = 0
    	response_dict['retailers'].append(retailer_dict)
    return Response(response_dict)


@api_view(['GET'])
def get_users(request):
# FIXME: Return false other than all the known user roles
# FIXME: Move this method to a more generic location, may be auth_helper
    print request.user.groups.all()
    if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
	try:
	    distributor_id = Distributor.objects.get(user_id=request.user.id).distributor_id
	    return get_associated_dsrs(request, distributor_id)
	except:
	    return Response({'error':'Distributor object error'})
    if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
	asm_id = AreaSparesManager.objects.get(user_id=request.user.id).asm_id
        return get_associated_distributors(request, asm_id)
    if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
	nsm_id = NationalSparesManager.objects.get(user_id=request.user.id).nsm_id
    	return get_associated_asms(request,nsm_id)
    if request.user.groups.filter(name=Roles.SFAADMIN).exists():
        return get_associated_nsms(request)
    else:
	##FIXME: Added this to test with 
	return get_associated_nsms(request)
    return Response({'error':'error'}) 

