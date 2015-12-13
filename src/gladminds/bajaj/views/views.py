import logging
import json
import random
import datetime
import operator
import re
import requests
import csv
from gladminds.core.utils import check_password
from tastypie.http import HttpBadRequest
from collections import OrderedDict
from django.shortcuts import render_to_response, render
from django.http.response import HttpResponseRedirect, HttpResponse, \
    HttpResponseBadRequest, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from gladminds.settings import BRAND_META
from gladminds.bajaj import models
from gladminds.core import utils, constants
from gladminds.sqs_tasks import send_otp, send_customer_phone_number_update_message, \
    send_mail_for_feed_failure, send_mail_customer_phone_number_update_exceeds
from gladminds.core.managers.mail import sent_otp_email, \
    send_recovery_email_to_admin, send_mail_when_vin_does_not_exist
from gladminds.bajaj.services.coupons.import_feed import SAPFeed
from gladminds.core.apis.coupon_apis import CouponDataResource
from gladminds.core.managers.feed_log_remark import FeedLogWithRemark
from gladminds.core.cron_jobs.scheduler import SqsTaskQueue
from gladminds.core.constants import PROVIDER_MAPPING, PROVIDERS, GROUP_MAPPING, \
    USER_GROUPS, REDIRECT_USER, TEMPLATE_MAPPING, ACTIVE_MENU, MONTHS, STATUS
from gladminds.core.utils import get_email_template, format_product_object, \
    get_file_name
from gladminds.core.auth_helper import Roles
from gladminds.core.auth.service_handler import check_service_active, Services
from gladminds.core.core_utils.utils import log_time
from gladminds.core.cron_jobs.queue_utils import send_job_to_queue
from gladminds.core.services.message_template import get_template
from gladminds.core.managers.audit_manager import sms_log
from gladminds.bajaj.services.coupons import export_feed
from gladminds.core.auth import otp_handler
from gladminds.bajaj.models import Retailer, UserProfile, DistributorStaff, Distributor, District, State, OrderPartDetails, \
PartPricing, OrderDeliveredHistory, DoDetails, PartsStock, OrderPart, OrderPartDetails, DistributorSalesRep, DSRWorkAllocation, \
BackOrders, DSRLocationDetails, OrderTempDeliveredHistory, Collection, CollectionDetails, DoDetails


from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader
from django.template.context import Context
from gladminds.core.managers.mail import send_email

from django.contrib import messages

from django.db.models import Sum, Count, Max, Min
from django.core.urlresolvers import reverse

from gladminds.bajaj.admin import OrderPartAdmin
from django.http import HttpResponse
from gladminds.core.core_utils.date_utils import convert_utc_to_local_time
from gladminds.core.constants import DATE_FORMAT, TIME_FORMAT

logger = logging.getLogger('gladminds')
TEMP_ID_PREFIX = settings.TEMP_ID_PREFIX
TEMP_SA_ID_PREFIX = settings.TEMP_SA_ID_PREFIX
AUDIT_ACTION = 'SEND TO QUEUE'


def get_user_info(request):
    user_id = request.GET.get('user_id')
    user_obj = UserProfile.objects.get(user_id=user_id)
    data = {"first_name": user_obj.user.first_name , "last_name": user_obj.user.last_name , "email" : user_obj.user.email, "dob" : user_obj.date_of_birth, "pincode":user_obj.pincode}
    return HttpResponse(json.dumps(data), content_type="application/json")
    
def get_districts(request):
    state = request.GET.get('selected_state')
    state_obj = State.objects.get(state_code=state)
    districts = District.objects.filter(state=state_obj.id).values("name", "id")
    return HttpResponse(json.dumps(list(districts), cls=DjangoJSONEncoder), content_type="application/json")

 

   
def accept_cancel_order(request):
    order_id = request.POST["order_id"]
    part_numbers_ids = ""
    opts = OrderPart._meta
    order_display = []
    orders = {}
    if 'cancel' in request.POST:
        part_numbers = request.POST.getlist("part_number")
        
        for each in part_numbers:
            part_obj = PartPricing.objects.get(part_number=each)
            ord = OrderPartDetails.objects.filter(part_number_id=part_obj.id, order_id=order_id).update(part_status=1)
            messages.success(request, "Successfully cancelled the part " + each + " from the order ID " + order_id)
    elif "place_order" in request.POST:
        part_numbers = request.POST.getlist("part_number")
        for each in part_numbers:
            part_obj = PartPricing.objects.get(part_number=each)
            ord = OrderPartDetails.objects.filter(part_number_id=part_obj.id, order_id=order_id).update(part_status=0)
            messages.success(request, "Successfully accepted the part " + each + " from the order ID " + order_id)
    order_status = "open"
    orders_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id)
    order_display = []
    orders = {}
    ordered_date = OrderPart.objects.get(id=order_id).order_date
    for each_order in orders_obj:
        orders['mrp'] = each_order.part_number.mrp
        orders['part_number'] = each_order.part_number.part_number
        orders['part_description'] = each_order.part_number.description
        orders['quantity'] = each_order.quantity
        orders['order_id'] = each_order.order_id
        orders['line_total'] = float(each_order.part_number.mrp) * float(each_order.quantity)
        orders["part_status"] = each_order.part_status
        available_quantity = PartsStock.objects.filter(part_number=each_order.part_number.id)
        if available_quantity:
            
              if available_quantity < each_order.quantity:
               dist_id = Distributor.objects.get(user=request.user.id).id
               orders['available_quantity'] = available_quantity[0].available_quantity
               remaining_qty = orders['available_quantity'] - orders["quantity"]
               if remaining_qty > 0:
                   backorder_obj = BackOrders(distributor_id=dist_id , qty=remaining_qty, datetime=datetime.datetime.now())
                   backorder_obj.save(using=settings.BRAND)
              else:
                  orders['available_quantity'] = available_quantity[0].available_quantity
        else:
            orders['available_quantity'] = None
        order_delivered_obj = OrderDeliveredHistory.objects.filter(part_number_id=each_order.part_number_id, order_id=each_order.order_id).aggregate(Sum('delivered_quantity'))                  
        if order_delivered_obj["delivered_quantity__sum"] != None:
            if each_order.quantity == int(order_delivered_obj["delivered_quantity__sum"]):
                 order_status = "shipped"
            else:
                order_status = "pending"  
            orders["delivered_quantity"] = order_delivered_obj["delivered_quantity__sum"]
            orders['pending'] = (each_order.quantity) - int(order_delivered_obj["delivered_quantity__sum"])
        else:
         
            orders["delivered_quantity"] = 0
            orders['pending'] = each_order.quantity
            order_status = "open"
        order_display.append(orders.copy())
    context = { 
                "order_display":order_display,
                "order_id":order_id,
                'order_id':order_id,
                'delivered':0,
                'order_status':order_status,
                "ordered_date":ordered_date,
                'app_label':opts.app_label,
                'opts':opts,
               }
    template = 'admin/bajaj/orderpart/show_parts.html'  # = Your new template
    return render(request, template, context)
    
    
def clear_order_temp(request):
    ret_id = request.POST.get("retailer_id") 
    order_obj = OrderTempDeliveredHistory.objects.filter(retailer_id=ret_id).delete()
    data = {"status":1, "message":"success"}
    return HttpResponse(json.dumps(data), content_type="application/json")
        

def get_orders(request, ret_id, invoice_id):
    print invoice_id
    print ret_id, "rettt"

  
    

    
def save_order_history(request):
    order_id = request.POST["order_id"]
    retailer_id = request.POST["retailer_id"]
    
    part_numbers_ids = ""
    opts = OrderPart._meta
    order_display = []
    orders = {}
    stock = request.POST.getlist("delivered_stock")
    part_number_ids = ""
    total_amount = 0    
    do_obj = DoDetails(order_id=order_id)
    do_obj.save(using=settings.BRAND)
    flag = 0
    for each in range(0, int(len(stock))):
        delivered_stock = request.POST.getlist("delivered_stock")[each]
        date = request.POST.getlist("delivered_date")[each]
        part_number = request.POST.getlist("part_number")[each]
        delivered_qty = request.POST.getlist("delivered_quantity")[each]
        if delivered_stock != "":
            part_pricing_obj = PartPricing.objects.get(part_number=part_number)
            part_obj = PartsStock.objects.get(part_number=part_pricing_obj.id)
            total_delivered_stock = int(delivered_qty) + int(delivered_stock)
            if int(delivered_stock) > int(part_obj.available_quantity) or (total_delivered_stock > int(request.POST.get("ordered_quantity"))):
                flag = 1
                
                messages.error(request, "Kindly check the stock and enter again fot the part " + part_number)
            else: 
                part_obj.available_quantity = int(part_obj.available_quantity) - int(delivered_stock)
                part_obj.save(using=settings.BRAND)
                ordered_date = datetime.datetime.strptime(date, "%m/%d/%Y") 

                order_obj = OrderDeliveredHistory(delivered_date=ordered_date, delivered_quantity=delivered_stock, order_id=order_id, part_number_id=part_pricing_obj.id, do_id=do_obj.id)
                order_obj.save(using=settings.BRAND)
                ret_id = OrderPart.objects.get(id=order_id).retailer 
                part_numbers_ids += part_number + " "
    if part_numbers_ids:
        messages.success(request, "Successfully placed the order " + order_id + " for the part number " + part_numbers_ids)
    if request.POST["order_status"] == "open":
        orders_obj = OrderPart.objects.filter(retailer_id=retailer_id, order_status=0)
    elif request.POST["order_status"] == "pending":
        orders_obj = OrderPart.objects.filter(retailer_id=retailer_id, order_status=1)
        

    order_display = []
    orders = {}
    ordered_date = OrderPart.objects.get(id=order_id).order_date
    for each in orders_obj:
        orderparts_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order_id=each.id, part_status=0)
        for each_order in orderparts_obj:
        
            orders['mrp'] = each_order.part_number.mrp
            orders['part_number'] = each_order.part_number.part_number
            orders['part_description'] = each_order.part_number.description
            orders['quantity'] = each_order.quantity
            orders['order_id'] = each.id
            orders['line_total'] = float(each_order.part_number.mrp) * float(each_order.quantity)
            orders["part_status"] = each_order.part_status
            
            available_quantity = PartsStock.objects.filter(part_number=each_order.part_number.id)
            print available_quantity, "avaiii"
            if available_quantity:
                
                  if available_quantity < each_order.quantity:
                   dist_id = Distributor.objects.get(user=request.user.id).id
                   orders['available_quantity'] = available_quantity[0].available_quantity
                   remaining_qty = orders['available_quantity'] - orders["quantity"]
                   if remaining_qty > 0:
                       backorder_obj = BackOrders(distributor_id=dist_id , qty=remaining_qty, datetime=datetime.datetime.now())
                       backorder_obj.save(using=settings.BRAND)
                  else:
                      orders['available_quantity'] = available_quantity[0].available_quantity
            else:
                orders['available_quantity'] = None
            
            order_delivered_obj = OrderDeliveredHistory.objects.filter(part_number_id=each_order.part_number_id, order_id=each_order.order_id).aggregate(Sum('delivered_quantity'))                  

            if order_delivered_obj["delivered_quantity__sum"] != None:
                if each_order.quantity == int(order_delivered_obj["delivered_quantity__sum"]):
                     order_status = "shipped"
                else:
                    order_status = "pending"  
                orders["delivered_quantity"] = order_delivered_obj["delivered_quantity__sum"]
                orders['pending'] = (each_order.quantity) - int(order_delivered_obj["delivered_quantity__sum"])
            else:
                orders["delivered_quantity"] = each_order.quantity
                orders['pending'] = each_order.quantity
                order_status = "open"
            order_display.append(orders.copy())
    context = { 
                "data":order_display,
                "order_id":order_id,
                'order_id':order_id,
#                 'delivered':0,
                'order_status':order_status,
                "ordered_date":ordered_date,
                'app_label':opts.app_label,
                'opts':opts,
               }
    template = 'admin/bajaj/orderpart/retailer_order_list.html'  # = Your new template
    return render(request, template, context)

  
def save_order_temp_history(request):
    ret_id = request.POST.get("retailer_id")
    stock = request.POST.getlist("delivered_stock")
    part_number_ids = ""
    total_amount = 0    
    flag = 0

    for each in range(0, int(len(stock))):
         order_id = request.POST.getlist("order_id")[each]
         delivered_stock = request.POST.getlist("delivered_stock")[each]
         date = request.POST.getlist("delivered_date")[each]
         part_number = request.POST.getlist("part_number")[each]
         delivered_qty = request.POST.getlist("delivered_quantity")[each]
         if delivered_stock != "":
         
         
             part_pricing_obj = PartPricing.objects.get(part_number=part_number)
             part_obj = PartsStock.objects.get(part_number=part_pricing_obj.id)
             total_delivered_stock = int(delivered_qty) + int(delivered_stock)
             if int(delivered_stock) > int(part_obj.available_quantity) or (total_delivered_stock > int(request.POST.get("ordered_quantity"))):
                 flag = 1           
                 messages.error(request, "Kindly check the stock and enter again fot the part " + part_number)
             else: 
                 part_obj.available_quantity = int(part_obj.available_quantity)
                 ordered_date = datetime.datetime.strptime(date, "%m/%d/%Y") 
                 
                 order_obj = OrderTempDeliveredHistory(delivered_date=ordered_date, delivered_quantity=delivered_stock, order_id=order_id, part_number_id=part_pricing_obj.id, retailer_id=ret_id)
                 order_obj.save(using=settings.BRAND)
             
     # query and send data  as response to invoice template(modal)
    
     
    invoice_details_obj = OrderTempDeliveredHistory.objects.filter().select_related("part_number", "order")
    invoice_details = []
    invoice_details_dict = {}
    for each_invoice in invoice_details_obj:
         invoice_details_dict["part_number"] = each_invoice.part_number.part_number
         invoice_details_dict["part_description"] = each_invoice.part_number.description
         invoice_details_dict["mrp"] = each_invoice.part_number.mrp
         invoice_details_dict["qty"] = each_invoice.delivered_quantity
         invoice_details_dict["rate"] = float(invoice_details_dict["mrp"]) * float(invoice_details_dict["qty"])
         invoice_details_dict["disc"] = 0
         invoice_details_dict["tax"] = 0
         invoice_details_dict["amount"] = (invoice_details_dict["rate"] - invoice_details_dict["disc"]) + invoice_details_dict["tax"]
         invoice_details.append(invoice_details_dict.copy())
    return HttpResponse(json.dumps(invoice_details), content_type="application/json") 

        
        
    
    

  
            
#             get_parts(request)
#             order_obj = OrderPart.objects.filter(retailer=ret_id,order_status=3).select_related("retailer","dsr")
#             print order_obj
#             order_status="shipped"
#             retailer_name = order_obj[0].retailer.retailer_name
#     for each_order in order_obj:
#         orders["retailer_name"] = each_order.retailer.retailer_name
#         orders["dsr_name"] = each_order.dsr.user.user.first_name
#         orders["order_date"] = each_order.order_date
#         orderdetails_obj = OrderPartDetails.objects.filter(order_id=each_order.id).aggregate(Sum('line_total'))
# #         part_status = OrderPartDetails.objects.get(order_id=each_order.id,part_number_id).part_status
#         orders["total_value"] = orderdetails_obj["line_total__sum"]
#         orders["order_id"] = each_order.id
#         orders["ret_id"] = each_order.retailer_id
# #         orders["part_status"] = 
#         
#         order_display.append(orders.copy())  
#     print order_display
#     context={"order_display":order_display,"order_status":order_status,'app_label':opts.app_label,'opts':opts,"retailer_name":retailer_name}
#     form_url=""
#     template = 'admin/bajaj/orderpart/change_form.html'
#     
#     return render(request,template,context)
            
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
     
def dsr_orders(request):    
    return HttpResponseRedirect('/admin/bajaj/orderpart/' + "?orders=dsr")


def ordered_part_details(request, part_number, order_id):
    part_obj = PartPricing.objects.get(part_number=part_number)
    ordered_part_details = OrderDeliveredHistory.objects.filter(part_number=part_obj.id, order_id=order_id).values("do_id", "order_id", "delivered_quantity", "part_number_id", "delivered_date")
    context = {"data":ordered_part_details}
    template = 'admin/bajaj/ordered_part_details.html'
    return render(request, template, {"data":ordered_part_details, "part_number":part_number, "part_description":part_obj.description})


def order_details(request, order_status, retailer_id):
    opts = OrderPart._meta
    order_display = []
    orders = {}
    if order_status == "open":
        order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=0).select_related("retailer", "dsr")
#     elif order_status == "pending":
#         order_obj = OrderPart.objects.filter(retailer=retailer_id,order_status=1).select_related("retailer","dsr")
    
    elif order_status == "cancelled":
        order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=2).select_related("retailer", "dsr")    
    if len(order_obj) > 0:
        retailer_name = order_obj[0].retailer.retailer_name   
        for each_order in order_obj:
            orders["retailer_name"] = each_order.retailer.retailer_name
            orders["dsr_name"] = each_order.dsr
            orders["order_date"] = each_order.order_date
            orderdetails_obj = OrderPartDetails.objects.filter(order_id=each_order.id).aggregate(Sum('line_total'))
            orders["total_value"] = orderdetails_obj["line_total__sum"]
            orders["order_id"] = each_order.id
            orders["ret_id"] = each_order.retailer_id
            order_display.append(orders.copy())  
    context = {
             "order_display":order_display,
             'order_status':order_status,
             'app_label':opts.app_label,
             'opts':opts,
             "retailer_name":retailer_name,
             "retailer_id":retailer_id
             }
    form_url = ""
    template = 'admin/bajaj/orderpart/change_form.html'
    return render(request, template, context)


def shipped_order_details(request, order_status, retailer_id):
    opts = OrderPart._meta
    shipped_details = []
    orders = {}
    order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=3).select_related("retailer", "dsr")
    if len(order_obj) > 0:
        
        retailer_name = order_obj[0].retailer.retailer_name   
        for each_order in order_obj:
            orders["order_id"] = each_order.id            
            do_obj = DoDetails.objects.filter(order_id=orders["order_id"]).select_related("invoice")
            for each in do_obj:
                orders["invoice_amt"] = each.invoice.invoice_amount
                orders["invoice_no"] = each.invoice.id
                orderpart_details = OrderDeliveredHistory.objects.filter(order_id=each_order.id, do_id=each.id)
                for each_orderpart in orderpart_details:
                    orders["shipped_date"] = each_orderpart.delivered_date

            shipped_details.append(orders.copy())  
    context = {
             "shipped_details":shipped_details,
             'order_status':order_status,
             'app_label':opts.app_label,
             'opts':opts,
             "retailer_name":retailer_name,
             "retailer_id":retailer_id
             }
    form_url = ""
    template = 'admin/bajaj/orderpart/shipped_details.html'
    return render(request, template, context)
    


def get_parts(request, order_id, order_status, retailer_id):
        opts = OrderPart._meta
        if order_status == "open":
            orders_obj = OrderPart.objects.filter(retailer_id=retailer_id, id=order_id, order_status=0)
#             orders_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id)
        elif order_status == "pending":
            
  
            orders_obj = OrderPart.objects.filter(retailer_id=retailer_id, id=order_id, order_status=1)
        elif order_status == "shipped":
             orders_obj = OrderPart.objects.filter(retailer_id=retailer_id, id=order_id, order_status=3)
              
#             orders_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id,part_status=0,retailer = ret_id)
        elif order_status == "cancelled":
            orders_obj = OrderPart.objects.filter(retailer_id=retailer_id, id=order_id, order_status=2)
#             orders_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id,part_status=1,retailer = ret_id)    
            
        order_display = []
        orders = {}
        ordered_date = OrderPart.objects.get(id=order_id).order_date
        for each in orders_obj:
            orderparts_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order_id=each.id)

            for each_order in orderparts_obj:
                orders['mrp'] = each_order.part_number.mrp
                orders['part_number'] = each_order.part_number.part_number
                orders['part_description'] = each_order.part_number.description
                orders['quantity'] = each_order.quantity
                orders['order_id'] = each_order.order_id
                orders['line_total'] = float(each_order.part_number.mrp) * float(each_order.quantity)
                orders["part_status"] = each_order.part_status
                
                available_quantity = PartsStock.objects.filter(part_number=each_order.part_number.id)
                if available_quantity:
                    available_quantity[0].available_quantity
                    orders['available_quantity'] = available_quantity[0].available_quantity
                else:
                    orders['available_quantity'] = None
                order_delivered_obj = OrderDeliveredHistory.objects.filter(part_number_id=each_order.part_number_id, order_id=each_order.order_id).aggregate(Sum('delivered_quantity'))         
#                 date = OrderDeliveredHistory.objects.get(part_number_id=each_order.part_number_id, order_id=each_order.order_id).delivered_date
#                 orders["shipped_date"] = date
#                 print date,"dateeee"
                if order_delivered_obj["delivered_quantity__sum"] != None:
                    orders["delivered_quantity"] = int(order_delivered_obj["delivered_quantity__sum"])
                    orders['pending'] = (each_order.quantity) - int(order_delivered_obj["delivered_quantity__sum"])
                else:
                    orders["delivered_quantity"] = 0
                    orders['pending'] = each_order.quantity
                order_display.append(orders.copy())
        context = { 
                "order_display":order_display,
                "order_id":order_id,
                'order_status':order_status,
                "ordered_date":ordered_date,
                'app_label':opts.app_label,
                'opts':opts,
                "retailer_id":retailer_id     
               }
        template = 'admin/bajaj/orderpart/show_parts.html'  
        return render(request, template, context)

    
    
        
def accept_order(request, order_id, action):
    opts = OrderPart._meta
    if action == "accept":
        order_obj = OrderPart.objects.filter(id=order_id).update(order_status=1)   
        order_status = "open"
        order_obj = OrderPart.objects.filter(order_status=0).select_related("retailer", "dsr")
        messages.success(request, "Successfully accepted Order No "+order_id)
    else:
        order_obj = OrderPart.objects.filter(id=order_id).update(order_status=2) 
        order_status = "cancelled"
        order_obj = OrderPart.objects.filter(order_status=2).select_related("retailer", "dsr")
        messages.success(request, "Successfully cancelled Order No "+order_id)
    order_display = []
    orders = {}
#     order_obj = OrderPart.objects.filter(id=order_id,order_status=0).select_related("retailer","dsr")
    if len(order_obj) > 0:
        retailer_name = order_obj[0].retailer.retailer_name
        retailer_id = order_obj[0].retailer.id
    
        for each_order in order_obj:
            orders["retailer_name"] = each_order.retailer.retailer_name
            orders["dsr_name"] = each_order.dsr
            orders["order_date"] = each_order.order_date
            orderdetails_obj = OrderPartDetails.objects.filter(order_id=each_order.id).aggregate(Sum('line_total'))
            orders["total_value"] = orderdetails_obj["line_total__sum"]
            orders["order_id"] = each_order.id
            orders["ret_id"] = each_order.retailer_id
            order_display.append(orders.copy())  
        context = {
                 "order_display":order_display,
                 "order_status":order_status,
                 'app_label':opts.app_label,
                 'opts':opts,
                 "retailer_name":retailer_name,
                 "retailer_id":retailer_id
                 }
    else:
        messages.success(request, "No open orders")
        context = { "order_status":order_status,
                 'app_label':opts.app_label,
                 'opts':opts}
    form_url = ""
    template = 'admin/bajaj/orderpart/change_form.html'
    return render(request, template, context)
    
def schedule_dsr(request):
    retailer_ids = request.POST.getlist("retailer[]")
    dsr_id = request.POST["dsr"]
    dist_id = Distributor.objects.get(user=request.user.id).id
    scheduled_time = request.POST["dateTime"]
    import pytz
    scheduled_time = datetime.datetime.strptime(scheduled_time, "%d/%m/%Y")

    now_aware = scheduled_time.replace(tzinfo=pytz.UTC)
    date_time = convert_utc_to_local_time(now_aware).strftime(TIME_FORMAT)   
    for each in retailer_ids:
        schedule_obj = DSRWorkAllocation(distributor_id=dist_id, dsr_id=dsr_id, retailer_id=each, date=date_time)
        schedule_obj.save()
    dsr_work_obj = DSRWorkAllocation.objects.filter(distributor_id=dist_id).select_related("dsr", "retailer")
    events_list = []
    for each in dsr_work_obj:
        events_dict = {}
        events_dict["location"] = each.retailer.address_line_3
        events_dict["retailer_name"] = each.retailer.retailer_name
        events_dict["firstname"] = each.retailer.user.user.first_name
        scheduled_time = datetime.datetime.strftime(each.date.date(), "%Y-%m-%d") 
        events_dict["start"] = scheduled_time
        events_dict["dsr_name"] = each.dsr.user.user.first_name
        events_dict["dsr_code"] = each.dsr.distributor_sales_code
        events_list.append(events_dict.copy())
    data = {'status': 0, 'message': "scheduled successfully", "events_list":events_list}
    return HttpResponse(json.dumps(data), content_type="application/json")




def cal_data(request):
    order_display = []
    dist = {}
    ret = {}
    ret_list = []
    import json
    data = []
    dist_list = []    
    dist_id = Distributor.objects.get(user=request.user.id).id
    dist_obj = DistributorSalesRep.objects.filter(distributor_id=dist_id).select_related("user")
    for each in dist_obj:
        dist["dist_id"] = each.id
        dist["dist_code"] = each.distributor_sales_code
        dist["firstname"] = each.user.user.first_name
        dist_list.append(dist.copy())
    data.append(dist_list)
    ret_obj = Retailer.objects.filter(distributor_id=dist_id).select_related("user")    
    for each in ret_obj:
        ret["ret_id"] = each.id
        ret["ret_code"] = each.retailer_code
        ret["firstname"] = each.user.user.first_name
        ret["location"] = each.address_line_3
        ret_list.append(ret.copy())
    data.append(ret_list) 
    dsr_work_obj = DSRWorkAllocation.objects.filter(distributor_id=dist_id).select_related("dsr", "retailer")
    events_list = []
    for each in dsr_work_obj:
        events_dict = {}
        events_dict["location"] = each.retailer.address_line_3
        events_dict["retailer_name"] = each.retailer.retailer_name
        events_dict["firstname"] = each.retailer.user.user.first_name
        scheduled_time = datetime.datetime.strftime(each.date.date(), "%Y-%m-%d") 
        events_dict["start"] = scheduled_time
        events_dict["dsr_name"] = each.dsr.user.user.first_name
        events_dict["dsr_code"] = each.dsr.distributor_sales_code
        events_list.append(events_dict.copy())
    data.append(events_list)
    return HttpResponse(json.dumps(data), content_type="application/json")



def get_collection_details(request, ret_id):
    collection_details = []
    collection_details_dict = {}
    collection_obj = Collection.objects.filter(retailer_id=ret_id)
    for each in collection_obj:
        collection_details_dict["payment_date"] = each.payment_date
        collection_details_dict["collected_by"] = each.dsr.user.user.first_name
#         json.dump(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        
        collection_details_dict["payment_date"] = datetime.datetime.strftime(each.payment_date, '%Y-%m-%dT%H:%M:%S') 
        more_details_obj = CollectionDetails.objects.filter(collection_id=each.id)
        for each_obj in more_details_obj:          
            collection_details_dict["collected_amount"] = each_obj.collected_amount
            if each_obj.mode == 1:
            
                collection_details_dict["mode"] = "cash"
            elif each_obj.mode == "2":
                collection_details_dict["mode"] = "cheque"
            collection_details_dict["cheque_number"] = each_obj.cheque_number
            collection_details_dict["cheque_bank"] = each_obj.cheque_bank
            print collection_details_dict, "dicttt"
            collection_details.append(collection_details_dict.copy())
    return HttpResponse(json.dumps(collection_details), content_type="application/json")
            
       
        

def test(request):
    opts = DSRLocationDetails._meta
    dsr_location_objs = OrderPart.objects.filter().select_related("dsr")
    ret_lat_long = Retailer.objects.aggregate(ret_lat=Max('latitude'), ret_long=Max('longitude'))
    dsr_lat_long = OrderPart.objects.aggregate(dsr_lat=Max('latitude'), dsr_long=Max('longitude'))
    max_long = []
    max_lat = []
    max_long.append(ret_lat_long["ret_long"])
    max_lat.append(ret_lat_long["ret_lat"])
    max_long.append(dsr_lat_long["dsr_long"])
    max_lat.append(dsr_lat_long["dsr_lat"])    
    maximum_lat = max(max_lat)
    minimum_long = min(max_long)
    lat_long = {}
    lat_long["max_lat"] = maximum_lat
    lat_long["min_long"] = minimum_long
    all_locations = []
    all_locations.append(lat_long.copy())
    ret_locations = []
    ret_location_dict = {}
    ret_obj = Retailer.objects.filter().select_related("user")
    for each in ret_obj:
        ret_location_dict["latitude"] = each.latitude
        ret_location_dict["longitude"] = each.longitude
        ret_location_dict["ret_code"] = each.retailer_code
        ret_location_dict["ret_name"] = each.retailer_name
        ret_locations.append(ret_location_dict.copy())
    all_locations.append(ret_locations)    
    dsr_locations = []
    dsr_location_dict = {}
    for each in dsr_location_objs:
        print each.dsr
        dsr_location_dict["latitude"] = each.latitude
        dsr_location_dict["longitude"] = each.longitude
#         dsr_location_dict["last_sync"] = each.last_sync
        dsr_location_dict["dsr_id"] = each.dsr_id
        dsr_location_dict["dsr_name"] = each.dsr.user.user.first_name
        dsr_locations.append(dsr_location_dict.copy())
    all_locations.append(dsr_locations) 
    data = json.dumps(all_locations, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type="application/json")



import csv
def upload_part_pricing(request):
    '''
    This method uploads stock availability in partpricing table
    '''
    # upload the file to the upload_bajaj folder 
    dist_id = Distributor.objects.get(user__user=request.user)
    part_pricing_list = []
    msg = ""
    flag = 0
    full_path = handle_uploaded_file(request.FILES['upload_part_pricing'])
    with open(full_path) as csvfile:
        partreader = csv.DictReader(csvfile)
        for row_list in partreader:
            part_pricing_list.append(row_list)            
        for part in part_pricing_list:
            try:
                part_pricing_object = PartPricing.objects.get(part_number=part['Part Number'])
                try:
                    part_stock_object = PartsStock.objects.filter(part_number_id=part_pricing_object.id, distributor_id=dist_id).update(available_quantity=part['Available Quantity'])
#                     part_stock_object.available_quantity = part['Available Quantity']
#                     part_stock_object.save(using=settings.BRAND)
                except Exception as ex:
                    part_stock_obj = PartsStock(part_number=part_pricing_object, available_quantity=part['Available Quantity'] , distributor=dist_id)
                    part_stock_obj.save(using=settings.BRAND)
                
            except Exception as ex:
                flag = 1
                msg = msg + part['Part Number'] + ","
        if flag == 1:
            messages.error(request, 'Part Number {0} does not exist'.format(msg))
        else:
            messages.success(request, "Stock updated successfully")
            
        return HttpResponseRedirect('/admin/bajaj/partpricing/')

 
def handle_uploaded_file(uploaded_file):
    '''
    This method gets the uploaded file and writes it in the upload dir under the same name
   '''
    path = settings.UPLOAD_DIR + uploaded_file.name
    with open(path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return path


@login_required
def approve_retailer(request, retailer_id):
    '''
    This method approves the retailer by the ASM/admin
    '''
      
    retailer = Retailer.objects.filter(id=retailer_id).update(approved=STATUS['APPROVED'])
    return HttpResponseRedirect('/admin/bajaj/retailer/')

@check_service_active(Services.FREE_SERVICE_COUPON)
def auth_login(request, provider):
    if request.method == 'GET':
            if provider not in PROVIDERS:
                return HttpResponseBadRequest()
            return render(request, PROVIDER_MAPPING.get(provider, 'asc/login.html'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                
                login(request, user)
                return HttpResponseRedirect('/aftersell/provider/redirect')
    return HttpResponseRedirect(request.path_info + '?auth_error=true')


@check_service_active(Services.FREE_SERVICE_COUPON)
def redirect_user(request):
    user_groups = utils.get_user_groups(request.user)
    for group in USER_GROUPS:
        if group in user_groups:
            return HttpResponseRedirect(REDIRECT_USER.get(group))
#     data = {'message': 'Invalid Credentials'}
#     return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponseBadRequest('Not Allowed')

@check_service_active(Services.FREE_SERVICE_COUPON)
def user_logout(request):
    if request.method == 'GET':
        # TODO: Implement brand restrictions.
        user_groups = utils.get_user_groups(request.user)
        for group in USER_GROUPS:
            if group in user_groups:
                logout(request)
                return HttpResponseRedirect(GROUP_MAPPING.get(group))

        return HttpResponseBadRequest()
    return HttpResponseBadRequest('Not Allowed')

@check_service_active(Services.FREE_SERVICE_COUPON)
@login_required()
def change_password(request):
    if request.method == 'GET':
        return render(request, 'portal/change_password.html')
    if request.method == 'POST':
        groups = utils.stringify_groups(request.user)
        if Roles.DEALERS in groups or Roles.ASCS in groups:
            user = User.objects.get(username=request.user)
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
            check_pass = user.check_password(str(old_password))
            if check_pass:
                invalid_password = check_password(new_password)
                if (invalid_password):
                    data = {'message':"password does not match the rules", 'status':False}
                else:    
                    user.set_password(str(new_password))
                    user.save()
                    data = {'message': 'Password Changed successfully', 'status': True}
            else:
                data = {'message': 'Old password wrong', 'status': False}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            return HttpResponseBadRequest('Not Allowed')


@check_service_active(Services.FREE_SERVICE_COUPON)
def generate_otp(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            user = User.objects.get(username=username)
            phone_number = ''
            user_profile_obj = models.UserProfile.objects.filter(user=user)
            if user_profile_obj:
                phone_number = user_profile_obj[0].phone_number
                logger.info('OTP request received . username: {0}'.format(username))
                token = otp_handler.get_otp(user=user)
                message = get_template('SEND_OTP').format(token)
                send_job_to_queue(send_otp, {'phone_number': phone_number, 'message': message,
                                         'sms_client': settings.SMS_CLIENT})
                logger.info('OTP sent to mobile {0}'.format(phone_number))
#             #Send email if email address exist
            if user.email:
                sent_otp_email(data=token, receiver=user.email, subject='Forgot Password')
        
            return HttpResponseRedirect('/aftersell/users/otp/validate?username=' + username)
        
        except Exception as ex:
            logger.error('Invalid details, mobile {0}'.format(ex))
            return HttpResponseRedirect('/aftersell/users/otp/generate?details=invalid')    
    
    elif request.method == 'GET':
        return render(request, 'portal/get_otp.html')

@check_service_active(Services.FREE_SERVICE_COUPON)
def validate_otp(request):
    if request.method == 'GET':
        return render(request, 'portal/validate_otp.html')
    elif request.method == 'POST':
        try:
            otp = request.POST['otp']
            username = request.POST['username']
            logger.info('OTP {0} recieved for validation. username {1}'.format(otp, username))
            user = User.objects.get(username=username)
            user_profile = models.UserProfile.objects.get(user=user)
            otp_handler.validate_otp(otp, user=user_profile)
            logger.info('OTP validated for name {0}'.format(username))
            return render(request, 'portal/reset_pass.html', {'otp': otp})
        except Exception as ex:
            logger.error('OTP validation failed for name {0} : {1}'.format(username, ex))
            return HttpResponseRedirect('/aftersell/users/otp/generate?token=invalid')


@check_service_active(Services.FREE_SERVICE_COUPON)
def update_pass(request):
    try:
        otp = request.POST['otp']
        password = request.POST['password']
        data = utils.update_pass(otp, password)
        return HttpResponse(json.dumps(data), content_type='application/json')

    except:
        logger.error('Password update failed.')
        return HttpResponseRedirect('/aftersell/asc/login?error=true')


@check_service_active(Services.FREE_SERVICE_COUPON)
@login_required()
def register(request, menu):
    groups = utils.stringify_groups(request.user)
    use_cdms = True
    if len(set([Roles.ASCS, Roles.DEALERS, Roles.SDMANAGERS]).intersection(set(groups))) == 0:
        return HttpResponseBadRequest()

    if request.method == 'GET':
        user_id = request.user
        reset_password = models.UserProfile.objects.get(user=request.user).reset_password
        if not reset_password:
            return render(request, 'portal/change_password.html')
        if Roles.DEALERS in groups:
            use_cdms = models.Dealer.objects.get(user__user=user_id).use_cdms
        return render(request, TEMPLATE_MAPPING.get(menu, 'portal/404.html'), {'active_menu' : ACTIVE_MENU.get(menu)\
                                                                    , 'groups': groups,
                                                                    'user_id' : user_id,
                                                                    'use_cdms' : use_cdms})
    elif request.method == 'POST':
        save_user = {
            'asc': save_asc_registration,
            'sa': save_sa_registration,
            'customer': register_customer
        }
        try:
            response_object = save_user[menu](request, groups)
            return HttpResponse(response_object, content_type="application/json")
        except Exception as ex:
            logger.error('[registration failure {0}] : {1}'.format(menu, ex))
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

ASC_REGISTER_SUCCESS = 'ASC registration is complete.'
EXCEPTION_INVALID_DEALER = 'The dealer-id provided is not registered.'
ALREADY_REGISTERED = 'Already Registered Number.'


@check_service_active(Services.FREE_SERVICE_COUPON)
@log_time
def save_asc_registration(request, groups=None):
    if request.method == 'GET':
        return render(request, 'portal/asc_registration.html',
                      {'asc_registration': True})
    elif request.method == 'POST':
        data = request.POST
        try:
            asc_obj = models.ASCTempRegistration.objects.get(phone_number=data['phone-number'])
            return HttpResponse(json.dumps({'message': ALREADY_REGISTERED}),
                            content_type='application/json')
        except ObjectDoesNotExist as ex:
            
            dealer_data = data["dealer_id"] if data.has_key('dealer_id') else None  
            asc_obj = models.ASCTempRegistration(name=data['name'],
                 address=data['address'], password=data['password'],
                 phone_number=data['phone-number'], email=data['email'],
                 pincode=data['pincode'], dealer_id=dealer_data)
            asc_obj.save()
        return HttpResponse(json.dumps({'message': ASC_REGISTER_SUCCESS}),
                            content_type='application/json')

SA_UPDATE_SUCCESS = 'Service advisor status has been updated.'
SA_REGISTER_SUCCESS = 'Service advisor registration is complete.'
@log_time
def save_sa_registration(request, groups):
    data = request.POST
    existing_sa = False
    data_source = []
    phone_number = utils.mobile_format(str(data['phone-number']))
    if data['sa-id']:
        service_advisor_id = data['sa-id']
        existing_sa = True
    else:
        service_advisor_id = TEMP_SA_ID_PREFIX + str(random.randint(10 ** 5, 10 ** 6))
    data_source.append(utils.create_sa_feed_data(data, request.user.username, service_advisor_id))
    logger.info('[Temporary_sa_registration]:: Initiating dealer-sa feed for ID' + service_advisor_id)
    if Roles.ASCS in groups:
        feed_type = 'asc_sa'
    else:
        feed_type = 'dealer'
    feed_remark = FeedLogWithRemark(len(data_source),
                                                feed_type='Dealer Feed',
                                                action='Received', status=True)
    sap_obj = SAPFeed()
    feed_response = sap_obj.import_to_db(feed_type=feed_type,
                        data_source=data_source, feed_remark=feed_remark)
    if feed_response.failed_feeds > 0:
        failure_msg = list(feed_response.remarks.elements())[0]
        logger.info('[Temporary_sa_registration]:: dealer-sa feed fialed ' + failure_msg)
        return json.dumps({"message": failure_msg})
    logger.info('[Temporary_sa_registration]:: dealer-sa feed completed')
    if existing_sa:
        return json.dumps({'message': SA_UPDATE_SUCCESS})
    return json.dumps({'message': SA_REGISTER_SUCCESS})

CUST_UPDATE_SUCCESS = 'Customer phone number has been updated.'
CUST_REGISTER_SUCCESS = 'Customer has been registered with ID: '


@log_time
def register_customer(request, group=None):
    post_data = request.POST
    data_source = []
    existing_customer = False
    product_obj = models.ProductData.objects.filter(product_id=post_data['customer-vin'])
    if not post_data['customer-id']:
        temp_customer_id = utils.generate_temp_id(TEMP_ID_PREFIX)
    else:
        temp_customer_id = post_data['customer-id']
        existing_customer = True
    data_source.append(utils.create_purchase_feed_data(post_data, product_obj[0], temp_customer_id))

    check_with_invoice_date = utils.subtract_dates(data_source[0]['product_purchase_date'], product_obj[0].invoice_date)    
    check_with_today_date = utils.subtract_dates(data_source[0]['product_purchase_date'], datetime.datetime.now())
    if not existing_customer and check_with_invoice_date.days < 0 or check_with_today_date.days > 0:
        message = "Product purchase date should be between {0} and {1}".\
                format((product_obj[0].invoice_date).strftime("%d-%m-%Y"), (datetime.datetime.now()).strftime("%d-%m-%Y"))
        logger.info('[Temporary_cust_registration]:: {0} Entered date is: {1}'.format(message, str(data_source[0]['product_purchase_date'])))
        return json.dumps({"message": message})

    try:
        with transaction.atomic():
            update_count = models.Constant.objects.get(constant_name='vin_to_mobile_mapping_count').constant_value
            if models.CustomerTempRegistration.objects.filter(new_number__contains=data_source[0]['customer_phone_number']).count() >= int(update_count):
                message = get_template('PHONE_NUMBER_CANNOT_BE_REGISTERED')
                return json.dumps({'message' : message})

            customer_obj = models.CustomerTempRegistration.objects.filter(temp_customer_id=temp_customer_id)
            if customer_obj:
                customer_obj = customer_obj[0]
                update_count = models.Constant.objects.get(constant_name='mobile_number_update_count').constant_value
                if customer_obj.new_number != data_source[0]['customer_phone_number']:
                    if customer_obj.mobile_number_update_count >= int(update_count) and group[0] != Roles.SDMANAGERS:
                        customer_update = models.CustomerUpdateFailure(product_id=product_obj[0],
                                                                       customer_name=data_source[0]['customer_name'],
                                                                       customer_id=customer_obj.temp_customer_id,
                                                                       updated_by="dealer-" + str(request.user),
                                                                       old_number=customer_obj.new_number,
                                                                       new_number=data_source[0]['customer_phone_number'])
                        customer_update.save()
                        message = get_template('PHONE_NUMBER_UPDATE_COUNT_EXCEEDED')
                        return json.dumps({'message' : message})

                    if models.UserProfile.objects.filter(phone_number=data_source[0]['customer_phone_number']):
                        message = get_template('FAILED_UPDATE_PHONE_NUMBER').format(phone_number=data_source[0]['customer_phone_number'])
                        return json.dumps({'message': message})
                    
                    old_number = customer_obj.new_number
                    customer_obj.new_number = data_source[0]['customer_phone_number']
                    customer_obj.product_data = product_obj[0]
                    customer_obj.sent_to_sap = False
                    customer_obj.dealer_asc_id = str(request.user)
                    customer_obj.mobile_number_update_count += 1
                    update_history = models.CustomerUpdateHistory(temp_customer=customer_obj,
                                                                  updated_field='Phone Number',
                                                                  old_value=old_number,
                                                                  new_value=customer_obj.new_number,
                                                                  email_flag=False)
                    update_history.save()
                    message = get_template('CUSTOMER_MOBILE_NUMBER_UPDATE').format(customer_name=customer_obj.new_customer_name, new_number=customer_obj.new_number)
                    for phone_number in [customer_obj.new_number, old_number]:
                        phone_number = utils.get_phone_number_format(phone_number)
                        sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
                        send_job_to_queue(send_customer_phone_number_update_message, {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})
                            
                    if models.UserProfile.objects.filter(user__groups__name=Roles.BRANDMANAGERS).exists():
                        groups = utils.stringify_groups(request.user)
                        if Roles.ASCS in groups:
                            dealer_asc_id = "asc : " + customer_obj.dealer_asc_id
                        elif Roles.DEALERS in groups:
                            dealer_asc_id = "dealer : " + customer_obj.dealer_asc_id
                        else :
                            dealer_asc_id = "manager : " + customer_obj.dealer_asc_id
                        
                        message = get_template('CUSTOMER_PHONE_NUMBER_UPDATE').format(customer_id=customer_obj.temp_customer_id, old_number=old_number,
                                                                                  new_number=customer_obj.new_number, dealer_asc_id=dealer_asc_id)
                        managers = models.UserProfile.objects.filter(user__groups__name=Roles.BRANDMANAGERS)
                        for manager in managers:
                            phone_number = utils.get_phone_number_format(manager.phone_number)
                            sms_log(settings.BRAND, receiver=phone_number, action=AUDIT_ACTION, message=message)
                            send_job_to_queue(send_customer_phone_number_update_message, {"phone_number":phone_number, "message":message, "sms_client":settings.SMS_CLIENT})

            else:
                if models.UserProfile.objects.filter(phone_number=data_source[0]['customer_phone_number']):
                    message = get_template('FAILED_UPDATE_PHONE_NUMBER').format(phone_number=data_source[0]['customer_phone_number'])
                    return json.dumps({'message': message})

                customer_obj = models.CustomerTempRegistration(product_data=product_obj[0],
                                                               new_customer_name=data_source[0]['customer_name'],
                                                               new_number=data_source[0]['customer_phone_number'],
                                                               product_purchase_date=data_source[0]['product_purchase_date'],
                                                               temp_customer_id=temp_customer_id,
                                                               dealer_asc_id=str(request.user))
            customer_obj.save()
            logger.info('[Temporary_cust_registration]:: Initiating purchase feed')
            feed_remark = FeedLogWithRemark(len(data_source),
                                                feed_type='Purchase Feed',
                                                action='Received', status=True)
            sap_obj = SAPFeed()
            feed_response = sap_obj.import_to_db(feed_type='purchase', data_source=data_source, feed_remark=feed_remark)
            if feed_response.failed_feeds > 0:
                logger.info('[Temporary_cust_registration]:: ' + json.dumps(feed_response.remarks))
                raise ValueError('purchase feed failed!')
            logger.info('[Temporary_cust_registration]:: purchase feed completed')
    except Exception as ex: 
        logger.info(ex)

        return HttpResponseBadRequest()
    if existing_customer:
        return json.dumps({'message': CUST_UPDATE_SUCCESS})
    return json.dumps({'message': CUST_REGISTER_SUCCESS + temp_customer_id})


@check_service_active(Services.FREE_SERVICE_COUPON)
def recover_coupon_info(data):
    customer_id = data['customerId']
    logger.info('UCN for customer {0} requested by User {1}'.format(customer_id, data['current_user']))
    coupon_data = utils.get_coupon_info(data)
    if coupon_data:
        user_obj = models.UserProfile.objects.get(user=data['current_user'])
        file_obj = data['job_card']
        customer_id = data['customerId']
        reason = data['reason']
        file_obj.name = get_file_name(data, file_obj)
        destination = settings.JOBCARD_DIR.format('bajaj')
        bucket = settings.JOBCARD_BUCKET
        path = utils.upload_file(destination, bucket, file_obj, logger_msg="JobCard")
        ucn_recovery_obj = models.UCNRecovery(reason=reason, user=user_obj,
                                        customer_id=customer_id, file_location=path,
                                        unique_service_coupon=coupon_data.unique_service_coupon)
        ucn_recovery_obj.save()
        send_recovery_email_to_admin(ucn_recovery_obj, coupon_data)
        message = 'UCN for customer {0} is {1}.'.format(customer_id,
                                                    coupon_data.unique_service_coupon)
        return {'status': True, 'message': message}
    else:
        message = 'No coupon in progress for customerID {0}.'.format(customer_id) 
        return {'status': False, 'message': message}


def get_customer_info_old(data):
    try:
        product_obj = models.ProductData.objects.get(product_id=data['vin'])
    except Exception as ex:
        logger.info(ex)
        message = '''VIN '{0}' does not exist in our records. Please contact customer support: +91-7847011011.'''.format(data['vin'])
        if data['groups'][0] == Roles.DEALERS:
            data['groups'][0] = "Dealer"
        else:
            data['groups'][0] = "ASC"
        template = get_email_template('VIN DOES NOT EXIST', settings.BRAND)['body'].format(data['current_user'], data['vin'], data['groups'][0])
        send_mail_when_vin_does_not_exist(data=template)
        return {'message': message, 'status': 'fail'}
    if product_obj.purchase_date:
        product_data = format_product_object(product_obj)
        product_data['group'] = data['groups'][0] 
        return product_data
    else:
        message = '''VIN '{0}' has no associated customer. Please register the customer.'''.format(data['vin'])
        return {'message': message}

def vin_sync_feed(request):
    message = ''
    post_data = request.POST.copy()
    post_data['current_user'] = request.user
    try:
        vin_sync_feed = export_feed.ExportUnsyncProductFeed(username=settings.SAP_CRM_DETAIL[
                       'username'], password=settings.SAP_CRM_DETAIL['password'],
                      wsdl_url=settings.VIN_SYNC_WSDL_URL, feed_type='VIN sync Feed')
        message = vin_sync_feed.export(data=post_data)
    except Exception as ex:
        logger.info(ex)

    return HttpResponse(content=json.dumps({'message':message}), content_type='application/json')
    
def get_customer_info(data):
    try:
        product_obj = models.ProductData.objects.get(product_id=data['vin'])
    except Exception as ex:
        logger.info(ex)
        message = "The Chassis {0} is not available in the current database, please wait while the Main database is being scanned.".format(data['vin'])
        return {'message': message, 'status': 0}
    if product_obj.purchase_date:
        product_data = format_product_object(product_obj)
        product_data['group'] = data['groups'][0] 
        return {'product': product_data, 'status': 1}
    else:
        message = '''VIN '{0}' has no associated customer. Please register the customer.'''.format(data['vin'])
        return {'message': message, 'status': 1}

@login_required()
def exceptions(request, exception=None):
    groups = utils.stringify_groups(request.user)
    if len(set([Roles.ASCS, Roles.DEALERS, Roles.SDMANAGERS]).intersection(set(groups))) == 0:
        return HttpResponseBadRequest()
    is_dealer = False
    if Roles.DEALERS in groups:
        is_dealer = True
    if request.method == 'GET':
        template = 'portal/exception.html'
        data = None
        if exception in ['close', 'check']:
            if Roles.ASCS in groups:
                data = models.ServiceAdvisor.objects.active_under_asc(request.user)
            else:
                data = models.ServiceAdvisor.objects.active_under_dealer(request.user)
        return render(request, template, {'active_menu': exception,
                                           "data": data, 'groups': groups, 'is_dealer':is_dealer})
    elif request.method == 'POST':
        function_mapping = {
            'customer': get_customer_info,
            'recover': recover_coupon_info,
            'search': utils.search_details,
            'status': utils.services_search_details,
            'serviceadvisor': utils.service_advisor_search
        }
        try:
            post_data = request.POST.copy()
            post_data['current_user'] = request.user
            post_data['groups'] = groups
            if request.FILES:
                post_data['job_card'] = request.FILES['jobCard']
            data = function_mapping[exception](post_data)
            return HttpResponse(content=json.dumps(data), content_type='application/json')
        except Exception as ex:
            logger.error(ex)
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@check_service_active(Services.FREE_SERVICE_COUPON)
@login_required()
def users(request, users=None):
    groups = utils.stringify_groups(request.user)
    if not (Roles.ASCS in groups or Roles.DEALERS in groups):
        return HttpResponseBadRequest()
    if request.method == 'GET':
        template = 'portal/users.html'
        data = None
        data_mapping = {
            'sa': utils.get_sa_list_for_login_dealer,
            'asc': utils.get_asc_list_for_login_dealer
        }
        try:
            data = data_mapping[users](request.user)
        except:
            # It is acceptable if there is no data_mapping defined for a function
            pass
        return render(request, template, {'active_menu' : users, "data" : data, 'groups': groups})
    else:
        return HttpResponseBadRequest()


@check_service_active(Services.FREE_SERVICE_COUPON)
@login_required()
def get_sa_under_asc(request, id=None):
    template = 'portal/sa_list.html'
    data = None
    try:
        data = utils.get_sa_list_for_login_dealer(id)
    except:
            # It is acceptable if there is no data_mapping defined for a function
        pass
    return render(request, template, {'active_menu':'sa', "data": data})


def sqs_tasks_view(request):
    return render_to_response('trigger-sqs-tasks.html')


def trigger_sqs_tasks(request):
    sqs_tasks = {
        'send-feed-mail': 'send_report_mail_for_feed',
        'export-coupon-redeem': 'export_coupon_redeem_to_sap',
        'expire-service-coupon': 'expire_service_coupon',
        'send-reminder': 'send_reminder',
        'export-customer-registered': 'export_customer_reg_to_sap',
        'send_reminders_for_servicedesk': 'send_reminders_for_servicedesk',
        'export_purchase_feed_sync_to_sap': 'export_purchase_feed_sync_to_sap',
        'send_mail_for_policy_discrepency': 'send_mail_for_policy_discrepency',
        'export_cts_to_sap': 'export_cts_to_sap',
        'send_mail_for_feed_failure': 'send_mail_for_feed_failure',
        'send_mail_for_customer_phone_number_update':'send_mail_for_customer_phone_number_update',
        'send_mail_for_manufacture_data_discrepancy': 'send_mail_for_manufacture_data_discrepancy',
        'send_vin_sync_feed_details': 'send_vin_sync_feed_details'
    }

    taskqueue = SqsTaskQueue(settings.SQS_QUEUE_NAME, settings.BRAND)
    taskqueue.add(sqs_tasks[request.POST['task']], settings.BRAND)
    return HttpResponse()


def site_info(request):
    if request.method != 'GET':
        raise Http404
    brand = settings.BRAND
    return HttpResponse(json.dumps({'brand': brand}), content_type='application/json')


@check_service_active(Services.FREE_SERVICE_COUPON)
@login_required()
def reports(request):
    groups = utils.stringify_groups(request.user)
    report_data = []
    if not (Roles.ASCS in groups or Roles.DEALERS in groups):
        return HttpResponseBadRequest()
    status_options = {'4': 'In Progress', '2':'Closed'}
    report_options = {'reconciliation': 'Reconciliation', 'credit':'Credit Note'}
    min_date, max_date = utils.get_min_and_max_filter_date()
    template_rendered = 'portal/reconciliation_report.html'
    report_data = {'status_options': status_options,
                    'report_options': report_options,
                    'min_date':min_date,
                    'max_date': max_date}
    if request.method == 'POST':
        report_data['params'] = request.POST.copy()
        if report_data['params']['type'] == 'credit':
            report_data['params']['status'] = '2'
            template_rendered = 'portal/credit_note_report.html'
        report_data['records'] = create_reconciliation_report(report_data['params'], request.user)
        if '_download' in request.POST:
            return download_reconcilation_reports(report_data)
    return render(request, template_rendered, report_data)

@log_time
def create_reconciliation_report(query_params, user):
    report_data = []
    filter = {}
    params = {}
    coupon_filter = []
    args = [Q(status=4), Q(status=2), Q(status=6)]
    if user.groups.filter(name=Roles.DEALERS).exists():
        dealer = models.Dealer.objects.filter(dealer_id=user)
        coupon_filter = [Q(service_advisor__dealer=dealer[0]), Q(servicing_dealer=dealer[0].dealer_id)]
    else:
        ascs = models.AuthorizedServiceCenter.objects.filter(user=user)
        coupon_filter = [Q(service_advisor__asc=ascs[0]), Q(servicing_dealer=ascs[0].asc_id)]
    
    status = query_params.get('status')
    from_date = query_params.get('from')
    to_date = query_params.get('to')
    input_date_range = (str(from_date) + ' 00:00:00', str(to_date) + ' 23:59:59')

    if query_params['type'] == 'credit': 
        filter['credit_date__range'] = input_date_range
    elif status == '4':
        filter['actual_service_date__range'] = input_date_range
    else:
        filter['closed_date__range'] = input_date_range

    if status:
        args = [Q(status=status)]
        if status == '2':
            args = [Q(status=2), Q(status=6)]
    all_coupon_data = models.CouponData.objects.filter(reduce(operator.or_, args), reduce(operator.or_, coupon_filter), **filter).order_by('-actual_service_date')
    map_status = {'6': 'Old FSC Closed', '4': 'In Progress', '2':'DFSC Closed'}
    for coupon_data in all_coupon_data:
        coupon_data_dict = {}
        coupon_data_dict['vin'] = coupon_data.product.product_id
        sa = coupon_data.service_advisor
        try:
            coupon_data_dict['sa_phone_name'] = sa.user.phone_number
        except:
            coupon_data_dict['sa_phone_name'] = None
        coupon_data_dict['service_avil_date'] = coupon_data.actual_service_date
        coupon_data_dict['closed_date'] = coupon_data.closed_date
        coupon_data_dict['service_status'] = map_status[str(coupon_data.status)]
        if query_params['type'] == 'credit':
            product_details = coupon_data.product
            coupon_data_dict['customer_name'] = product_details.customer_name
            coupon_data_dict['customer_number'] = product_details.customer_phone_number
            coupon_data_dict['credit_date'] = coupon_data.credit_date
            coupon_data_dict['credit_note'] = coupon_data.credit_note
        else:
            coupon_data_dict['customer_id'] = coupon_data.product.customer_id
            coupon_data_dict['product_type'] = coupon_data.product.product_type
            coupon_data_dict['coupon_no'] = coupon_data.unique_service_coupon
            coupon_data_dict['kms'] = coupon_data.actual_kms
            coupon_data_dict['service_type'] = coupon_data.service_type
            coupon_data_dict['special_case'] = coupon_data.special_case
        report_data.append(coupon_data_dict)
        
    return report_data

# FIXME: Refactor the code
@check_service_active(Services.FREE_SERVICE_COUPON)
def get_active_asc_report(request, role=None):
    '''get number of tickets closed by ASC'''
    if request.method != 'GET':
        return HttpResponse(json.dumps({"message":"method not allowed"}), content_type="application/json", status=401)
    try:
        role = request.path.split('/')[3]
        data = request.GET.copy()
        if data.has_key('month'):
            month = MONTHS.index(data['month']) + 1
            year = data['year']
        else:
            now = datetime.datetime.now()
            year = now.year
            month = now.month
        no_of_days = utils.get_number_of_days(year, month)
        coupon_resource = CouponDataResource()
        asc_query = coupon_resource.closed_ticket(year, month, role)

        asc_list = []
        for asc in asc_query:
            active = filter(lambda active: active['id'] == asc['asc_id'], asc_list)
            if not active:
                temp = {}
                temp['id'] = asc['asc_id'] 
                temp['name'] = asc['first_name']
                temp['address'] = asc['address']
                temp['coupon_closed'] = {}
                for day in range(1, no_of_days):
                    temp['coupon_closed'][day] = 0
                day = int(asc['day'])
                temp['total_coupon_closed'] = 0 
                temp['coupon_closed'][day] = asc['cnt']
                temp['total_coupon_closed'] = temp['total_coupon_closed'] + asc['cnt']
                asc_list.append(temp)
            else:
                day = int(asc['day'])
                active[0]['coupon_closed'][day] = asc['cnt']
                active[0]['total_coupon_closed'] = active[0]['total_coupon_closed'] + asc['cnt']
    except Exception as ex:
        logger.error('Exception while counting data : {0}'.format(ex))
        return HttpResponseBadRequest()
    years = utils.gernate_years()
    return render(request, 'portal/asc_report.html', \
                  {"data": asc_list,
                   "range": range(1, no_of_days),
                   "month": MONTHS,
                   "years": years,
                   "mon": MONTHS[int(month) - 1],
                   "cyear": str(year),
                   "role": role
                   })
    
'''Download the reconciliation report under the filter criteria'''
    
def download_reconcilation_reports(download_data):
    response = HttpResponse(content_type='text/excel')
    response['Content-Disposition'] = 'attachment; filename="ReportList.xls"'
    c = Context({
        'data': download_data['records'],
    })
    if download_data['params']['type'] == 'credit':
        template = loader.get_template('portal/reconciliation_credit_download.html')
    else:
        template = loader.get_template('portal/reconciliation_download.html')
    
    response.write(template.render(c))
    return response

@login_required
def rejected_reason(request):
    '''
    This method updates the retailer with the reason for rejection by the ASM/admin
    '''
    retailer_id = request.POST['retailer_id']
    rejected_reason = request.POST['rejected_reason']
    retailer_email = request.POST['retailer_email']
    Retailer.objects.filter(id=retailer_id).update(approved=STATUS['REJECTED'], \
                                                 rejected_reason=rejected_reason)
    try:
        send_email(sender=constants.FROM_EMAIL_ADMIN, receiver=retailer_email,
                   subject=constants.REJECT_RETAILER_SUBJECT, body='',
                   message=constants.REJECT_RETAILER_MESSAGE)
    except Exception as e:
        logger.error('Mail is not sent. Exception occurred', e)
    return HttpResponseRedirect('/admin/bajaj/retailer/')

def handle_uploaded_file(uploaded_file):
    '''
    This method gets the uploaded file and writes it in the upload dir under the same name
    '''
    path = settings.UPLOAD_DIR + uploaded_file.name
    with open(path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return path

@login_required
def bulk_upload_retailer(request):
    '''
    This method uploads retailers in bulk to the retailer model
    '''
    # upload the file to the upload_bajaj folder
    full_path = handle_uploaded_file(request.FILES['bulk_upload_retailer'])
    with open(full_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # get the userprofile data and save it in userprofile model
            userprofile = UserProfile()
            userprofile.user = \
                    User.objects.create_user(username=row['username'], password=row['password'])
            userprofile.country = row['country']
            userprofile.pincode = row['pincode']
            userprofile.state = row['state']
            userprofile.address = row['address']
            userprofile.save()
            # get the retailer data and save it in retailer model
            retailer = Retailer()
            retailer.retailer_name = row['retailer name']
            retailer.retailer_town = row['retailer town']
            retailer.billing_code = row['billing code']
            retailer.territory = row['territory']
            retailer.email = row['email']
            retailer.mobile = row['mobile']
            retailer.language = row['language']
            retailer.user = UserProfile.objects.get(user__username=row['username'])
            if DistributorStaff.objects.filter(user__user=request.user).exists():
                distributorstaff = DistributorStaff.objects.get(user__user=request.user)
                retailer.distributor = \
                        Distributor.objects.get(id=distributorstaff.distributor.id)
            else:
                retailer.distributor = \
                        Distributor.objects.get(user__user=request.user)
            retailer.save()
    return HttpResponseRedirect('/admin/bajaj/retailer/')
    
