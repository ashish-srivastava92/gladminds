import json
import logging
from datetime import datetime, timedelta, date

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.contrib.sites.models import RequestSite


from tastypie.utils.urls import trailing_slash
from tastypie import fields,http, bundle
from tastypie.http import HttpBadRequest
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.exceptions import ImmediateHttpResponse

from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.auth.access_token_handler import create_access_token, \
    delete_access_token
    
from gladminds.core import constants

from gladminds.core.model_fetcher import models
from gladminds.core.model_fetcher import get_model

from django.db import connections

from gladminds.bajaj.models import RetailerTarget,DistributorTarget,AsmTarget,NsmTarget,DistributorSalesRepTarget
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gladminds.core.auth_helper import Roles
from gladminds.core import constants
from gladminds.bajaj.models import DistributorSalesRep, Retailer,PartModels, Categories, \
                            PartPricing, Distributor,  Invoices, \
                            Collection,CollectionDetails,PartsStock,DSRWorkAllocation,DSRLocationDetails, \
                            NationalSparesManager,AreaSparesManager
from gladminds.bajaj.models import PartPricing,OrderPart,OrderPartDetails, \
                        PartIndexDetails, PartIndexPlates, FocusedPart
from django.shortcuts import render
from django.http import HttpResponse
import pytz
LOG = logging.getLogger('gladminds')




class NsmTargetResource(CustomBaseModelResource):
        '''
            National Spares Manager Target Resource
        '''
        class Meta:
                queryset = models.NsmTarget.objects.all()
                resource_name = "national-spares-manager-target"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

class AsmTargetResource(CustomBaseModelResource):
        '''
            Area Spares Manager Target Resource
        '''
        class Meta:
                queryset = models.AsmTarget.objects.all()
                resource_name = "area-spares-manager-target"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

class DistributorTargetResource(CustomBaseModelResource):
        '''
            Distributor Target Resource
        '''
        class Meta:
                queryset = models.DistributorTarget.objects.all()
                resource_name = "distributor-target"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

class DistributorSalesRepTargetResource(CustomBaseModelResource):
        '''
            DistributorSalesRep Target Resource
        '''
        class Meta:
                queryset = models.DistributorSalesRepTarget.objects.all()
                resource_name = "distributor-sales-rep-target"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True


class RetailerTargetResource(CustomBaseModelResource):
        '''
            Retailer Target Resource
        '''
        class Meta:
                queryset = models.RetailerTarget.objects.all()
                resource_name = "retailer-target"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

##FIXME: Highlights should only allow GET methods
class AsmHighlightsResource(CustomBaseModelResource):
        '''
            Area Spares Manager Highlights Resource
        '''
        class Meta:
                queryset = models.AsmHighlights.objects.all()
                resource_name = "area-spares-manager-highlights"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

class NsmHighlightsResource(CustomBaseModelResource):
        '''
            Area Spares Manager Highlights Resource
        '''
        class Meta:
                queryset = models.NsmHighlights.objects.all()
                resource_name = "national-spares-manager-highlights"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

class DistributorHighlightsResource(CustomBaseModelResource):
        '''
            Distributor Highlights Resource
        '''
        class Meta:
                queryset = models.DistributorHighlights.objects.all()
                resource_name = "distributor-highlights"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True

class DistributorSalesRepHighlightsResource(CustomBaseModelResource):
        '''
            Distributor Sales Rep Highlights Resource
        '''
        class Meta:
                queryset = models.DistributorSalesRepHighlights.objects.all()
                resource_name = "distributor-sales-rep-highlights"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True


class RetailerHighlightsResource(CustomBaseModelResource):
        '''
            Retailer Highlights Resource
        '''
        class Meta:
                queryset = models.RetailerHighlights.objects.all()
                resource_name = "retailer-highlights"
                authorization = Authorization()
                #authentication = AccessTokenAuthentication()
                allowed_methods = ['get', 'post', 'put']
                always_return_data = True


def get_retailer_report(retailer,month,year):
    retailer_report={}
    retailer_report["report_type"] = "month"
    #print(type(month))
    date=datetime.strptime(str(month)+'-1'+'-'+str(year),"%m-%d-%Y")
    start_datetime=datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    print start_datetime
    today=datetime.today()
    if date.month == today.month and date.year == today.year:
        end_date=datetime.today()#.date()
    else:
        end_date=datetime.strptime(str(int(month)+1)+'-1'+'-'+str(year),"%m-%d-%Y")
        end_datetime=datetime(end_date.year,end_date.month,end_date.day,0,0,0,0,pytz.timezone('UTC'))
        
    print end_datetime
    try:
        try:
            retailer_target = RetailerTarget.objects.get(retailer=retailer,month=month,year=year)
            retailer_report["target_per_month"] = retailer_target.target
        except:
            retailer_report["target_per_month"] = 0
        retailer_report["retailer_id"] = retailer.retailer_code
        #Get the actual order
        retailer_line_total = 0
        retailer_total_mrp = 0
        #FIXME: Can use order_date field
        orders = OrderPart.objects.filter(retailer=retailer , created_date__range=(start_datetime,end_datetime))
        print "length of orders", len(orders)
        #retailer_report["orders"]=orders
        #Set of unique parts
        line_billings=set()
        #Set of recent created parts
        new_parts_billed=set()

        total_outstanding_amount = 0
        invoices = Invoices.objects.filter(retailer=retailer , created_date__range=(start_datetime,end_datetime))
        for invoice in invoices:
            invoice.invoice_amount = invoice.invoice_amount if invoice.invoice_amount else 0
            invoice.paid_amount = invoice.paid_amount if invoice.paid_amount else 0
            total_outstanding_amount = total_outstanding_amount + (invoice.invoice_amount - invoice.paid_amount)
        total_outstanding_amount = float(format(total_outstanding_amount, '.2f'))

        if orders:
            for order in orders:
                order_details=OrderPartDetails.objects.filter(order=order)
                for order_detail in order_details:
                    #FIXME:Add just id field
                    line_billings.add(order_detail.part_number)
                    retailer_line_total += order_detail.line_total
                    new_partpricing = PartPricing.objects.get(id=order_detail.part_number_id)
                    if new_partpricing:
                        try:
                            if new_partpricing.created_date.month==int(month) and new_partpricing.created_date.year==int(year):
                                new_parts_billed.add(new_partpricing.id) 
                                print "New Parts          ",len(new_parts_billed)
                            #print new_partpricing.created_date.month,month
                            #print new_partpricing.created_date.year,year
                        except:
                            pass
                    #FIXME: mrp field in DB is varchar could be changed to int
                    #retailer_total_mrp += int(partpricing.mrp)
            #retailer_report["Actual"] = retailer_total_mrp
            
            retailer_report["number_of_line_billings"] = len(line_billings)#retailer_line_total#retailer.total_sale_parts
            retailer_report["new_parts_billed"] = len(new_parts_billed)#retailer_line_total#retailer.total_sale_parts
            retailer_report["order_value"] = retailer_line_total#retailer_total_mrp
            retailer_report["total_outstanding_amount"]=total_outstanding_amount
            retailer_report["collection_value"] = ""
        else:
            #retailer_report["Actual"] = month
            retailer_report["number_of_line_billings"] = 0
            retailer_report["order_value"] = 0
            retailer_report["collection_value"] = 0
    except Exception as e:
        retailer_report["Error"]= e
        retailer_report["Actual"] = 0
        retailer_report["number_of_line_billings"] = 0
        retailer_report["order_value"] = 0
        retailer_report["collection_value"] = 0
    return retailer_report

#@api_view(['GET'])
def get_admin_reports(month,year,flag=None):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
    date=datetime.strptime(str(month)+'-1'+'-'+str(year),"%m-%d-%Y")
    start_datetime=datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    print start_datetime
    today=datetime.today()
    if date.month == today.month and date.year == today.year:
        end_date=datetime.today()#.date()
    else:
        end_date=datetime.strptime(str(int(month)+1)+'-1'+'-'+str(year),"%m-%d-%Y")
        end_datetime=datetime(end_date.year,end_date.month,end_date.day,0,0,0,0,pytz.timezone('UTC'))
        
    print end_datetime
    try:
        nsms=NationalSparesManager.objects.all()
        new_parts_billed=0
        total_order_value = 0
        retailer_count=0
        newretailers=0
        for nsm in nsms:
            asms=AreaSparesManager.objects.filter(nsm__nsm_id=nsm.nsm_id)
            for asm in asms:
                distributors=Distributor.objects.filter(asm__asm_id=asm.asm_id)
                for distributor in distributors:
                    dsrs=DistributorSalesRep.objects.filter(distributor__distributor_id=distributor.distributor_id)
                    for dsr in dsrs:
                        dsr_id=dsr.id
                        retailers=Retailer.objects.filter(dsr_id=dsr_id)
                        ##FIXME:Can use len()
                        retailer_count+=Retailer.objects.filter(dsr_id=dsr_id).count()
                        print month, year
                        print type(month)
                        print type(year)
                        newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime)).count()
                        print "new 1's",newretailers 
                        orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime))
                        #New parts billed
                        for order in orderpart:
                            orderpartdetails=OrderPartDetails.objects.filter(order=order).count()#,created_date__range=(start_datetime,end_datetime)).count()

                            new_parts_billed += orderpartdetails
                        #Monthly Report
                        for retailer in retailers:
                           retailer_report = get_retailer_report(retailer,month,year)
                           #FIXME: total_order_value is now based on total retailer's orders
                           total_order_value += retailer_report["order_value"]
                           report.append(retailer_report)
        report_type1={}
        report_type1["target"] = "NA"
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        #report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except Exception as e:
        report_type1={}
        report_type1["target"] = e
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        #report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    if flag:
        return Response(report)
    else:
        return report

     
def get_nsm_reports(nsm_id,month,year,flag=None):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
    date=datetime.strptime(str(month)+'-1'+'-'+str(year),"%m-%d-%Y")
    start_datetime=datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    print start_datetime
    today=datetime.today()
    if date.month == today.month and date.year == today.year:
        end_date=datetime.today()#.date()
    else:
        end_date=datetime.strptime(str(int(month)+1)+'-1'+'-'+str(year),"%m-%d-%Y")
        end_datetime=datetime(end_date.year,end_date.month,end_date.day,0,0,0,0,pytz.timezone('UTC'))
        
    print end_datetime
    try:
        asms=AreaSparesManager.objects.filter(nsm__nsm_id=nsm_id)
        new_parts_billed=0
        total_order_value = 0
        retailer_count=0
        newretailers=0
        for asm in asms:
            distributors=Distributor.objects.filter(asm__asm_id=asm.asm_id)
            for distributor in distributors:
                dsrs=DistributorSalesRep.objects.filter(distributor__distributor_id=distributor.distributor_id)
                for dsr in dsrs:
                    dsr_id=dsr.id
                    retailers=Retailer.objects.filter(dsr_id=dsr_id)
                    ##FIXME:Can use len()
                    retailer_count+=Retailer.objects.filter(dsr_id=dsr_id).count()
                    newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime)).count()
                    orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime))
                    #New parts billed
                    for order in orderpart:
                        orderpartdetails=OrderPartDetails.objects.filter(order=order,created_date__range=(start_datetime,end_datetime)).count()
                        new_parts_billed += orderpartdetails
                    #Monthly Report
                    for retailer in retailers:
                       retailer_report = get_retailer_report(retailer,month,year)
                       total_order_value += retailer_report['order_value']
                       report.append(retailer_report)
        report_type1={}
        # print report
        nsmtarget=NsmTarget.objects.filter(nsm__nsm_id=nsm_id,month=month,year=year,active=1)
        print nsmtarget
        if nsmtarget:
            report_type1["target"] = nsmtarget[0].target
        else:
            report_type1["target"] = 0
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        #report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except Exception as e:
        report_type1={}
        print e
        nsmtarget=NsmTarget.objects.filter(nsm__nsm_id=nsm_id,month=month,year=year,active=1).values()
        #report_type1["target"] = nsmtarget.target
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        #report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    if flag:
        return Response(report)
    else:
        return report

#@api_view(['GET'])
def get_asm_reports(asm_id,month,year,flag=None):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
    date=datetime.strptime(str(month)+'-1'+'-'+str(year),"%m-%d-%Y")
    start_datetime=datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    print start_datetime
    today=datetime.today()
    if date.month == today.month and date.year == today.year:
        end_date=datetime.today()#.date()
    else:
        end_date=datetime.strptime(str(int(month)+1)+'-1'+'-'+str(year),"%m-%d-%Y")
        end_datetime=datetime(end_date.year,end_date.month,end_date.day,0,0,0,0,pytz.timezone('UTC'))
        
    print end_datetime
    try:
        distributors=Distributor.objects.filter(asm__asm_id=asm_id)
        new_parts_billed=0
        total_order_value = 0
        retailer_count=0
        newretailers=0
        for distributor in distributors:
            dsrs=DistributorSalesRep.objects.filter(distributor__distributor_id=distributor.distributor_id)
            for dsr in dsrs:
                dsr_id=dsr.id
                retailers=Retailer.objects.filter(dsr_id=dsr_id)
                ##FIXME:Can use len()
                retailer_count+=Retailer.objects.filter(dsr_id=dsr_id).count()
                newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime)).count()
                orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime))
                #New parts billed
                for order in orderpart:
                    orderpartdetails=OrderPartDetails.objects.filter(order=order).count()#,created_date__month=month,created_date__year=year).count()
                    new_parts_billed += orderpartdetails
                #Monthly Report
                for retailer in retailers:
                   retailer_report = get_retailer_report(retailer,month,year)
                   #total_order_value += retailer_report['order_value']
                   report.append(retailer_report)
        report_type1={}
        asmtarget=AsmTarget.objects.filter(asm__asm_id=asm_id,month=month,year=year,active=1)
        print asmtarget
        if asmtarget:
            report_type1["target"] = asmtarget[0].target
        else:
            report_type1["target"] = 0

        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        #report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except Exception as e:
        print e
        report_type1={}
        asmtarget=AsmTarget.objects.filter(asm__asm_id=asm_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = 0#asmtarget.target
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        #report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    if flag:
        return Response(report)
    else:
        return report

def get_distributor_reports(distributor_id,month,year,flag=None):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
    date=datetime.strptime(str(month)+'-1'+'-'+str(year),"%m-%d-%Y")
    start_datetime=datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    print start_datetime
    today=datetime.today()
    if date.month == today.month and date.year == today.year:
        end_date=datetime.today()#.date()
    else:
        end_date=datetime.strptime(str(int(month)+1)+'-1'+'-'+str(year),"%m-%d-%Y")
        end_datetime=datetime(end_date.year,end_date.month,end_date.day,0,0,0,0,pytz.timezone('UTC'))
        
    print end_datetime
    try:
        dsrs=DistributorSalesRep.objects.filter(distributor__distributor_id=distributor_id)
        new_parts_billed=0
        total_order_value = 0
        retailer_count=0
        newretailers=0
        for dsr in dsrs:
            dsr_id=dsr.id
            retailers=Retailer.objects.filter(dsr_id=dsr_id)
            ##FIXME:Can use len()
            retailer_count+=Retailer.objects.filter(dsr_id=dsr_id).count()
            newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime)).count()
            orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
            #New parts billed
            for order in orderpart:
                orderpartdetails=OrderPartDetails.objects.filter(order=order).count()#,created_date__range=(start_datetime,end_datetime)).count()
                new_parts_billed += orderpartdetails
            #Monthly Report
            for retailer in retailers:
               retailer_report = get_retailer_report(retailer,month,year)
               total_order_value += retailer_report['order_value']
               report.append(retailer_report)
        report_type1={}
        distributortarget=DistributorTarget.objects.filter(distributor__distributor_id=distributor_id,month=month,year=year,active=1)
        if distributortarget:
            report_type1["target"] = distributortarget[0].target
        else:
            report_type1["target"] = 0
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        #report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except:
        report_type1={}
        distributortarget=DistributorTarget.objects.filter(distributor__distributor_id=distributor_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = distributortarget.target
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        #report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    if flag:
        return Response(report)
    else:
        return report

def get_dsr_reports(dsr_id,month,year,flag=None):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
    date=datetime.strptime(str(month)+'-1'+'-'+str(year),"%m-%d-%Y")
    start_datetime=datetime(date.year,date.month,date.day,0,0,0,0,pytz.timezone('UTC'))
    print start_datetime
    today=datetime.today()
    if date.month == today.month and date.year == today.year:
        end_date=datetime.today()#.date()
    else:
        end_date=datetime.strptime(str(int(month)+1)+'-1'+'-'+str(year),"%m-%d-%Y")
        end_datetime=datetime(end_date.year,end_date.month,end_date.day,0,0,0,0,pytz.timezone('UTC'))
        
    print end_datetime
    try:
        retailer=Retailer.objects.filter(dsr_id=dsr_id)
        ##FIXME:Can use len()
        retailer_count=Retailer.objects.filter(dsr_id=dsr_id).count()
        newretailers=Retailer.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime)).count()
        orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__range=(start_datetime,end_datetime))
        new_parts_billed=0
        #New parts billed
        top_qty=0
        top_val=0
        top_qty_dict={}
        top_val_dict={}
        for order in orderpart:
            orderpartdetails_count=OrderPartDetails.objects.filter(order=order).count()#,created_date__month=month,created_date__year=year).count()
            orderpartdetails=OrderPartDetails.objects.filter(order=order)#,created_date__month=month,created_date__year=year)
            if top_qty_dict[orderpartdetails.part_number.part_number]:
                top_qty_dict[orderpartdetails.part_number.part_number]+=orderpartdetails.quantity
            else:
                top_qty_dict[orderpartdetails.part_number.part_number]=0
            if top_val_dict[orderpartdetails.part_number.part_number]:
                top_val_dict[orderpartdetails.part_number.part_number]+=orderpartdetails.line_total
            else:
                top_val_dict[orderpartdetails.part_number.part_number]=0
            #new_parts_billed += orderpartdetails_count
        top_qty_list=[]
        for no in top_qty_dict:
            top_qty_list.append((top_qty_dict[no],no))
        top_val_list=[]
        for no in top_val_dict:
            top_val_list.append((top_val_dict[no],no))
        top_qty_list.sort()
        top_val_list.sort()

        total_order_value = 0
        #Monthly Report
        for retailer in retailers:
           retailer_report = get_retailer_report(retailer,month,year)
           total_order_value += retailer_report['order_value']
           report.append(retailer_report)
        report_type1={}
        dsrtarget=DistributorSalesRepTarget.objects.filter(dsr_id=dsr_id,month=month,year=year,active=1)
        print dsrtarget
        if dsrtarget:
            report_type1["target"] = dsrtarget[0].target
        else:
            report_type1["target"] = 0
        report_type1["total_retailers"] = retailer_count
        #report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report_type1["total_order_value"] = total_order_value
        report_type1["top_selling_qty_number"] = top_qty_list[0][1]
        report_type1["top_selling_qty"] = top_qty_list[0][0]
        report_type1["top_selling_val_number"] = top_val_list[0][1]
        report_type1["top_selling_val"] = top_val_list[0][0]
        report[0].update(report_type1)
    except:
        dsrtarget=DistributorSalesRepTarget.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = dsrtarget.target
        report_type1["total_retailers"]=0
        #report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report_type1["total_order_value"]=0
    if flag:
        return Response(report)
    else:
        return report

    
@api_view(['GET'])
def get_web_reports(request,accesstoken,month,year,state,actionlist):
    months={
            'January':1,
            'February':2,
            'March':3,
            'April':4,
            'May':5,
            'June':6,
            'July':7,
            'August':8,
            'September':9,
            'October':10,
            'November':11,
            'December':12
            }
    charts_header={
                "caption": "",#"Visualisation: Accumulated Points",
                #"subCaption": "(Total: 296,006)",
                "description": "",#"This is the description",
                "canvasBgColor": "#eeeeee",
                "xAxisName": "",#"Months",
                "yAxisName": "",#"Numbers",
                "paletteColors": "#eea236",
                "valueFontColor": "#000000",
                "baseFont": "Helvetica Neue,Arial",
                "captionFontSize": "14",
                "subcaptionFontSize": "14",
                "subcaptionFontBold": "0",
                "placeValuesInside": "1",
                "baseFontSize": "12",
                "rotateValues": "0",
                "showShadow": "0",
                "divlineColor": "#999999",
                "divLineIsDashed": "1",
                "divlineThickness": "1",
                "divLineDashLen": "1",
                "divLineGapLen": "1",
                "canvasBgColor": "#ffffff",
                "legendPosition": "bottom"
    }
    actionlist_dict={
            'linebillings':1,
            'newpartsbilled':2,
            'newretailers':3,
            'actual_target':4,
            'associated_retailers':5,
            'topsellingpartqty':6,
            'topsellingpartval':7,
            'totaloutstanding':8,
            'totalcollections':9
            }
    actionlist_key_dict={
            'linebillings':'number_of_line_billings',
            'newpartsbilled':'number_of_new_parts_billed',
            'newretailers':'number_of_new_retailers_registered',
            'actual-target':'',
            'associated-retailers':'',
            'topsellingpartqty':'',#DSR per month
            'topsellingpartval':'',#DSR per month
            'totaloutstanding':'',#Retailer-wise till now
            'totalcollections':'collection_value'#Retailer-wise till now
            }

    user=[]
    #auth_user=.objects.get(token=accesstoken)
    #user_id=auth_user.user.id
    chart={}
    chart['chart']=charts_header
    chart['data']=[]
    data_dict={}       

    ##Authenticate accesstoken and get request.user objects
    if actionlist_dict[actionlist]==4:
        #FIXME:uncomment after merging accesstoken changes
        #status=get_role(user) 
        #FIXME:Remove this after testing
        status={}
        status['message']='pass'
        status['role']=2
        status['Id']=4

        charts_header['yAxisName']='Numbers'
        charts_header['caption']='Targets'
        charts_header['description']='Actuals vs Targets'
        chart['data1']=[]

        if status['message'] == 'pass':
            if status['role']==1:
                charts_header['xAxisName']='NSM'
                if month in months:
                    targets=NsmTarget.objects.filter(active=1,month=months[month],year=year)
                    for nsm in targets:
                        data_dict={}       
                        data1_dict={}
                        data_dict['label']=nsm.nsm.nsm_id#label
                        data_dict['value']=nsm.target
                        data1_dict['label']=nsm.nsm.nsm_id
                        report=get_nsm_reports(nsm.nsm.nsm_id,months[month],year)
                        print report[0]
                        data1_dict['value']=report[0]['total_order_value']
                        chart['data'].append(data_dict)
                        chart['data1'].append(data1_dict)
            if status['role']==2:
                charts_header['xAxisName']='ASM'
                if month in months:
                    targets=AsmTarget.objects.filter(asm__nsm_id=status['Id'],active=1,month=months[month],year=year)
                    for asm in targets:
                        data_dict={}       
                        data1_dict={}
                        data_dict['label']=asm.asm.asm_id#label
                        data_dict['value']=asm.target
                        data1_dict['label']=asm.asm.asm_id
                        report=get_asm_reports(asm.asm.asm_id,months[month],year)
                        print report[0]
                        data1_dict['value']=report[0]['total_order_value']
                        chart['data'].append(data_dict)
                        chart['data1'].append(data1_dict)
                else:
                    chart={
                        'status':0,
                        'message':'Access Denied'
                        }
                    '''
                    for label in months:
                        targets=AsmTarget.objects.get(asm__nsm_id=status['Id'],active=1,year=year,month=months[label])
                        data_dict['label']=label
                        data_dict['value']=targets.target
                        chart['data'].append(data_dict)
                    '''
            if status['role']==3:
                if month in months:
                    targets=DistributorTarget.objects.filter(distributor__asm_id=status['Id'],active=1,month=months[month],year=year)
                    for dstr in targets:
                        data_dict={}       
                        data1_dict={}
                        data_dict['label']=dstr.distributor.distributor_id#label
                        data_dict['value']=dstr.target
                        data1_dict['label']=dstr.distributor.distributor_id#label
                        report=get_distributor_reports(dstr.distributor.distributor_id,months[month],year)
                        print report[0]
                        data1_dict['value']=report[0]['total_order_value']
                        chart['data'].append(data_dict)
                else:
                    chart={
                        'status':0,
                        'message':'Access Denied'
                        }
                    '''
                    for label in months:
                        targets=DistributorTarget.objects.get(distributor__asm_id=status['Id'],active=1,year=year,month=months[label])
                        data_dict['label']=label
                        data_dict['value']=targets.target
                        chart['data'].append(data_dict)
                    '''
            if status['role']==4:
                if month in months:
                    targets=DistributorSalesRepTarget.objects.get(dsr__distributor_id=status['Id'],active=1,month=months[month],year=year)
                    for dsr in targets:
                        data_dict={}       
                        data_dict['label']=dsr.distributor_sales_code
                        data_dict['value']=dsr.target
                        chart['data'].append(data_dict)
                else:
                    chart={
                        'status':0,
                        'message':'Access Denied'
                        }
                    '''
                    for label in months:
                        targets=DistributorSalesRepTarget.objects.get(dsr__distributor_id=status['Id'],active=1,year=year,month=months[label])
                        data_dict['label']=label
                        data_dict['value']=targets.target
                        chart['data'].append(data_dict)

                    '''
    else:
        chart={
                'status':0,
                'message':'Access Denied'
        }

    return Response(chart)

    ret_dict=[]
    if not month:
        for i,j in months:
            ret_dict+=get_retailer_report(request,j,year)
    charts['chart']=charts_header
    #for each data
    charts['data'].append(data_dict)
    print charts


def get_role(user):
    '''
    Pass a user object
    '''
    status={'message':'fail','Id':0,'role':0}
    if user.groups.filter(name=Roles.SFAADMIN).exists() or user.groups.filter(name=Roles.SUPERADMINS).exists():
        #Id = NationalSparesManager.objects.get(user_id=user.id).id
        status={'message':'pass','Id':'','role':1}
        return status
    if user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
        Id = NationalSparesManager.objects.get(user_id=user.id).id
        status={'message':'pass','Id':Id,'role':2}
        return status
    if user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
        Id = AreaSparesManager.objects.get(user_id=user.id).id
        status={'message':'pass','Id':Id,'role':3}
        return status
    if user.groups.filter(name=Roles.DISTRIBUTORS).exists():
        Id = Distributor.objects.get(user_id=user.id).id
        status={'message':'pass','Id':Id,'role':4}
        return status
    return status

@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_reports(request,month,year):
    '''
    Get the reports for Authenticated Users only based on Roles
    Return if month,year is > today
    '''
    if request.user.groups.filter(name=Roles.DISTRIBUTORSALESREP).exists():
        if request.user.is_authenticated():
            dsr_id = DistributorSalesRep.objects.get(user_id=request.user.id).id
            return get_dsr_reports(dsr_id,month,year,flag='api')
        else:
            return Response({'Error':'Not an authenticated user'})

    if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
        try:
            if request.user.is_authenticated():
                distributor_id = Distributor.objects.get(user_id=request.user.id).distributor_id
                return get_distributor_reports(distributor_id,month,year,flag='api')
            else:
                return Response({'Error':'Not an authenticated user'})
        except:
            return Response({'Error':'Distributor object error'})

    if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
        if request.user.is_authenticated():
            asm_id = AreaSparesManager.objects.get(user_id=request.user.id).asm_id
            return get_asm_reports(asm_id,month,year,flag='api')
        else:
            return Response({'Error':'Not an authenticated user'})

    if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
        if request.user.is_authenticated():
            nsm_id = NationalSparesManager.objects.get(user_id=request.user.id).nsm_id
            return get_nsm_reports(nsm_id,month,year,flag='api')
        else:
            return Response({'Error':'Not an authenticated user'})
    #FIXME: Admin Reports visibility should be removed??
    if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
        if request.user.is_authenticated():
            return get_admin_reports(month,year,flag='api')
        else:
            return Response({'Error':'Not an authenticated user'})
    return Response({'Error':'Not an authorized user'})

def save_targets(request):
    '''
    Save the targets in the table 
    '''
    data=request.POST
    targets=data.getlist('targets')
    name=data.getlist('name1')
    code=data.getlist('code1')
    type1=data.get('type1')
    month=data.get('month1')
    year=data.get('year1')
    opts=Retailer._meta
    context={'opts':opts,'app_label':opts.app_label}
    template='admin/bajaj/reports/save-targets.html'
    if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
        try:
            if request.user.is_authenticated():
                try:
                    Distributor.objects.get(user_id=request.user.id)
                except:
                    return HttpResponse('Error in DB')
                #dsrs = DistributorSalesRep.objects.filter(distributor_id=request.user.id)
                #FIXME: Use bulk_create
                dsrtargets_active=DistributorSalesRepTarget.objects.filter(month=month,year=year,active=1)
                for each in dsrtargets_active:
                    each.active=0
                    each.save()
                if(type1==4):
                    for i in range(len(targets)):
                        #dsr_target also has dsr_sales_code
                        target = DistributorSalesRepTarget()
                        target.month = month
                        target.year = year
                        target.active = 1
                        target.target = targets[i]
                        dsr=Distributor.objects.get(distributor_sales_code=code[i])
                        target.dsr = dsr
                        target.save()
                    context.update({'status':'success'})
                    return render(request,template,context) 
                #type 5
                else:
                    rtargets_active=RetailerTarget.objects.filter(month=month,year=year,active=1)
                    for each in rtargets_active:
                        each.active=0
                        each.save()
                    for i in range(len(targets)):
                    #for r_target in targets:
                        #dsr_target also has dsr_sales_code
                        Rtarget = RetailerTarget()
                        Rtarget.month = month
                        Rtarget.year = year
                        Rtarget.active = 1
                        Rtarget.target = targets[i]
                        retailer=Retailer.objects.get(retailer_code=code[i])
                        Rtarget.retailer = retailer
                        Rtarget.save()
                    context.update({'status':'success'})
                    return render(request,template,context) 
            else:
                return HttpResponse('Error, Not an authenticated user')
        except:
            return HttpResponse('error Distributor object error')

    if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
        if request.user.is_authenticated():
            try:
                AreaSparesManager.objects.get(user_id=request.user.id)
            except:
                return Response({'error':'Error in DB'})
            Dtargets_active=DistributorTarget.objects.filter(month=month,year=year,active=1)
            for each in Dtargets_active:
                each.active=0
                each.save()
            for i in range(len(targets)):
                Dtarget = DistributorTarget()
                Dtarget.month = month
                Dtarget.year = year
                Dtarget.active = 1
                Dtarget.target = targets[i]
                distributor=Distributor.objects.get(distributor_id=code[i])
                Dtarget.distributor = distributor
                Dtarget.save()
            context.update({'status':'success'})
            return render(request,template,context) 
        else:
            return HttpResponse('Error, Not an authenticated user')

    if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
        if request.user.is_authenticated():
            try:
                NationalSparesManager.objects.get(user_id=request.user.id)
            except:
                return Response({'error':'Error in DB'})
            asmtargets_active=AsmTarget.objects.filter(month=month,year=year,active=1)
            for each in asmtargets_active:
                each.active=0
                each.save()
            for i in range(len(targets)):
                    Asmtarget = AsmTarget()
                    Asmtarget.month = month
                    Asmtarget.year = year
                    Asmtarget.active = 1
                    Asmtarget.target = targets[i]
                    asm=AreaSparesManager.objects.get(asm_id=code[i])
                    Asmtarget.asm = asm
                    Asmtarget.save()
            context.update({'status':'success'})
            return render(request,template,context) 
        else:
            return HttpResponse('Error, Not an authenticated user')
    if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
        if request.user.is_authenticated():
            nsmtargets_active=NsmTarget.objects.filter(month=month,year=year,active=1)
            for each in nsmtargets_active:
                each.active=0
                each.save()
            for i in range(len(targets)):
                    Nsmtarget = NsmTarget()
                    Nsmtarget.month = month
                    Nsmtarget.year = year
                    Nsmtarget.active = 1
                    Nsmtarget.target = targets[i]
                    nsm=NationalSparesManager.objects.get(nsm_id=code[i])
                    Nsmtarget.nsm = nsm
                    Nsmtarget.save()
            context.update({'status':'success'})
            return render(request,template,context) 
        else:
            return HttpResponse('Error, Not an authenticated user')
    else:
        pass
        
    return HttpResponse('error') 

def add_targets(request):
    '''
    Add Targets view
    '''
    data=request.POST
    month=data.get('month')
    year=data.get('year')
    target_type=data.get('type')
    objs=[]
    context={'objs':'','month':'','year':'','opts':'','app_label':'', 'type':"", 'target':''}

    if request.user.is_authenticated():
        if  target_type=='1': 
            opts=NsmTarget._meta
            nsms=NationalSparesManager.objects.all()
            for nsm in nsms:
                nsm_dict={}
                nsm_dict['name']=nsm.name
                nsm_dict['code']=nsm.nsm_id
                objs.append(nsm_dict)
            context={'objs':objs,'month':month,'year':year,'opts':opts,'app_label':opts.app_label, 'type':"1",'target':'Null'}
        elif  target_type=='2': 
            opts=AsmTarget._meta
            try:
                Id=NationalSparesManager.objects.get(user_id=request.user.id).id
                asms=AreaSparesManager.objects.filter(nsm_id=Id)
                try:
                    target=NsmTarget.objects.get(month=month,year=year,active=1).target
                except:
                    target='Null'
            except:
                pass
                '''
                #Admin accessing page
                asms=AreaSparesManager.objects.all()
                target='Null'
                '''
            for asm in asms:
                asm_dict={}
                asm_dict['name']=asm.name
                asm_dict['code']=asm.asm_id
                objs.append(asm_dict)
            context={'objs':objs,'month':month,'year':year,'opts':opts,'app_label':opts.app_label, 'type':"2", 'target':target}
        elif  target_type=='3': 
            opts=DistributorTarget._meta
            try:
                Id=AreaSparesManager.objects.get(user_id=request.user.id).id
                distributors=Distributor.objects.filter(asm_id=Id)
                try:
                    target=AsmTarget.objects.get(month=month,year=year,active=1).target
                except:
                    target='Null'
            except:
                pass
                '''
                #Admin accessing page
                distributors=Distributor.objects.all()
                target='Null'
                '''
            for distributor in distributors:
                distributor_dict={}
                distributor_dict['name']=distributor.name
                distributor_dict['code']=distributor.distributor_id
                objs.append(distributor_dict)
            context={'objs':objs,'month':month,'year':year,'opts':opts,'app_label':opts.app_label, 'type':"3", 'target':target}
        elif  target_type=='4': 
            opts=DistributorSalesRepTarget._meta
            try:
                Id=Distributor.objects.get(user_id=request.user.id).id
                dsrs=DistributorSalesRep.objects.filter(distributor_id=Id)
                #Do not send target as Distributor's target is staggered with both dsr and retailer
                target='Null'
            except:
                pass
                '''
                #Admin accessing page
                dsrs=DistributorSalesRep.objects.all()
                target='Null'
                '''
            for dsr in dsrs:
                dsr_dict={}
                dsr_dict['name']=dsr.user_id
                dsr_dict['code']=dsr.distributor_sales_code
                objs.append(dsr_dict)
            context={'objs':objs,'month':month,'year':year,'opts':opts,'app_label':opts.app_label, 'type':"4", 'target':target}
        elif target_type=='5':
            opts=Retailer._meta
            try:
                Id=Distributor.objects.get(user_id=request.user.id).id
                retailers=Retailer.objects.filter(distributor_id=Id)
                #Do not send target as Distributor's target is staggered with both dsr and retailer
                target='Null'
            except:
                pass
                '''
                #Admin accessing page
                retailers=Retailer.objects.all()
                target='Null'
                '''
            for retailer in retailers:
                retailer_dict={}
                retailer_dict['name']=retailer.retailer_name
                retailer_dict['code']=retailer.retailer_code
                objs.append(retailer_dict)
            context={'objs':objs,'month':month,'year':year,'opts':opts,'app_label':opts.app_label, 'type':"5", 'target':target}
    else:
        return HttpResponse('errorNot an authenticated user')
    ''' 
    if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
        try:
            if request.user.is_authenticated():
                try:
                    Id=Distributor.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'Error in DB'})
                retailers = Retailers.objects.filter(distributor_id=Id)
                for retailer in retailers:
                    #dsr_target also has dsr_sales_code
                    retailer_dict={}
                    retailer_dict['name']=retailer.retailer_name
                    retailer_dict['code']=retailer.retailer_code
                    objs.append(retailer_dict)
                dsrs = DistributorSalesRep.objects.filter(distributor_id=Id)
                objs2=[]
                for dsr in dsrs:
                    dsr_dict={}
                    #FIXME: give appropriate name
                    dsr_dict['name']=dsr.user_id
                    dsr_dict['code']=dsr.distributor_sales_code
                    objs2.append(dsr_dict)
                print objs
                print objs2
                context={'objs':objs,'month':data.get('month'),'year':data.get('year'),'opts':opts,'app_label':opts.app_label, 'type':"4",'objs2':objs2}
            else:
                return Response({'error':'Not an authenticated user'})
        except:
            return Response({'error':'Distributor object error'})

    if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
        if request.user.is_authenticated():
            try:
                Id=AreaSparesManager.objects.get(user_id=request.user.id).id
            except:
                return Response({'error':'Error in DB'})
            distributors=Distributor.objects.filter(asm_id=Id)
            for distributor in distributors:
                distributor_dict={}
                distributor_dict['name']=distributor.name
                distributor_dict['code']=distributor.distributor_id
                objs.append(distributor_dict)
            print objs
            context={'objs':objs,'month':data.get('month'),'year':data.get('year'),'opts':opts,'app_label':opts.app_label, 'type':"3"}
        else:
            return Response({'error':'Not an authenticated user'})

    if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
        if request.user.is_authenticated():
            try:
                Id=NationalSparesManager.objects.get(user_id=request.user.id).id
            except:
                return Response({'error':'Error in DB'})
            asms=AreaSparesManager.objects.filter(nsm_id=Id)
            for asm in asms:
                asm_dict={}
                asm_dict['name']=asm.name
                asm_dict['code']=asm.asm_id
                objs.append(asm_dict)
            print objs
            context={'objs':objs,'month':data.get('month'),'year':data.get('year'),'opts':opts,'app_label':opts.app_label, 'type':"2"}
        else:
            return Response({'error':'Not an authenticated user'})
    #FIXME: Admin Reports visibility should be removed
    if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
        if request.user.is_authenticated():
            opts=NsmTarget._meta
            nsms=NationalSparesManager.objects.all()
            for nsm in nsms:
                nsm_dict={}
                nsm_dict['name']=nsm.name
                nsm_dict['code']=nsm.nsm_id
                objs.append(nsm_dict)
            print objs
            context={'objs':objs,'month':data.get('month'),'year':data.get('year'),'opts':opts,'app_label':opts.app_label, 'type':"1"}
        else:
            return Response({'error':'Not an authenticated user'})
    else:
        pass
        ##FIXME: Added this to test with 
        #if request.user.is_authenticated():
            #return get_nsm_reports(request,month,year)
            #FIXME:Admin reports visibility should be removed
           # return get_admin_reports(request,month,year)
        #else:
        #    return Response({'error':'Not an authenticated user'})
    '''
    template='admin/bajaj/reports/add-targets.html'
    return render(request,template,context)
  


