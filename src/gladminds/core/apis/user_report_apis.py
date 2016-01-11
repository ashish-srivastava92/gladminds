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

from gladminds.bajaj.models import RetailerTarget,DistributorTarget,AsmTarget,NsmTarget
from gladminds.bajaj.models import DistributorSalesRepTarget
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gladminds.core.auth_helper import Roles
from gladminds.core import constants
from gladminds.bajaj.models import DistributorSalesRep, Retailer,PartModels, Categories, \
                            PartPricing, Distributor,  Invoices, \
                            Collection,CollectionDetails,PartsStock,DSRWorkAllocation,DSRLocationDetails, \
                            NationalSparesManager,AreaSparesManager
from gladminds.bajaj.models import PartMasterCv,OrderPart,OrderPartDetails, \
                        PartIndexDetails, PartIndexPlates, FocusedPart

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


def get_retailer_report(retailer):
   retailer_report={}
   retailer_report["report_type"] = "month"
   try:
       retailer_target = RetailerTarget.object.filter(retailer=retailer,month=month,year=year)
       retailer_report["retailer_id"] = retailer.retailer_code
       retailer_report["target_per_month"] = retailer_target.month
       #Get the actual order
       retailer_order_value = 0
       orders = OrderPart.objects.filter(retailer=retailer, created_date__month=month, created_date__year=year)
       if orders:
           for order in orders:
                order_details=OrderPartDetails.objects.filter(order=order)
                for order_detail in order_details:
                    retailer_order_value += order_detail.line_total
           retailer_report["Actual"] = retailer_order_value
           total_order_value += retailer_order_value
           retailer_report["number_of_line_billings"] = retailer.total_sale_parts
           retailer_report["order_value"] = ""
           retailer_report["collection_value"] = ""
       else:
           retailer_report["Actual"] = 0
           retailer_report["number_of_line_billings"] = 0
           retailer_report["order_value"] = 0
           retailer_report["collection_value"] = 0
   except:
        #retailer_report['Error']= "Error"
        retailer_report["Actual"] = 0
        retailer_report["number_of_line_billings"] = 0
        retailer_report["order_value"] = 0
        retailer_report["collection_value"] = 0
   return retailer_report

@api_view(['GET'])
def get_admin_reports(request,month,year):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
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
                        newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year).count()
                        orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
                        #New parts billed
                        for order in orderpart:
                            orderpartdetails=OrderPartDetails.objects.filter(order=order,created_date__month=month,created_date__year=year).count()
                            new_parts_billed += orderpartdetails
                        #Monthly Report
                        for retailer in retailers:
                           retailer_report = get_retailer_report(retailer)
                           total_order_value += retailer_report['order_value']
                           report.append(retailer_report)
        report_type1={}
        report_type1["target"] = "NA"
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except:
        report_type1={}
        report_type1["target"] = "NA"
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    return Response(report)

     
@api_view(['GET'])
def get_nsm_reports(request,nsm_id,month,year):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
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
                    newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year).count()
                    orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
                    #New parts billed
                    for order in orderpart:
                        orderpartdetails=OrderPartDetails.objects.filter(order=order,created_date__month=month,created_date__year=year).count()
                        new_parts_billed += orderpartdetails
                    #Monthly Report
                    for retailer in retailers:
                       retailer_report = get_retailer_report(retailer)
                       total_order_value += retailer_report['order_value']
                       report.append(retailer_report)
        report_type1={}
        nsmtarget=NsmTarget.objects.filter(nsm_id=nsm_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = nsmtarget.target
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except:
        report_type1={}
        nsmtarget=NsmTarget.objects.filter(nsm_id=nsm_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = nsmtarget.target
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    return Response(report)

@api_view(['GET'])
def get_asm_reports(request,asm_id,month,year):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
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
                newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year).count()
                orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
                #New parts billed
                for order in orderpart:
                    orderpartdetails=OrderPartDetails.objects.filter(order=order,created_date__month=month,created_date__year=year).count()
                    new_parts_billed += orderpartdetails
                #Monthly Report
                for retailer in retailers:
                   retailer_report = get_retailer_report(retailer)
                   total_order_value += retailer_report['order_value']
                   report.append(retailer_report)
        report_type1={}
        asmtarget=AsmTarget.objects.filter(asm_id=asm_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = asmtarget.target
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except:
        report_type1={}
        asmtarget=AsmTarget.objects.filter(asm_id=asm_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = asmtarget.target
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    return Response(report)

@api_view(['GET'])
def get_distributor_reports(request,distributor_id,month,year):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
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
            newretailers+=Retailer.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year).count()
            orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
            #New parts billed
            for order in orderpart:
                orderpartdetails=OrderPartDetails.objects.filter(order=order,created_date__month=month,created_date__year=year).count()
                new_parts_billed += orderpartdetails
            #Monthly Report
            for retailer in retailers:
               retailer_report = get_retailer_report(retailer)
               total_order_value += retailer_report['order_value']
               report.append(retailer_report)
        report_type1={}
        distributortarget=DistributorTarget.objects.filter(distributor__distributor_id=distributor_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = distributortarget.target
        report_type1["total_order_value"] = total_order_value
        report_type1["total_retailers"] = retailer_count
        report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report[0].update(report_type1)
    except:
        report_type1={}
        distributortarget=DistributorTarget.objects.filter(distributor__distributor_id=distributor_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = distributortarget.target
        report_type1["total_order_value"]=0
        report_type1["total_retailers"]=0
        report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report[0].update(report_type1)
    return Response(report)

@api_view(['GET'])
def get_dsr_reports(request,dsr_id,month,year):
    report=[]
    report_type1={}
    report_type1["report_type"] = "month"
    report.append(report_type1)
    try:
        retailer=Retailer.objects.filter(dsr_id=dsr_id)
        ##FIXME:Can use len()
        retailer_count=Retailer.objects.filter(dsr_id=dsr_id).count()
        newretailers=Retailer.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year).count()
        orderpart=OrderPart.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
        new_parts_billed=0
        #New parts billed
        for order in orderpart:
            orderpartdetails=OrderPartDetails.objects.filter(order=order,created_date__month=month,created_date__year=year).count()
            new_parts_billed += orderpartdetails
        total_order_value = 0
        #Monthly Report
        for retailer in retailers:
           retailer_report = get_retailer_report(retailer)
           total_order_value += retailer_report['order_value']
           report.append(retailer_report)
        report_type1={}
        dsrtarget=DistributorSalesRepTarget.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = dsrtarget.target
        report_type1["total_retailers"] = retailer_count
        report_type1["number_of_new_parts_billed"] = new_parts_billed
        report_type1["number_of_new_retailers_registered"] = newretailers
        report_type1["total_order_value"] = total_order_value
        report[0].update(report_type1)
    except:
        dsrtarget=DistributorSalesRepTarget.objects.filter(dsr_id=dsr_id,created_date__month=month,created_date__year=year)
        report_type1["target"] = dsrtarget.target
        report_type1["total_retailers"]=0
        report_type1["number_of_new_parts_billed"]=0
        report_type1["number_of_new_retailers_registered"]=0
        report_type1["total_order_value"]=0
    return Response(report)

    
@api_view(['GET'])
# # @authentication_classes((JSONWebTokenAuthentication,))
# # @permission_classes((IsAuthenticated,))
def get_reports(request,month,year):
    '''
    Get the reports for Authenticated Users only based on Roles
    '''
    print request.user.groups.all()
    #month=request.GET.__getitem__('month')
    #year=request.GET.__getitem__('year')
    if request.user.groups.filter(name=Roles.DISTRIBUTORSALESREP).exists():
        if request.user.is_authenticated():
            dsr_id = DistributorSalesRep.objects.get(user_id=request.user.id).id
            return get_dsr_reports(request, dsr_id,month,year)
        else:
            return Response({'error':'Not an authenticated user'})

    if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
        try:
            if request.user.is_authenticated():
                distributor_id = Distributor.objects.get(user_id=request.user.id).distributor_id
                return get_distributor_reports(request, distributor_id,month,year)
            else:
                return Response({'error':'Not an authenticated user'})
        except:
            return Response({'error':'Distributor object error'})

    if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
        if request.user.is_authenticated():
            dsr_id = AreaSparesManager.objects.get(user_id=request.user.id).asm_id
            return get_asm_reports(request, asm_id,month,year)
        else:
            return Response({'error':'Not an authenticated user'})

    if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
        if request.user.is_authenticated():
            nsm_id = NationalSparesManager.objects.get(user_id=request.user.id).nsm_id
            return get_nsm_reports(request, nsm_id,month,year)
        else:
            return Response({'error':'Not an authenticated user'})

    if request.user.groups.filter(name=Roles.SFAADMIN).exists():
        if request.user.is_authenticated():
            #return Response({'month':month,'year':year})
            return get_admin_reports(request,month,year)
        else:
            return Response({'error':'Not an authenticated user'})
    else:
        ##FIXME: Added this to test with 
        if request.user.is_authenticated():
            #return get_nsm_reports(request,month,year)
            #FIXME:Admin reports visibility should be removed
            return get_admin_reports(request,month,year)
        else:
            return Response({'error':'Not an authenticated user'})
    return Response({'error':'error'}) 

