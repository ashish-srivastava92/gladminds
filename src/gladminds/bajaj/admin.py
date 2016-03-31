import datetime, logging
from django import forms
from django.contrib.admin import AdminSite, TabularInline
from django.contrib.auth.models import User, Group
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList, ORDER_VAR
from django.contrib.admin import DateFieldListFilter
from django import forms
from django.utils.html import mark_safe
from operator import itemgetter

from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
    AdminPasswordChangeForm)

from gladminds.bajaj import models
from gladminds.bajaj.models import Distributor, DistributorStaff, DistributorSalesRep, DSRWorkAllocation, \
                        Retailer, UserProfile, District, \
                         SparePartPoint, State, AreaSparesManager, City, OrderPartDetails, OrderDeliveredHistory, \
                          Collection, PartsStock, OrderPart, NationalSparesManager, DSRLocationDetails, CollectionDetails,\
                          Invoices,DoDetails, PermanentJourneyPlan, PartIndexDetails, SFAReports,SFAHighlights,\
                          NsmTarget,AsmTarget,DistributorTarget,DistributorSalesRepTarget,RetailerTarget
from gladminds.core.model_fetcher import get_model
from gladminds.core.services.loyalty.loyalty import loyalty
from gladminds.core import utils
from gladminds.core.auth_helper import GmApps, Roles
from gladminds.core.admin_helper import GmModelAdmin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.conf import settings
from gladminds.core.auth_helper import Roles
from gladminds.core import constants
from django.forms.widgets import TextInput
from gladminds.core.managers.mail import send_email


from django.shortcuts import render
from django.conf.urls import patterns, url, include
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.db.models import Sum, Count
from django.contrib import messages
from src.gladminds.bajaj.models import RecentOrder
from rest_framework.response import Response
from django.forms import ModelForm
from suit.widgets import SuitDateWidget
from django.http import HttpResponseRedirect

logger = logging.getLogger('gladminds')
global district_list
PROFILE_CHOICES = (
        ('distributor', 'Wholesale Distributors'),
    )

from django.contrib import admin



class BajajAdminSite(AdminSite):
    pass




class ZonalServiceManagerAdmin(GmModelAdmin):
    search_fields = ('zsm_id',)
    list_display = ('zsm_id', 'get_user', 'get_profile_number', 'regional_office')
    
class AreaServiceManagerAdmin(GmModelAdmin):
    search_fields = ('asm_id', 'zsm__zsm_id')
    list_display = ('asm_id', 'get_user', 'get_profile_number', 'get_profile_address', 'area', 'zsm')
    
class AreaSalesManagerAdmin(GmModelAdmin):
    search_fields = ('state__state_name', 'rm__region')
    list_display = ('get_user', 'get_profile_number', 'get_state')
    
class DealerAdmin(GmModelAdmin):
    search_fields = ('dealer_id', 'asm__asm_id')
    list_display = ('dealer_id', 'get_user', 'get_profile_number', 'get_profile_address', 'asm', 'sm')

class AuthorizedServiceCenterAdmin(GmModelAdmin):
    search_fields = ('asc_id', 'dealer__dealer_id')
    list_display = ('asc_id', 'get_user', 'get_profile_number', 'get_profile_address', 'dealer', 'asm')

class ServiceAdvisorAdmin(GmModelAdmin):
    search_fields = ('service_advisor_id', 'dealer__dealer_id', 'asc__asc_id')
    list_display = ('service_advisor_id', 'get_user', 'get_profile_number', 'get_profile_address', 'dealer', 'asc', 'status')

class BrandProductCategoryAdmin(GmModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'description')

class ProductTypeAdmin(GmModelAdmin):
    search_fields = ('product_type',)
    list_display = ('id', 'product_type', \
                    'image_url', 'is_active')

class DispatchedProduct(models.ProductData):

    class Meta:
        proxy = True

class ListDispatchedProduct(GmModelAdmin):
    search_fields = ('product_id', 'dealer_id__dealer_id')
    list_display = (
        'product_id', 'sku_code', 'engine', 'UCN', 'dealer_id', "invoice_date")
    list_per_page = 50

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        utils.get_search_query_params(request, self)
        query_set = self.model._default_manager.get_query_set()
        query_set = query_set.select_related('').prefetch_related('dealer_id', 'product_type')

        return query_set

    def UCN(self, obj):
        coupons = models.CouponData.objects.filter(product=obj.id)
        if coupons:
            return ' | '.join([str(ucn.unique_service_coupon) for ucn in coupons])
        else:
            return None
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ListDispatchedProduct, self).get_form(request, obj, **kwargs)
        return form

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Product Id' : 'product_id',
                                 'Dealer Id': 'dealer_id__dealer_id', }
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping
                        }
        return super(ListDispatchedProduct, self).changelist_view(request, extra_context=extra_context)


class Couponline(TabularInline):
    model = models.CouponData
    fields = ('unique_service_coupon', 'service_type', 'status', 'mark_expired_on', 'extended_date')
    extra = 0
    max_num = 0
    readonly_fields = ('unique_service_coupon', 'service_type', 'status', 'mark_expired_on', 'extended_date')


class ProductDataAdmin(GmModelAdmin):
    search_fields = ('product_id', 'customer_id', 'customer_phone_number',
                     'customer_name')
    list_display = ('product_id', 'customer_id', "UCN", 'customer_name',
                    'customer_phone_number', 'purchase_date')
    inlines = (Couponline,)
    list_per_page = 50

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        utils.get_search_query_params(request, self)
        query_set = self.model._default_manager.get_query_set()
        query_set = query_set.select_related('')
        query_set = query_set.filter(purchase_date__isnull=False)
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set

    def UCN(self, obj):
        coupons = models.CouponData.objects.filter(product=obj.id)
        if coupons:
            return ' | '.join([str(ucn.unique_service_coupon) for ucn in coupons])
        else:
            return None

    def service_type(self, obj):
        gm_coupon_data_obj = models.CouponData.objects.filter(product=obj.id)
        coupon_service_type = ''
        if gm_coupon_data_obj:
            coupon_service_type = " | ".join(
                [str(obj.service_type) for obj in gm_coupon_data_obj])
        return coupon_service_type
    
    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Product Id' : 'product_id',
                                 'Customer ID':'customer_id',
                                 'Customer Name': 'customer_name',
                                 'Customer Phone Number': 'customer_phone_number'}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping
                        }
        return super(ProductDataAdmin, self).changelist_view(request, extra_context=extra_context)


class CouponAdmin(GmModelAdmin):
    search_fields = (
        'unique_service_coupon', 'product__product_id', 'status')
    list_display = ('product', 'unique_service_coupon', 'actual_service_date',
                    'actual_kms', 'status', 'service_type', 'service_advisor', 'associated_with')
    exclude = ('order',)

    def suit_row_attributes(self, obj):
        class_map = {
            '1': 'success',
            '2': 'warning',
            '3': 'error',
            '4': 'info',
            '5': 'error',
            '6': 'warning'
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}
    
    def associated_with(self, obj):
        if obj.service_advisor:
            sa = models.ServiceAdvisor.objects.filter(service_advisor_id=obj.service_advisor.service_advisor_id).select_related('dealer', 'authorizedservicecenter')[0]
            if sa.dealer:
                return sa.dealer.dealer_id + ' (D)'
            elif sa.asc:
                return sa.asc.asc_id + ' (A)'
            else:
                return None

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Unique Service Coupon' : 'unique_service_coupon',
                                 'Product Id': 'product__product_id',
                                 'Status': 'status'}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping, 'created_date_search': True
                        }
        return super(CouponAdmin, self).changelist_view(request, extra_context=extra_context)

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        if utils.get_search_query_params(request, self) and self.search_fields[0] == 'status':
            try:
                request.GET = request.GET.copy()
                search_value = str(constants.COUPON_STATUS[request.GET["q"].title()])
                request.GET["q"] = search_value
                request.META['QUERY_STRING'] = search_value
            except Exception:
                pass
        qs = self.model._default_manager.get_query_set()
        qs = qs.select_related('').prefetch_related('product')
        '''
            This if condition only for landing page
        '''
        if not request.GET.has_key('q') and not request.GET.has_key('_changelist_filters'):
            qs = qs.filter(status=4)
        return qs

    def get_changelist(self, request, **kwargs):
        return CouponChangeList

class CouponChangeList(ChangeList):

    def get_ordering(self, request, queryset):
        '''
            This remove default ordering of django admin
            default ordering of django admin is primary key
        '''
        params = self.params
        ordering = list(self.model_admin.get_ordering(request)
                        or self._get_default_ordering())

        if ORDER_VAR in params:
            # Clear ordering and used params
            ordering = []
            order_params = params[ORDER_VAR].split('.')
            for p in order_params:
                try:
                    none, pfx, idx = p.rpartition('-')
                    field_name = self.list_display[int(idx)]
                    order_field = self.get_ordering_field(field_name)
                    if not order_field:
                        continue  # No 'admin_order_field', skip it
                    ordering.append(pfx + order_field)
                except (IndexError, ValueError):
                    continue  # Invalid ordering specified, skip it.

        ordering.extend(queryset.query.order_by)

        return ordering

class SMSLogAdmin(GmModelAdmin):
    search_fields = ('sender', 'receiver', 'action')
    list_display = (
        'created_date', 'action', 'message', 'sender', 'receiver')
    
    def suit_row_attributes(self, obj):
        class_map = {
            'success': 'success',
            'failed': 'error',
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}
    
    def action(self, obj):
        return obj.action
    
    def has_add_permission(self, request):
        return False
    
class EmailLogAdmin(GmModelAdmin):
    search_fields = ('subject', 'sender', 'receiver')
    list_display = (
        'created_date', 'subject', 'message', 'sender', 'receiver', 'cc')

class FeedLogAdmin(GmModelAdmin):
    search_fields = ('status', 'data_feed_id', 'feed_type', 'action')
    list_display = ('timestamp', 'feed_type', 'action',
                    'total_data_count', 'success_data_count',
                    'failed_data_count', 'feed_remarks')

    def feed_remarks(self, obj):
        if obj.file_location:
            update_remark = ''
            update_remark = u'<a href="{0}" target="_blank">{1}</a>'.\
                                            format(obj.file_location, " Click for details")
            return update_remark
    feed_remarks.allow_tags = True

    def has_add_permission(self, request):
        return False

    def suit_row_attributes(self, obj):
        class_map = {
            'success': 'success',
            'failed': 'error',
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}
    
    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.CTSADMIN).exists():
            query_set = query_set.filter(feed_type__in=['ContainerTracker Feed', 'CTS Feed'])
        return query_set
        
    def changelist_view(self, request, extra_context=None):
        extra_context = {'created_date_search': True
                        }
        return super(FeedLogAdmin, self).changelist_view(request, extra_context=extra_context)

class ASCTempRegistrationAdmin(GmModelAdmin):
    search_fields = (
        'name', 'phone_number', 'email', 'dealer_id')

    list_display = (
        'name', 'phone_number', 'email', 'pincode',
        'address', 'timestamp', 'dealer_id')

class SATempRegistrationAdmin(GmModelAdmin):
    search_fields = (
        'name', 'phone_number')

    list_display = (
        'name', 'phone_number', 'status')

class CustomerTempRegistrationAdmin(GmModelAdmin):
    search_fields = (
        'product_data__product_id', 'new_customer_name', 'new_number', 'temp_customer_id', 'sent_to_sap')

    list_display = (
        'temp_customer_id', 'product_data', 'new_customer_name', 'new_number',
        'product_purchase_date', 'sent_to_sap', 'remarks')

    def suit_row_attributes(self, obj):
        class_map = {
            '1': 'success',
            '0': 'error'
        }
        css_class = class_map.get(str(obj.sent_to_sap))
        if css_class:
            return {'class': css_class}
        
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('product_data',)
        form = super(CustomerTempRegistrationAdmin, self).get_form(request, obj, **kwargs)
        return form

class MessageTemplateAdmin(GmModelAdmin):
    search_fields = ('template_key', 'template')
    list_display = ('template_key', 'template', 'description')

class EmailTemplateAdmin(GmModelAdmin):
    search_fields = ('template_key', 'sender', 'receiver', 'subject')
    list_display = ('template_key', 'sender', 'receivers', 'subject')

    def receivers(self, obj):
        return ' | '.join(obj.receiver.split(','))

class SlaAdmin(GmModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
        'priority', ('response_time', 'response_unit'),
        ('reminder_time', 'reminder_unit'),
        ('resolution_time', 'resolution_unit'))
        }),
        )
    def response_time(self):
        return str(self.response_time) + ' ' + self.response_unit
    
    def reminder_time(self):
        return str(self.reminder_time) + ' ' + self.reminder_unit
    
    def resolution_time(self):
        return str(self.resolution_time) + ' ' + self.resolution_unit
    
    list_display = ('priority', response_time, reminder_time, resolution_time)

class ServiceAdmin(GmModelAdmin):
    list_display = ('service_type', 'name', 'description')
    readonly_fields = ('file_tag',)

class ServiceDeskUserAdmin(GmModelAdmin):
    list_display = ('user_profile', 'name', 'phone_number', 'email')


# UserProfile

# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     
    
# class NSMAdminInline(admin.StackedInline):
#     model = NationalSparesManager
#     groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
#     search_fields = ('nsm_id', 'name', 'phone_number')
#     list_display = ('nsm_id', 'name', 'email', 'phone_number', 'get_territory')

# class AuthorAdmin(admin.ModelAdmin):
#     inlines = [
#         BookInline,
#     ]    

class UserProfileAdmin(GmModelAdmin):
    search_fields = ('user__username', 'phone_number',)
    list_display = ('user', 'phone_number', 'status', 'address',
                    'state', 'country', 'pincode', 'date_of_birth', 'gender')
    readonly_fields = ('image_tag',)
    
#     inlines = [
#         NSMAdminInline,
#     ]
#     


'''Admin View for loyalty'''
class NSMAdmin(GmModelAdmin):
#     UserAdmin()
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    add_form = UserCreationForm
    search_fields = ('nsm_id', 'name', 'phone_number')
    list_display = ('nsm_id', 'names', 'emailid', 'phone', 'get_territory')
#                     'user_email','username', 'email', 'first_name', 'last_name', 'is_staff')

        
    def nsm(self, obj):
       
        return obj.nsm_id
    nsm.short_description = 'NSM ID'
    
    
    def emailid(self, obj):
        return obj.email
    emailid.short_description = 'Email ID'
      
    def phone(self, obj):
        if obj.phone_number:
            if obj.phone_number[0:3] == "+91":
                obj.phone_number = obj.phone_number[3:]
            else:
                obj.phone_number
            return obj.phone_number
        return "NA"
    phone.short_description = 'Mobile No'
   
    def names(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    names.short_description = 'Name'

    def get_territory(self, obj):
        territories = obj.territory.all()
        if territories:
            return ' | '.join([str(territory.territory) for territory in territories])
        else:
            return None
    get_territory.short_description = 'Territory'

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('nsm_id',)
        form = super(NSMAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.phone_number = utils.mobile_format(obj.phone_number)
        super(NSMAdmin, self).save_model(request, obj, form, change)



class ASMAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('asm_id', 'nsm__name',
                     'phone_number', 'state')
    list_display = ('asm_id', 'names', 'emailid',
                     'phone', 'get_state', 'nsm')
    
    
    def asm(self, obj):
        return obj.asm_id
    asm.short_description = 'ASM ID'
    
    
    def phone(self, obj):
        if obj.phone_number:
            if obj.phone_number[0:3] == "+91":
                obj.phone_number = obj.phone_number[3:]
            else:
                obj.phone_number
            return obj.phone_number
        return "NA"
    phone.short_description = 'Mobile No'
    
    
    def emailid(self, obj):
        return obj.email
    emailid.short_description = 'Email ID'
        
    def names(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    names.short_description = 'Name'
    
    def get_state(self, obj):
        states = obj.state.all()
        if states:
            return ' | '.join([str(state.state_name) for state in states])
        else:
            return None
    get_state.short_description = 'State'

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('asm_id',)
        form = super(ASMAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.phone_number = utils.mobile_format(obj.phone_number)
        super(ASMAdmin, self).save_model(request, obj, form, change)
        
class NationalSalesManagerAdmin(GmModelAdmin):
    search_fields = ('name', 'phone_number')
    list_display = ('name', 'email', 'phone_number', 'get_territory')

    def get_territory(self, obj):
        territories = obj.territory.all()
        if territories:
            return ' | '.join([str(territory.territory) for territory in territories])
        else:
            return None
    get_territory.short_description = 'Territory'
    
    def save_model(self, request, obj, form, change):
        obj.phone_number = utils.mobile_format(obj.phone_number)
        super(NationalSalesManagerAdmin, self).save_model(request, obj, form, change)
     

         
class DistributorForm(forms.ModelForm):
#     distributor_id = forms.CharField(max_length=30,required=True)
    name = forms.CharField(label='Name of Distributorship', max_length=300)
    last_name = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=40, label='First Name', required=False)
    mobile1 = forms.CharField(max_length=15)
    mobile2 = forms.CharField(max_length=15)
    email = forms.CharField(max_length=50, required=False, label="Email")
    email_bajaj = forms.CharField(max_length=50)
    date_birth = forms.DateTimeField(label='Date of birth', required=False)
    profile = forms.ChoiceField(choices=PROFILE_CHOICES, required=True)
    image_tag = forms.FileField(max_length=200, required=False)
    plot_no = forms.CharField(max_length=20)
    street_name = forms.CharField(max_length=30)
    locality = forms.CharField(max_length=30)
    city = forms.CharField(max_length=20)
    pincode = forms.CharField(max_length=15, required=False)
    phone_number = forms.CharField(max_length=15, label='Phone (Land line)')
    tin = forms.IntegerField()
    cst = forms.IntegerField()
    states = State.objects.all()
    states = forms.ChoiceField(choices=((st.state_code, st.state_name) for st in states),label="State")
#     DISTRICTS = (
#    
# )
    district = District.objects.all()
    districts = forms.MultipleChoiceField(required=True, choices=((dt.id, dt.name) for dt in district))
    is_active = forms.BooleanField(required=False)
    
    def image_tag(self):
        return u'<img src="{0}/{1}" width="200px;"/>'.format('/static', self.image_tag)
    image_tag.short_description = 'User Image'
    image_tag.allow_tags = True
    
    class Meta:
        model = Distributor
#         exclude = ['sent_to_sap', 'phone_number', 'profile', 'language', 'territory']

    
class DistributorAdmin(GmModelAdmin):
    class Media:
        js = ['js/user.js']

    groups_update_not_allowed = [Roles.NATIONALSPARESMANAGERS]
    form = DistributorForm
    search_fields = ('name', 'email',)
    list_display = ('distributor_code', 'distributor_name', 'head', 'locality', 'phone',
                    'Email')
    
    fieldsets = (
            ('User Information', {
              'fields': ('user', 'asm', 'distributor_id', 'name', ['first_name'], ['last_name'], ['email'], 'mobile1',
                'mobile2', 'email_bajaj', 'date_birth', 'profile', 'image_url', 'is_active')
            }),
            ('Location', {
              'fields': ('plot_no', 'locality', 'phone_number', 'street_name', 'city',
               ['pincode'])
            }),
            ('Territory', {
              'fields': ('state', 'districts', 'tin', 'cst')
            }),
          )
   
#     readonly_fields = ('image_tag',)
    
    
    def is_active(self, obj):
        return obj.is_active
    
    
    def name(self, obj):
            return obj.name
    name.short_description = 'Last Name'
        
    
    def lastname(self, obj):
        if obj.user:
            return obj.user.user.last_name
        return None
    lastname.short_description = 'Last Name'
    
    def pincode(self, obj):
        if obj.user:
            return obj.user.pincode
        return None
    pincode.short_description = 'PinCode'
    
    
    
    def Email(self, obj):
        if obj.user:
            return obj.user.user.email
        return None
    Email.short_description = 'Email'
    
    
    def email(self, obj):
        if obj.user:
            return obj.user.user.email
            
    
    def first_name(self, obj):
        if obj.user:
          return obj.user.user.first_name
        return None
    first_name.short_description = 'First Name'
    
        
    def distributor_code(self, obj):

        return obj.distributor_id
    distributor_code.admin_order_field = 'distributor_id'
    
    def distributor_name(self, obj):

        return obj.name
    distributor_name.short_description = 'Name of Distributorship'
    
    def head(self, obj):
        if obj.user:
            return obj.user.user.first_name
        return None

    head.short_description = 'Distributor Head'
    
    def locality(self, obj):

        return obj.city
    locality.short_description = 'locality'
    
    def phone(self, obj):
        if obj.phone_number:
            if obj.phone_number[0:3] == "+91":
                phone_number = obj.phone_number[3:]
    #             print obj.phone_number[3:]
            else:
                phone_number = obj.phone_number
            return phone_number
        else:
            return "NA"
        
    phone.short_description = 'Phone/ Mobile'


    
    def staff_status(self, obj):
        if obj.user.user.is_staff == True:
            return '<html><img src = /static/img/active.gif></html>'
        else:
            return '<html><img src = /static/img/not_active.gif></html>'
    staff_status.allow_tags = True
    


    def get_form(self, request, obj=None, **kwargs):
        form = super(DistributorAdmin, self).get_form(request, obj, **kwargs)
        if request.method == "GET" and obj is not None:

            dist_obj = Distributor.objects.get(distributor_id=obj.distributor_id)
            first_name = dist_obj.user.user.first_name
            last_name = dist_obj.user.user.last_name
            email = dist_obj.user.user.email
            dob = dist_obj.user.date_of_birth
            pincode = dist_obj.user.pincode
            active = dist_obj.user.user.is_active
            district_list = []
            form.base_fields['user'].initial = first_name
            form.base_fields['first_name'].initial = first_name
            form.base_fields['last_name'].initial = last_name
            form.base_fields['email'].initial = email
            form.base_fields['pincode'].initial = pincode
            form.base_fields['date_birth'].initial = dob
            form.base_fields['plot_no'].initial = dist_obj.address_line_2
            form.base_fields['locality'].initial = dist_obj.address_line_3
            form.base_fields['street_name'].initial = dist_obj.address_line_4
            form.base_fields['districts'].initial = district_list
            form.base_fields['is_active'].initial = active
#             form.base_fields['districts'].initial = district_list
#             districts = district_list
        return form
        

        if obj is not None and request.POST:

            dist = request.POST.get("districts")
            dist_id = request.POST.get("distributor_id")

            form = copy.deepcopy(form)
#             for each in dist:
#                 dist_obj = DistributorDistrict(distributor_id=request.POST.get("distributor_id"))
#                 dist_obj.district_id = each
#                 dist_obj.save(using=settings.BRAND)
        return form
    
    
    
    def save_model(self, request, obj, form, Change):
        obj.address_line_2 = form.cleaned_data['plot_no']
        obj.address_line_3 = form.cleaned_data['locality']
        obj.address_line_4 = form.cleaned_data['street_name']          
        obj.save(using=settings.BRAND)
        user_obj = User.objects.get(id=obj.user_id)
        user_obj.is_active = form.cleaned_data['is_active']
        user_obj.save(using=settings.BRAND)
            
            
    
        super(DistributorAdmin, self).save_model(request, obj, form, Change)
        try:
            send_email(sender=constants.FROM_EMAIL_ADMIN, receiver=obj.email,
                   subject=constants.ADD_DISTRIBUTOR_SUBJECT, body='',
                   message=constants.ADD_DISTRIBUTOR_MESSAGE)
        except Exception as e:
            logger.error('Mail is not sent. Exception occurred', e)
        
    
    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(state=asm_state_list)
        return query_set
    
           
    def change_view(self, request, obj):
        extra_context = {}
        retailer_obj = Retailer.objects.filter(distributor=obj).aggregate(ret=Count("distributor"))
        distributor_obj = DistributorSalesRep.objects.filter(distributor=obj).aggregate(dist=Count("distributor"))
        extra_context['retailer_count'] = retailer_obj["ret"]      
        extra_context['dist_count'] = distributor_obj["dist"] 
        extra_context["obj"] = obj
        return super(DistributorAdmin, self).change_view(request, obj, extra_context=extra_context)

    
    
    
#     
#     def changelist_view(self, request, extra_context=None):
#             print request
#             print request.user,"userrrrr"
# #             print request.user.id
# #             #             distributorstaff = DistributorStaff.objects.get(user__user = request.user)
# #             obj = Distributor.objects.get(user__user__username = request.user)
# #             print obj.id,"iddddd"
# #             retailer_count = Retailer.objects.filter(distributor_id = obj.id).annotate(Count("retailer_id"))
# #             print retailer_count,"retttt"
# #             distributor_count = DistributorSalesRep.objects.filter(distributor_id = obj.id).annotate(Count("distributor_id"))
# #             print distributor_count,"distttttt"
# #         custom_search_mapping = {'Product Id' : 'product_id',
# #                                  'Dealer Id': 'dealer_id__dealer_id', }
# #         extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping
# #                         }
#             extra_context={}
#             return super(DistributorAdmin, self).changelist_view(request, extra_context=extra_context)

# 
#     def changelist_view(self, request, extra_context=None):
#         self.param = request.user
#         
#         return super(DistributorAdmin, self).changelist_view(request)
    
#      def changelist_view(self, request, extra_context=None):
#         self.param = request.user
#         return super(RetailerAdmin, self).changelist_view(request)
#  


class PartMasterCvAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number', 'description',)
    list_display = ('part_no', 'thisdescription', 'thiscategory', 'Applicable_model', 'price',
                    'quantityavailable', 'orderpending')
    
    def part_no(self, obj):
        return obj.part_number
    part_no.short_description = 'Parts #'
    part_no.admin_order_field = 'part_number'
    
    def thisdescription(self, obj):
        return obj.description
    thisdescription.short_description = 'Part Description'
    
    def Applicable_model(self, obj):
        return obj.part_model
    Applicable_model.short_description = 'Applicable Model'
    
    def thiscategory(self, obj):
        return obj.category.name
    thiscategory.short_description = 'Category'
    
    def price(self, obj):
        return obj.mrp
    price.short_description = 'Price'
    
    def quantityavailable(self, obj):
        if obj.available is None:
            return ''
        else:
            return obj.available
    quantityavailable.short_description = 'Available Qut.'
    
    def orderpending(self, obj):
        if obj.pending is None:
            return ''
        else:
            return obj.pending
    orderpending.short_description = 'Pending order Qut.'


   
class DistributorSalesRepForm(forms.ModelForm):
    class Meta:
        model = get_model('DistributorSalesRep')
        exclude = ['distributor_sales_code']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DistributorSalesRepForm, self).__init__(*args, **kwargs)
        
class DSRScorecardReportAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ()
    list_display = ()
        
class DistributorSalesRepAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('distributor_sales_code',)
    list_display = ('sales_representative_code', 'sales_representative_name', 'distributor', 'mobile', 'is_active')
    form = DistributorSalesRepForm
    
    
    def mobile(self, obj):
        if obj.user.phone_number:
            if obj.user.phone_number[0:3] == "+91":
                phone_number = obj.user.phone_number[3:]
            else:
                phone_number = obj.user.phone_number
            return phone_number
        return "NA"
    mobile.short_description = 'Mobile'
    
    
    
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(DistributorSalesRepAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass
    
    def get_actions(self, request):
        actions = super(DistributorSalesRepAdmin, self).get_actions(request)
        return actions
    
    def save_model(self, request, obj, form, change):
#         if DistributorStaff.objects.filter(user__user = request.user).exists():
#             distributorstaff = DistributorStaff.objects.get(user__user = request.user)
#             obj.distributor = Distributor.objects.get(id = distributorstaff.distributor.id)
#         else:
#             obj.distributor = Distributor.objects.get(user__user = request.user)
        try:
            dsr = DistributorSalesRep.objects.filter().last()
            obj.distributor_sales_code = str(int(dsr.distributor_sales_code) + \
                                            constants.DSR_SEQUENCE_INCREMENT)
        except:
            obj.distributor_sales_code = str(constants.DSR_SEQUENCE)
        super(DistributorSalesRepAdmin, self).save_model(request, obj, form, change)
        try:
            send_email(sender=constants.FROM_EMAIL_ADMIN, receiver=obj.email,
                   subject=constants.ADD_DSR_SUBJECT, body='',
                   message=constants.ADD_DSR_MESSAGE)
        except Exception as e:
            logger.error('Mail is not sent. Exception occurred', e)
            
    def sales_representative_code(self, obj):
        return obj.distributor_sales_code
    
    def sales_representative_name(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    
    def distributor_code(self, obj):
        return obj.distributor.distributor_code
    
    def distributor_name(self, obj):
        return obj.distributor.name

    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            logged_in_dist_id = Distributor.objects.get(user_id=request.user).id
            query_set = query_set.filter(distributor_id=logged_in_dist_id)
        return query_set


    
class DistributorStaffForm(forms.ModelForm):
    class Meta:
        model = get_model('DistributorStaff')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DistributorStaffForm, self).__init__(*args, **kwargs)
        self.fields['distributor'].queryset = Distributor.objects.filter(user_id=self.request.user.id)
    
class DistributorStaffAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('distributor_staff_code', 'user_id')
    list_display = ('distributor_staff_code', 'staff_name', 'is_active')
    form = DistributorStaffForm
    
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(DistributorStaffAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass
    
    def get_actions(self, request):
        actions = super(DistributorStaffAdmin, self).get_actions(request)
        return actions
    
    def save_model(self, request, obj, form, change):
        super(DistributorStaffAdmin, self).save_model(request, obj, form, change)
        try:
            send_email(sender=constants.FROM_EMAIL_ADMIN, receiver=obj.email,
                   subject=constants.ADD_DISTRIBUTOR_STAFF_SUBJECT, body='',
                   message=constants.ADD_DISTRIBUTOR_STAFF_MESSAGE)
        except Exception as e:
            logger.error('Mail is not sent. Exception occurred', e)
    
    def staff_name(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    
    
   
    
class RetailerForm(forms.ModelForm):
    plot_no = forms.CharField(max_length=20, label="Plot No")
    street_name = forms.CharField(max_length=30)
    #locality = forms.CharField(max_length=30)
    date_birth = forms.DateTimeField(label='Date of birth', required=False)
    class Meta:
        model = get_model('Retailer')
        exclude = ['approved', 'rejected_reason', 'retailer_code']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RetailerForm, self).__init__(*args, **kwargs)
        self.fields['profile'].widget = TextInput(attrs={'placeholder': 'Retailer'})
        
class RetailerAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    form = RetailerForm
    search_fields = ('retailer_name', 'retailer_town', 'billing_code')
    list_display = ('retailer_code', 'contact', 'name', 'city', 'pincode', 'phone',
                    'mail', 'status')
    exclude = ['mobile', 'approved', 'address_line_2', 'address_line_3', 'address_line_4', 'identification_no', \
               'mechanic_1', 'mechanic_2', 'identity_url', 'signature_url', 'shop_size', 'total_counter_sale', \
               'near_dealer_name', 'total_sale_parts', 'retailer_code']
               
    list_filter = ['approved']
    
    
    def suit_cell_attributes(self, obj, column):
        if column == 'status':
            return {'width': '165px'}
    
    
    def pincode(self, obj):
        return obj.user.pincode
    pincode.admin_order_field = 'user__pincode'
    
    def billing_code(self, obj):
        return obj.billing_code
    billing_code.short_description = 'Retailer billing code'
    
    def name(self, obj):
        return obj.retailer_name
    name.short_description = 'Name of the Shop'
    
    def contact(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    contact.short_description = 'Retailer Contact'
#     

    
    def city(self, obj):
        return obj.retailer_town
    city.short_description = 'City'
    
    def phone(self, obj):
      if obj.user.phone_number:
        if obj.user.phone_number[0:3] == "+91":
            phone_number = obj.user.phone_number[3:]
        else:
            phone_number = obj.user.phone_number
        return phone_number
      else:
            return "NA"
        
    phone.short_description = 'Phone/ Mobile'
    


    
    def mail(self, obj):
        return obj.email
    mail.short_description = 'Email'
#     

    
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(RetailerAdmin, self).get_form(request, obj, **kwargs)
        
        if obj:
            ret_obj = Retailer.objects.get(retailer_code=obj)
        
            
            ModelForm.base_fields['date_birth'].initial = ret_obj.user.date_of_birth
            ModelForm.base_fields['plot_no'].initial = ret_obj.address_line_2
            #ModelForm.base_fields['locality'].initial = ret_obj.address_line_3
            ModelForm.base_fields['street_name'].initial = ret_obj.address_line_4
  
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass
    
    def get_actions(self, request):
        # in case of administrator only, grant him the approve retailer option

        if self.param.groups.filter(name__in=['SuperAdmins', 'Admins', 'AreaSparesManagers']).exists():
            self.actions.append('approve')
        actions = super(RetailerAdmin, self).get_actions(request)
        return actions
    
    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
	    logged_in_dist_id = Distributor.objects.get(user_id=request.user).id
	    
#             asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(approved=2, distributor_id=logged_in_dist_id)
        return query_set

    def changelist_view(self, request, extra_context=None):
        self.param = request.user
        return super(RetailerAdmin, self).changelist_view(request)
    
    def approve(self, request, queryset):
        queryset.update(approved=constants.STATUS['APPROVED'])
        for retailer in queryset:
            try:
                send_email(sender=constants.FROM_EMAIL_ADMIN, receiver=retailer.email,
                       subject=constants.APPROVE_RETAILER_SUBJECT, body='',
                       message=constants.APPROVE_RETAILER_MESSAGE)
            except Exception as e:
                logger.error('Mail is not sent. Exception occurred ', e)
    approve.short_description = 'Approve Selected Retailers'
    
    

#     
    
    
    def save_model(self, request, obj, form, change):

#         if request.user.groups.filter(name__in=[Roles.DISTRIBUTORS, Roles.DISTRIBUTORSALESREP, Roles.SUPERADMINS, Roles.SFAADMIN]).exists():
#         obj.approved = constants.STATUS['WAITING_FOR_APPROVAL']

        # get latest retailer code, add increment and assign it, else assign the sequence first number
        try:
            if form.has_changed:
                obj.retailer_code = obj.retailer_code
                obj.approved = obj.approved
            else:
                retailer = Retailer.objects.filter().last()
                obj.retailer_code = str(int(retailer.retailer_code) + \
                                        constants.RETAILER_SEQUENCE_INCREMENT)
                obj.approved = obj.approved
                
        except:
            obj.retailer_code = str(constants.RETAILER_SEQUENCE)
            
        obj.address_line_2 = form.cleaned_data['plot_no']
        #obj.address_line_3 = form.cleaned_data['locality']
        obj.address_line_4 = form.cleaned_data['street_name']
        obj.save(using=settings.BRAND)
        super(RetailerAdmin, self).save_model(request, obj, form, change)
        
    def status(self, obj):
        # Added retailer by distributor/distributorstaff must be approved by the ASM/admin
        # he can also be rejected on some conditions
        if obj.approved == constants.STATUS['APPROVED']:
   
            return 'Approved'
            
        elif obj.approved == constants.STATUS['WAITING_FOR_APPROVAL'] :
            if self.param.groups.filter(name__in=\
                                    ['SuperAdmins', 'Admins', 'AreaSparesManagers', 'SFAAdmins']).exists():
                
                reject_button = "<a  class='btn btn-success' data-toggle='modal'  href=\"/admin/retailer/approve_retailer/retailer_id/" + str(obj.id) + "\">Approve</a>&nbsp;<input type=\"button\"  class='btn btn-warning' data-toggle='modal'  id=\"button_reject\" value=\"Reject\" onclick=\"popup_reject(\'" + str(obj.id) + "\',\'" + obj.retailer_name + "\',\'" + obj.email + "\',\'" + obj.distributor.name + "\'); return false;\">"
#                 reject_button = "<input type=\"button\" id=\"button_reject\" value=\"Reject\" onclick=\"popup_reject(\'"+str(obj.id)+"\',\'"+obj.retailer_name+"\',\'"+obj.email+"\',\'"+obj.distributor.name+"\'); return false;\">"
                return mark_safe(reject_button)
            else:
                return 'Waiting for approval'
        elif obj.approved == constants.STATUS['REJECTED'] :
            if self.param.groups.filter(name__in=['SuperAdmins', 'Admins', 'AreaSparesManagers', 'SFAAdmins']).exists():
                return 'Rejected'
            else:
                if self.param.groups.filter(name__in=['Distributors', 'DistributorStaffs']).exists():
                    rejected_reason = "<input type=\"button\" value=\"Rejected Reason\" onclick=\"popup_rejected_reason(\'" + str(obj.id) + "\',\'" + obj.retailer_name + "\',\'" + obj.rejected_reason + "\'); return false;\">"
                    return mark_safe(rejected_reason)
    status.allow_tags = True


class RecentOrderAdmin(GmModelAdmin):
    
    
    search_fields =('order_number','dsr','order_date','retailer_name')
    list_display = ('order_number','dsr','retailer','order_date',)
    
    change_form_template = 'admin/bajaj/orderpart/change_list.html'
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS, Roles.DISTRIBUTORSALESREP, Roles.RETAILERS]
    
    exclude = ['so_id', 'po_id', 'do_id']    
    list_filter = ['order_status','retailer','dsr', ]
    
    
    
    def get_actions(self, request):
        # in case of administrator only, grant him the approve retailer option
        print "in action function"
        self.actions.append('process')
        actions = super(RecentOrderAdmin, self).get_actions(request)
        return actions
        
    
    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            logged_in_dist_id = Distributor.objects.get(user_id=request.user).id
        
#             asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(approved=2, distributor_id=logged_in_dist_id)
        return query_set

    def changelist_view(self, request, extra_context=None):
        self.param = request.user
        return super(RecentOrderAdmin, self).changelist_view(request)
        
    
    def process(self, request, queryset):
        print "in process function", queryset
        print queryset[0].order_number
        pass
     
class InvoiceAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]

     
    def changelist_view(self, request, extra_context={}):
        opts= self.model._meta
        self.param = request.user
        invoice_details = []
        invoice_details_dict = {}
        if self.param.groups.filter(name__in=\
                                    ['SuperAdmins', 'Admins', 'NationalSparesManagers', 'AreaSparesManagers', 'SFAAdmins']).exists():
            do_obj = DoDetails.objects.all()
        elif  self.param.groups.filter(name__in=['Distributors']).exists():
            dist_id = Distributor.objects.get(user_id=request.user).id
            do_obj = DoDetails.objects.filter(distributor_id = dist_id)
        for each in do_obj:
            if each.invoice_id != None:
                invoice_obj =   Invoices.objects.get(id = each.invoice_id) 
                invoice_details_dict["invoice_id"] = invoice_obj.invoice_id
                invoice_details_dict["invoice_amount"] = invoice_obj.invoice_amount
                invoice_details_dict["invoice_date"] = invoice_obj.invoice_date
                invoice_details_dict["retailer_name"] = invoice_obj.retailer.retailer_name
                invoice_details.append(invoice_details_dict.copy())

        context = {"invoice_details":invoice_details}
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            extra_context["show_upload_invoice"] = True
        template = 'admin/bajaj/invoices/change_list.html'  # = Your new template
        form_url = ''
        return super(InvoiceAdmin, self).changelist_view(request, context)
   
 
class CollectionAdminForm(forms.ModelForm):
    class Meta:
        model = get_model('Collection')
         
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CollectionAdminForm, self).__init__(*args, **kwargs)



class CollectionAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS, Roles.RETAILERS]
    form = CollectionAdminForm

     
    def __init__(self, *args, **kwargs):
        super(CollectionAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def changelist_view(self, request, extra_context={}):
        self.param = request.user
        ret_details = []
        ret_details_dict = {}
        if self.param.groups.filter(name__in=\
                                    ['SuperAdmins', 'Admins', 'NationalSparesManagers', 'AreaSparesManagers', 'SFAAdmins']).exists():
            ret_objs = Retailer.objects.all()
        elif  self.param.groups.filter(name__in=['Distributors']).exists():
            dist_id = Distributor.objects.get(user_id=request.user).id
            ret_objs = Retailer.objects.filter(distributor=dist_id)        
        for each in ret_objs :
            ret_details_dict["retailer_name"] = each.retailer_name
            # order_objs = OrderPart.objects.filter(retailer_id = each.id).values_list("id",flat=True)
            # orderdetails_obj = OrderPartDetails.objects.filter(order_id__in=order_objs).aggregate(total_value=Sum('line_total'))
            # ret_details_dict["total_value"] = orderdetails_obj["total_value"]
            # total_value = ret_details_dict["total_value"]
            # if total_value != None:
            #     collection_objs = Collection.objects.filter(retailer_id=each.id).values_list("id", flat=True)
            #     total_collected_amount = CollectionDetails.objects.filter(collection_id__in=collection_objs).aggregate(total_value=Sum('collected_amount'))              
            #     if total_collected_amount["total_value"] != None:
            #         tca = total_collected_amount["total_value"]
            #     else :
            #         tca = 0

            ret_details_dict["collection_details"] = "aaaa"
            total_outstanding_amount = 0
            total_order_value = 0
            invoices = Invoices.objects.filter(retailer_id=each.id)
            for invoice in invoices:
                invoice.invoice_amount = invoice.invoice_amount if invoice.invoice_amount else 0
                invoice.paid_amount = invoice.paid_amount if invoice.paid_amount else 0
                total_order_value = total_order_value + invoice.invoice_amount
                total_outstanding_amount = total_outstanding_amount + (invoice.invoice_amount - invoice.paid_amount)
            total_outstanding_amount = float(format(total_outstanding_amount, '.2f'))
            total_order_value = float(format(total_order_value, '.2f'))
            ret_details_dict["outstanding"] = total_outstanding_amount
            ret_details_dict["total_value"] = total_order_value
            ret_details_dict["retailer_id"] = each.id
            ret_details.append(ret_details_dict.copy()) 


        context = {"ret_collection_details":ret_details}
        
        template = 'admin/bajaj/collection/change_list.html'  # = Your new template
        form_url = ''
        return super(CollectionAdmin, self).changelist_view(request, context)



   
class SparePartMasterAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number', 'description',
                     'product_type__product_type')
    list_display = ('part_number', 'description',
                    'part_model', 'price')
    
    def price(self, obj):
        price = SparePartPoint.objects.get(part_number=obj.id)
        return price.price
    
class PartModelAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('name',)
    list_display = ('name', 'active')
    
class CategoriesAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('category_name',)
    list_display = ('category_name', 'active',)
    
# class SubCategoriesAdmin(GmModelAdmin):
#     groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
#     search_fields = ('subcategory_name', 'category')
#     list_display = ('subcategory_name', 'category', 'active')
    
    
class FocusedPartAdmin(GmModelAdmin):
    list_display = ('part_number', 'description', 'start_date', 'end_date', 'get_locality')

    def part_number(self, obj):
        return obj.part.part_number
    
    def description(self, obj):
        return obj.part.description
    description.short_description = 'Description'

    def get_locality(self, obj):
        return obj.locality.name
    get_locality.short_description = 'Locality'

from django.contrib.admin.filters import SimpleListFilter

class NullFilterSpec(SimpleListFilter):
    title = u''

    parameter_name = u''

    def lookups(self, request, model_admin):
        return (
            ('1', 'Parts with Associated Parts',),
        )

    def queryset(self, request, queryset):
        kwargs = {
        '%s'%self.parameter_name : None,
        }
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset

class StartNullFilterSpec(NullFilterSpec):
    title = u'Associated Parts'
    parameter_name = u'associated_parts'


 
class PartCategoryAdmin(GmModelAdmin):
    class Media:
        js = ['js/uploadExcel.js']
    list_filter = ('subcategory', 'products',StartNullFilterSpec )    
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS, Roles.DISTRIBUTORSALESREP, Roles.RETAILERS]
    search_fields = ('part_number', 'description')
    list_display = ('part_no', 'Part_Description', 'Applicable_Model', 'Category',
                    'Price', 'Available', 'active'
                   )
    exclude = ['category', ] 

    def queryset(self, request):
        qs = super(PartCategoryAdmin, self).queryset(request)
        self.request = request
        return qs

    def part_no(self, obj):
        return obj.part_number
    
    part_no.short_description = 'Parts #'
    part_no.admin_order_field = 'part_number'
    
    def Part_Description(self, obj):
        return obj.description
    Part_Description.short_description = 'Part Description'
    Part_Description.allow_tags = True
    
    def Category(self, obj):
         return obj.subcategory.name
    Category.short_description = 'Category'
    
    def Applicable_Model(self, obj):
        return obj.part_models
        
#         return obj.subcategory.part_model.name
    Applicable_Model.short_description='Applicable Model'
    
    def Price(self, obj):
        return obj.mrp
    Price.short_description = 'MRP'

    Category.short_description = 'Category'
    def Applicable_Model(self, obj): 
         if obj.products:       
            return obj.products
         return "NA"
    Applicable_Model.short_description = 'Applicable Model'


    def Available(self, obj):
        try:
            if self.request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                distributor_id = Distributor.objects.get(user_id=self.request.user).id
                partstock_obj = PartsStock.objects.get(part_number_id=obj.id, distributor_id=distributor_id)    
                available_qty = partstock_obj.available_quantity
                return available_qty
            else:
                available_qty = 0
                partstock_obj = PartsStock.objects.filter(part_number=obj.id)    
                for stock_obj in partstock_obj:
                    available_qty = int(stock_obj.available_qty) + int(available_qty)
                return available_qty
        except Exception as ex:
            return 0
    Available.short_description = 'Available Qty.'
    
#     def Pending(self, obj):
#         
#         ordered_qty = OrderPartDetails.objects.filter(part_number_id = obj.id).aggregate(total_ordered=Sum('quantity'))
# #         print ordered_qty,"qtyyyy"
# #         
#         if ordered_qty["total_ordered"] == None:
#           ordered_qty1 =0 
#         else:
#             ordered_qty1 = ordered_qty["total_ordered"]
#         del_qty = OrderDeliveredHistory.objects.filter(part_number_id = obj.id).aggregate(total_delivered = Sum('delivered_quantity'))
#         if del_qty["total_delivered"] == None:
#            del_qty1 = 0 
#         else:
#             del_qty1 = del_qty["total_delivered"]
#         pending_qty= ordered_qty1 - del_qty1
#         return pending_qty
#     Pending.short_description = 'Pending Order Qty.'
#     
#     def Current(self, obj):
#         return obj.current_month_should
#     Current.short_description = 'Monthly Sales Target'
    
    def get_form(self, request, obj=None, **kwargs):
#         self.exclude = ("price)
        form = super(PartCategoryAdmin, self).get_form(request, obj, **kwargs)
        return form
    
    
    def changelist_view(self, request, extra_context={}):
	self.params=request.user
        if request.user.is_superuser or request.user.groups.filter(name=Roles.SFAADMIN).exists():

            self. list_display = ('part_no', 'Part_Description', 'Applicable_Model', 'Category',
                    'Price', 'active')
            
            
        else:
            self.list_display = ('part_no', 'Part_Description', 'Applicable_Model', 'Category',
                    'Price', 'Available', 'active'
                   )
        extra_context["show_upload_stock"] = False
        extra_context["show_upload_part_list"] = False
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            extra_context["show_upload_stock"] = True
        if request.user.groups.filter(name=Roles.SFAADMIN).exists():
            extra_context["show_upload_part_list"] = True

        return super(PartCategoryAdmin, self).changelist_view(request, extra_context=extra_context)



class PartsRackLocationAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number__part_number', 'part_number__description', 'rack_location')
    list_display = ('get_part_number', 'part_description', 'rack_location')
	
    def rack_location(self,obj):
	   return obj.rack_location
    rack_location.short_description = "Rack Location"
 
    def get_part_number(self, obj):
        return obj.part_number.part_number
    get_part_number.short_description = 'Part Number'

    def part_description(self, obj):
        return obj.part_number.description
    part_description.short_description = 'Part Description'
    

    
    def changelist_view(self, request, extra_context={}):
                    
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            extra_context["show_upload_rack_location"] = True
        return super(PartsRackLocationAdmin, self).changelist_view(request, extra_context=extra_context)

    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            logged_in_dist_id = Distributor.objects.get(user_id=request.user).id
            query_set = query_set.filter(distributor_id=logged_in_dist_id)
        return query_set
    
    
class SparePartUPCAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number__part_number', 'unique_part_code', 'part_number__description')
    list_display = ('unique_part_code', 'part_number', 'get_part_description')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('is_used',)
        form = super(SparePartUPCAdmin, self).get_form(request, obj, **kwargs)
        return form

class SparePartPointAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number__part_number', 'points', 'territory')

    def changelist_view(self, request, extra_context={}):
        if request.user.is_superuser or request.user.groups.filter(name=Roles.LOYALTYSUPERADMINS).exists():
            self.list_display = ('part_number', 'points', 'valid_from',
                    'valid_till', 'territory', 'price', 'MRP')
        else:
            self.list_display = ('part_number', 'points', 'valid_from',
                    'valid_till', 'territory')
        return super(SparePartPointAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser and not request.user.groups.filter(name=Roles.LOYALTYSUPERADMINS).exists():
            self.exclude = ('price', 'MRP')
        form = super(SparePartPointAdmin, self).get_form(request, obj, **kwargs)
        return form



    
class DSRWorkAllocationForm(forms.ModelForm):
    class Meta:
        model = get_model('DSRWorkAllocation')
        exclude = ['distributor', 'status']
#         
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super(DSRWorkAllocationForm, self).__init__(*args, **kwargs)
#         dsr_objects = DistributorSalesRep.objects.filter(distributor__user=\
#                                                                     self.request.user)
#         if not dsr_objects:
#             dsr_objects = DistributorSalesRep.objects.all()
#         self.fields['dsr'].queryset = dsr_objects
#         # list the retailer, based on the distributor who is logged in
#         retailer_objects = Retailer.objects.filter(distributor__user=\
#                                                                     self.request.user)
#         if not retailer_objects:
#             retailer_objects = Retailer.objects.all()
#         self.fields['retailer'].queryset = retailer_objects


class DSRWorkAllocationAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    form = DSRWorkAllocationForm
    search_fields = ('dsr', 'date')
    list_display = ('allocated_date', 'dsr_id', 'dist_id')
    
    
    def dsr_id(self, obj):
        return obj.dsr.user.user.username
    dsr_id.short_description = "DSR"
    
    def dist_id(self, obj):
        print "distttt"
       
    dist_id.short_description = "Distributor"
#     
    
#     def distributor(self,obj):
#         return obj.distributor.user.user.username

    def changelist_view(self, request, extra_context={}):

        opts = DSRWorkAllocation._meta
        context = {"opts":opts, "app_label":opts.app_label}
        template = 'admin/bajaj/dsrworkallocation/change_list.html'  
        form_url = ''
        return super(DSRWorkAllocationAdmin, self).changelist_view(request, context)
    
    
    def allocated_date(self, obj):
        return obj.date
    allocated_date.short_description = 'Date'
    allocated_date.admin_order_field = 'date'
    
    def queryset(self, request):
        qs = super(DSRWorkAllocationAdmin, self).queryset(request)
        return qs
    
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(DSRWorkAllocationAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass
    
    def save_model(self, request, obj, form, change):

    
#         obj.distributor = Distributor.objects.get(user__user=request.user)
        super(DSRWorkAllocationAdmin, self).save_model(request, obj, form, change)

class PermanentJourneyPlanForm(forms.ModelForm):
    class Meta:
        model = get_model('PermanentJourneyPlan')

class PermanentJourneyPlanAdmin(GmModelAdmin):
    form = PermanentJourneyPlanForm

    def changelist_view(self, request, extra_context={}):

        opts = PermanentJourneyPlan._meta
        context = {"opts":opts, "app_label":opts.app_label}
        template = 'admin/bajaj/permanentjourneyplan/change_list.html'
        form_url = ''
        return super(PermanentJourneyPlanAdmin, self).changelist_view(request, context)

    def queryset(self, request):
        qs = super(PermanentJourneyPlanAdmin, self).queryset(request)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(PermanentJourneyPlanAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass

    def save_model(self, request, obj, form, change):


#         obj.distributor = Distributor.objects.get(user__user=request.user)
        super(PermanentJourneyPlanAdmin, self).save_model(request, obj, form, change)


class MonthlyPartSalesHistoryAdmin(GmModelAdmin):
    search_fields = ('month', 'year')
    list_display = ('get_retailer_code', 'get_retailer_name', 'get_part', 'quantity', 'month', 'year')

    def get_retailer_name(self, obj):
        return obj.retailer.retailer_name
    def get_retailer_code(self, obj):
        return obj.retailer.retailer_code
    def get_part(self, obj):
        return obj.part.part_number

    get_retailer_name.short_description = "Retailer Name"
    get_retailer_code.short_description = "Retailer Code"
    get_part.short_description = "Part Number"


class AverageLocationSalesHistoryAdmin(GmModelAdmin):
    search_fields = ('month', 'year')
    list_display = ('get_state_name', 'get_city_name', 'get_locality_name', 'get_part', 'sale_value', 'start_month', 'end_month', 'year')

    def get_state_name(self, obj):
        return obj.location.city.state.state_name
    def get_city_name(self, obj):
        return obj.location.city.city
    def get_locality_name(self, obj):
        return obj.location.name
    def get_part(self, obj):
        return obj.part.part_number

    get_state_name.short_description = "State Name"
    get_city_name.short_description = "City Name"
    get_locality_name.short_description = "Locality Name"
    get_part.short_description = "Part Number"

class SFAReportsAdmin(GmModelAdmin):
    def has_change_permission(request,obj=None):
        return True
    def changelist_view(self, request, extra_context={}):
        #FIXME: No SFATargetReports
        #FIXME: Redirect to Charts-application
        return HttpResponseRedirect('https://www.google.com/') 
        #opts = SFATargets._meta
        #context={'objs':objs,'month':month,'year':year,'opts':opts,'app_label':opts.app_label, 'type':"1",'target':'Null'}
        #template = ''
        #form_url = ''
        #return super(SFAReportsAdmin, self).changelist_view(request, context)
    
class SFAHighlightsAdmin(GmModelAdmin):
    def has_change_permission(self,request):
        return True
    def changelist_view(self, request, extra_context={}):
        #FIXME: No SFATargetreports
        opts = SFAHighlights._meta
        extra_context={'type':'1'}
        GmModelAdmin.add_form_template='admin/bajaj/reports/month-year.html'
        context = {"opts":opts, "app_label":opts.app_label}
        #template = ''
        #form_url = ''
        return super(SFAHighlightsAdmin, self).changelist_view(request, context)

'''
class DistributorSalesRepTargetAdmin(GmModelAdmin):
        pass #form = DistributorSalesRepTargetAdminForm
'''
class NsmTargetAdmin(GmModelAdmin):
    pass #form = RetailerTargetAdminForm
    search_fields = ('month', 'year')
    list_display = ('nsm','month', 'year', 'target')
    list_per_page=50
    list_filter=('year','month')

    def add_view(self, request, form_url='', extra_context={}):
        extra_context={'type':'1'}
        GmModelAdmin.add_form_template='admin/bajaj/reports/month-year.html'
        return super(NsmTargetAdmin, self).add_view(request, extra_context=extra_context)

    def has_add_permission(self,request):
        if request.user.is_authenticated():
            if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
                return True
        return False

    def get_queryset(self,request):
        if request.user.is_authenticated():
            #targets=super(NsmTargetAdmin,self).queryset(request)
            if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
                targets=NsmTarget.objects.filter(active=1)
            return targets
        else:
            return HttpResponse({'Error':'User not authenticated'})

class AsmTargetAdmin(GmModelAdmin):
    pass #form = RetailerTargetAdminForm
    search_fields = ('month', 'year')
    list_display = ('asm','month', 'year', 'target')
    list_per_page=50
    list_filter=('year','month')

    def add_view(self, request, form_url='', extra_context={}):
        extra_context={'type':'2'}
        GmModelAdmin.add_form_template='admin/bajaj/reports/month-year.html'
        return super(AsmTargetAdmin, self).add_view(request, extra_context=extra_context)

    def has_add_permission(self,request):
        if request.user.is_authenticated():
            if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
                return True
        return False

    def has_change_permission(self,request,obj=None):
        if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists() or request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
            return True
        return False
    '''
    def changelist_view(self,request, extra_context=None):
        return super(AsmTargetAdmin,self).changelist_view(request)
    '''
    def get_queryset(self,request):
        if request.user.is_authenticated():
            targets=AsmTarget.objects.none()
            #targets=super(AsmTargetAdmin,self).queryset(request)
            if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
                try:
                    Id = NationalSparesManager.objects.get(user_id=request.user.id).id
                    targets=AsmTarget.objects.filter(asm__nsm_id=Id,active=1)
                except:
                    return targets
            if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
                targets=AsmTarget.objects.filter(active=1)
            return targets
        else:
            return Response({'error':'error'})

class DistributorTargetAdmin(GmModelAdmin):
    pass #form = RetailerTargetAdminForm
    search_fields = ('month', 'year')
    list_display = ('distributor','month', 'year', 'target')
    list_per_page=50
    list_filter=('year','month')

    def add_view(self, request, form_url='', extra_context={}):
        extra_context={'type':'3'}
        GmModelAdmin.add_form_template='admin/bajaj/reports/month-year.html'
        return super(DistributorTargetAdmin, self).add_view(request, extra_context=extra_context)

    def has_add_permission(self,request):
        if request.user.is_authenticated():
            #FIXME: Add permission available to only ASM (remove admin)
            if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                return True
        return False

    def has_change_permission(self,request,obj=None):
        if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists() or request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
            return True
        return False

    def get_queryset(self,request):
        if request.user.is_authenticated():
            #targets=super(DistributorTargetAdmin,self).queryset(request)
            targets=AsmTarget.objects.none()
            if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                try:
                    Id = AreaSparesManager.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=DistributorTarget.objects.filter(distributor__asm_id=Id,active=1)
            #if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
            #    try:
            #        Id = NationalSparesManager.objects.get(user_id=request.user.id).id
            #    except:
            #        return Response({'error':'error'})
            #    targets=DistributorTarget.objects.filter(asm__nsm_id=Id,active=1)
            if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
                targets=DistributorTarget.objects.filter(active=1)
                print 'Admin for distributor-----'
            return targets
        else:
            return Response({'error':'error'})


class DistributorSalesRepTargetAdmin(GmModelAdmin):
    pass #form = RetailerTargetAdminForm
    search_fields = ('month', 'year')
    list_display = ('dsr','month', 'year', 'target')
    list_per_page=50
    list_filter=('year','month')

    def add_view(self, request, form_url='', extra_context={}):
        extra_context={'type':'4'}
        GmModelAdmin.add_form_template='admin/bajaj/reports/month-year.html'
        return super(DistributorSalesRepTargetAdmin, self).add_view(request, extra_context=extra_context)

    def has_add_permission(self,request):
        if request.user.is_authenticated():
            #FIXME: Add permission available to only Distributor (remove admin)
            if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                return True
        return False

    def has_change_permission(self,request,obj=None):
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists() or request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
            return True
        return False

    def get_queryset(self,request):
        if request.user.is_authenticated():
            #targets=super(DistributorSalesRepTargetAdmin,self).queryset(request)
            targets=AsmTarget.objects.none()
            if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                try:
                    Id = Distributor.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=DistributorSalesRepTarget.objects.filter(dsr__distributor_id=Id,active=1)
            '''
            if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                try:
                    Id = AreaSparesManager.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=DistributorSalesRepTarget.objects.filter(distributor__asm_id=Id,active=1)
            if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
                try:
                    Id = NationalSparesManager.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=DistributorSalesRepTarget.objects.filter(distributor__asm__nsm_id=Id,active=1)
            '''
            if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
                targets=DistributorSalesRepTarget.objects.filter(active=1)
            return targets
        else:
            return Response({'error':'error'})

class RetailerTargetAdminForm(ModelForm):
    class Meta:
        widgets={
                'year':SuitDateWidget,
        }

class RetailerTargetAdmin(GmModelAdmin):
    form=RetailerTargetAdminForm
    search_fields = ('month', 'year')
    list_display = ('retailer','month', 'year', 'target')
    #suit_form_tabs = (('dsr', 'Distributor Sales Rep'), ('retailer', 'Retailer'))
    list_per_page=50
    #ModelAdmin.date_hierarchy='year'
    #list_select_related=True
    list_filter=('year','month')

    def add_view(self, request, form_url='', extra_context={}):
        extra_context={'type':'5'}
        GmModelAdmin.add_form_template='admin/bajaj/reports/month-year.html'
        return super(RetailerTargetAdmin, self).add_view(request, extra_context=extra_context)
    '''
    def has_delete_permission(self, request,obj=None):
        if request.user.is_authenticated():
            if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                try:
                    Distributor.objects.get(user_id=request.user.id)
                except:
                        return Response({'error':'error'})
                return True
        return False
    '''
    def has_add_permission(self,request):
        if request.user.is_authenticated():
            #FIXME: Add permission available to only Distributor (remove admin)
            if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                #try:
                #    Distributor.objects.get(user_id=request.user.id)
                #except:
                #        return Response({'error':'error'})
                return True
        return False

    def has_change_permission(self,request,obj=None):
        if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists() or request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
            return True
        return False

    def get_queryset(self,request):
        if request.user.is_authenticated():
            #targets=super(RetailerTargetAdmin,self).queryset(request)
            targets=AsmTarget.objects.none()
            if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
                try:
                    Id = Distributor.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=RetailerTarget.objects.filter(retailer__distributor_id=Id,active=1)
            '''
            if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
                try:
                    Id = AreaSparesManager.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=RetailerTarget.objects.filter(retailer__distributor__asm_id=Id,active=1)
            if request.user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
                try:
                    Id = NationalSparesManager.objects.get(user_id=request.user.id).id
                except:
                    return Response({'error':'error'})
                targets=RetailerTarget.objects.filter(retailer__distributor__asm__nsm_id=Id,active=1)
            '''
            if request.user.groups.filter(name=Roles.SFAADMIN).exists() or request.user.groups.filter(name=Roles.SUPERADMINS).exists():
                targets=RetailerTarget.objects.filter(active=1)
            return targets
        else:
            return Response({'error':'error'})
 

import json
class DSRLocationDetailsAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    list_display = ('dsr',)
    def changelist_view(self, request, extra_context={}):
        opts = DSRLocationDetails._meta
        context = {"opts":opts, "app_label":opts.app_label}
        template = 'admin/bajaj/dsrlocationdetails/change_list.html'  # = Your new template
        form_url = ''
        return super(DSRLocationDetailsAdmin, self).changelist_view(request, context)
        
        
        
        
        
#     template = 'admin/bajaj/orderpart/change_list.html'  # = Your new template
#         form_url = ''
#         return super(OrderPartAdmin, self).changelist_view(request,context)




from gladminds.core.core_utils.utils import dictfetchall
from django.db import connections
from django.conf import  settings
class OrderPartAdmin(GmModelAdmin):
    
#     def get_urls(self):
#         urls = super(OrderPartAdmin, self).get_urls()
#         my_urls = [
#             url(r'^admin/order_details/(?P<order_status>\w+)/(?P<retailer_id>\d+)/$', self.my_view),
#         ]
#         return my_urls + urls
    
    change_form_template = 'admin/bajaj/orderpart/change_form.html'
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS, Roles.DISTRIBUTORSALESREP, Roles.RETAILERS]
    
    
    exclude = ['so_id', 'po_id', 'do_id']    
    list_filter = ['order_status', ]
    
    class Media:
        js = ['js/uploadExcel.js']
    
    
       
        


    def my_view(self, request, order_status, retailer_id):
        opts = OrderPart._meta
        order_display = []
        orders = {}
        if order_status == "open":
            order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=0).select_related("retailer", "dsr")
        elif order_status == "allocated":
            order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=1).select_related("retailer", "dsr")
        elif order_status == "shipped":
            order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=3).select_related("retailer", "dsr")
        elif order_status == "cancelled":
            order_obj = OrderPart.objects.filter(retailer=retailer_id, order_status=2).select_related("retailer", "dsr")    
        if len(order_obj) > 0:
            retailer_name = order_obj[0].retailer.retailer_name   
            retailer_id = order_obj[0].retailer.id
            for each in order_obj:
                parts_list = []
                order_id = each.id
                orders_details_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id, part_status=0)
                for each_order in orders_details_obj:
                    parts_dict = {}
                    parts_dict['mrp'] = each_order.part_number.mrp
                    parts_dict['part_number'] = each_order.part_number.part_number
                    parts_dict['part_description'] = each_order.part_number.description
                    parts_dict['quantity'] = each_order.quantity
                    orders['order_id'] = each_order.order_id
                    if each_order.part_number.mrp == "#N/A":
                        each_order.part_number.mrp = 0
                    parts_dict['line_total'] = float(each_order.part_number.mrp) * float(each_order.quantity)
                    parts_dict["part_status"] = each_order.part_status
                    orders["retailer_name"] = each_order.order.retailer.retailer_name
                    orders["dsr_name"] = each_order.order.dsr
                    parts_dict["order_date"] = each_order.order.order_date
                    orderdetails_obj = OrderPartDetails.objects.filter(order_id=order_id).aggregate(Sum('line_total'))
                    orders["total_value"] = orderdetails_obj["line_total__sum"]
                    orders["order_status"] = order_status
                    available_quantity = PartsStock.objects.filter(part_number=each_order.part_number.id)
                    if available_quantity:
                        available_quantity[0].available_quantity
                        parts_dict['available_quantity'] = available_quantity[0].available_quantity
                    else:
                        parts_dict['available_quantity'] = None
                    order_delivered_obj = OrderDeliveredHistory.objects.filter(part_number_id=each_order.part_number_id, order_id=each_order.order_id).aggregate(Sum('delivered_quantity'))         
                    if order_delivered_obj["delivered_quantity__sum"] != None:
                        
                        if each_order.quantity == int(order_delivered_obj["delivered_quantity__sum"]):
                            order_status = "shipped"
                        else:
                            order_status = "allocated"  
                        
                        parts_dict["delivered_quantity"] = int(order_delivered_obj["delivered_quantity__sum"])
                        parts_dict['pending'] = (each_order.quantity) - int(order_delivered_obj["delivered_quantity__sum"])
                    else:
                                    
                        parts_dict["delivered_quantity"] = 0
#                 orders['pending'] = each_order.quantity
                        parts_dict['pending'] = each_order.quantity
                        order_status = order_status
                    parts_list.append(parts_dict.copy())
                if len(orders_details_obj) > 0:
                    orders["parts"] = parts_list
                    order_display.append(orders.copy())
#                 print order_display
#                 orders["retailer_name"] = each_order.retailer.retailer_name
#                 orders["dsr_name"] = each_order.dsr
#                 orders["order_date"] = each_order.order_date
#                 orderdetails_obj = OrderPartDetails.objects.filter(order_id=each_order.id).aggregate(Sum('line_total'))
#                 orders["total_value"] = orderdetails_obj["line_total__sum"]
                
        
        context = {"order_display":order_display,
                 'order_status':order_status,
                 'app_label':opts.app_label,
                 'opts':opts,
                 "retailer_name":retailer_name,
                 "retailer_id":retailer_id
                 }
        
        form_url = ""
        template = 'admin/bajaj/orderpart/retailer_order_list.html'   
        return render(request, template, context)
        

    def get_items(self, request, order_id, order_status):
        opts = OrderPart._meta
        orders_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id)
        length_orders = orders_obj.count() 
        if length_orders == 0:
            delivered = 0
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
                available_quantity[0].available_quantity
                orders['available_quantity'] = available_quantity[0].available_quantity
            else:
                orders['available_quantity'] = None
            order_obj = OrderDeliveredHistory.objects.filter(part_number_id=each_order.part_number_id, order_id=each_order.order_id).aggregate(Sum('delivered_quantity'))
            try:
                orders_det = OrderDeliveredHistory.objects.get(part_number_id=each_order.part_number_id, order_id=each_order.order_id)
                orders['delivered_date'] = orders_det.delivered_date.strftime('%Y-%m-%d %H:%M')
                orders['delivered_quantity'] = orders_det.delivered_quantity
            except Exception as ex:
                orders['delivered_date'] = ""
                orders['delivered_quantity'] = ""
                
            if order_obj["delivered_quantity__sum"] != None:
                orders['pending'] = (each_order.quantity) - int(order_obj["delivered_quantity__sum"])
            else:
                orders['pending'] = each_order.quantity
            order_display.append(orders.copy())
        context = { 
                    "data":order_display,
                    "order_id":order_id,
                    'orders_length': length_orders,
                    'order_id':order_id,
                    'delivered':0,
                    'order_status':order_status,
                    "ordered_date":ordered_date  ,
                    "opts":opts,
                    'app_label':opts.app_label
                            
                   }
        template = 'admin/bajaj/orderpart/retailer_order_list.html'  # = Your new template
        return super(OrderPartAdmin, self).change_view(request, order_id, form_url, context)
#         return render(request,template,context)
        
    
    def total_value(self, obj):    
        order_obj = OrderPartDetails.objects.filter(order_id=obj.id).aggregate(Sum('line_total'))
        return order_obj["line_total__sum"]

    def order_link(self, obj):
        return obj.id
    order_link.short_description = 'order id'
    order_link.admin_order_field = 'order_id'

    def dsr_id(self, obj):
            return obj.dsr
    dsr_id.short_description = "DSR"
    dsr_id.admin_order_field = "DSR"
    
 
    def retailer_name(self, obj):    
        return obj.retailer.retailer_name
    retailer_name.short_description = 'Retailer Shop Name'
#     
    def address_line_2(self, obj):
        return obj.retailer.address_line_2
    address_line_2.short_description = 'Locality'
    
    def get_sql_data(self, query):
        conn = connections[settings.BRAND]
        cursor = conn.cursor()
        cursor.execute(query)
        data = dictfetchall(cursor)
        conn.close()
        return data
    

    
    
    def open_orders(self, obj):
        open_orders = obj.retailer_id
        query = "Select Count(retailer_id) from gm_orderpart  where accept=0 and retailer_id={0} group by retailer_id;".format(obj.retailer_id)
        open_orders_count = self.get_sql_data(query)
        return open_orders_count[0]["Count(retailer_id)"]


    
    def get_actions(self, request):
        # in case of administrator only, grant him the approve retailer option
        # if self.param.groups.filter(name__in =['distributors']).exists():
        self.actions.append('accept')
        actions = super(OrderPartAdmin, self).get_actions(request)
        return actions
    


    
       
    def changelist_view(self, request, extra_context={}):
        order_details = []
        order_details_dict = {}
        query = "select *from orderDetail";
        data = self.get_sql_data(query)
        for each in data:
            order_details_dict["open_orders_len"] = each["open_count"]
            order_details_dict["pending_orders_len"] = each["pending_count"]
            order_details_dict["shipped_orders_len"] = each["shipped_count"]
            order_details_dict["cancelled_orders_len"] = each["cancelled_count"]
            order_details_dict["ret_id"] = each["retailer_id"]
            retailer_obj = Retailer.objects.get(id = order_details_dict["ret_id"])
            order_details_dict["ret_mobile"] = retailer_obj.mobile
            order_details_dict["ret_name"] = each["retailer_name"]
            invoices = Invoices.objects.filter(retailer_id = order_details_dict["ret_id"])
            if invoices:
                total_amount = 0
                collection = 0
                for invoice in invoices:
                    invoice.invoice_amount = invoice.invoice_amount if invoice.invoice_amount else 0
                    invoice.paid_amount = invoice.paid_amount if invoice.paid_amount else 0
                    total_amount = total_amount + (invoice.invoice_amount - invoice.paid_amount)
#                     retailer_dict.update({'retailer_id':retailer.retailer_code})
#                     retailer_dict.update({'invoice_id': invoice.invoice_id})
#                     retailer_dict.update({'total_amount': total_amount})
#                     retailer_dict.update({'invoice_date': invoice.invoice_date.date()})
                    #get the collections for that invoice
                    # collection_objs = Collection.objects.filter(invoice_id = invoice.id)
                    # for each in collection_objs:
                    #     collections = CollectionDetails.objects.filter(collection_id = each.id)
                    #     if collections:
                    #         for each_collections in collections:
                    #             if each_collections.collected_amount == None:
                    #                     each_collections.collected_amount=0
                    #             collection = collection + each_collections.collected_amount
#                     retailer_dict.update({'collected_amount': collection})
                
                # outstanding = total_amount + collection
                total_amount = float(format(total_amount, '.2f'))
                order_details_dict["outstanding"] = total_amount
#                     retailer_list.append(retailer_dict)
            else: 
                outstanding =0
                order_details_dict["outstanding"] = "NA"

            order_details.append(order_details_dict.copy()) 
            order_details = filter(lambda x: self.role_based_filter_data(x, request.user), order_details)

        order_details = sorted(order_details, key=itemgetter('ret_name'))

        context = {"order_details":order_details}
        template = 'admin/bajaj/orderpart/change_list.html'  # = Your new template
        form_url = ''
        return super(OrderPartAdmin, self).changelist_view(request, context)

    def role_based_filter_data(self, order_details_dict, user):
        # FIXME: Return false other than all the known user roles
        # FIXME: Move this method to a more generic location, may be auth_helper
        retailer_obj = Retailer.objects.get(id=order_details_dict['ret_id'])
        if user.groups.filter(name=Roles.DISTRIBUTORS).exists():
            associated_dist_id = retailer_obj.distributor_id
            logged_in_dist = Distributor.objects.get(user=user.id).id
            return logged_in_dist ==  associated_dist_id
        if user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            logged_in_asm = AreaSparesManager.objects.get(user=user.id).id
            associated_asm_id = retailer_obj.distributor.asm_id
            return logged_in_asm ==  associated_asm_id
        if user.groups.filter(name=Roles.NATIONALSPARESMANAGERS).exists():
            logged_in_nsm = NationalSparesManager.objects.get(user=user.id).id
            associated_nsm_id = retailer_obj.distributor.asm.nsm_id
            return logged_in_nsm ==  associated_nsm_id
        return True

        
        
        
        
#         if request.user.is_superuser or request.user.groups.filter(name=Roles.SFAADMIN).exists():
# 
#             self. list_display = ('part_no', 'Part_Description','Applicable_Model', 'Category',
#                     'Price', 'active')
#             
#             
#         else:
#             self.list_display = ('part_no', 'Part_Description', 'Applicable_Model','Category',
#                     'Price', 'Available', 'Pending')
#                     
#         if request.user.groups.filter(name=Roles.DISTRIBUTORS).exists():
#             extra_context["show_upload_stock"] = True

       
    
     
     
    def retailer_change_view(self, request, model_admin, order_id=None):
        template = 'admin/bajaj/orderpart/change_form.html'  # = Your new template
        opts = model_admin.model._meta
        order_details=[]
        order_obj = OrderPart.objects.get(id=order_id)
        print order_obj.retailer,"retttt"
        order_objs = OrderPart.objects.filter(retailer=order_obj.retailer,accept=0)
        print order_objs,"objssssssssssssssssss"
        for each in order_objs:
            print each.id
            orderdetails_obj = OrderPartDetails.objects.filter(order_id=each.id).aggregate(Sum('line_total'))
            orderdetails_obj["line_total__sum"]
            
            
            order_dict={}
            order_dict["total_value"]= orderdetails_obj["line_total__sum"]
            order_dict["order_id"] = each.id
            order_dict["order_date"] = order_obj.order_date
            order_details.append(order_dict)
        print order_details,"disppp"
        context = { 
                   'opts':opts,
                   'app_label' : opts.app_label,
                    'order_details': order_details,
                    'order_id':order_id,
                    'delivered':0                    
                   }
        template = 'admin/bajaj/orderpart/change_form.html'  # = Your new template
        form_url = ''
        return super(OrderPartAdmin, self).change_view(request, order_id, form_url, context)

        form_url = ''
        context={}
        
        return super(OrderPartAdmin, self).change_view(request, retailer_name, form_url, context)
        
        
        
     
     

    def admin_change_view(self, request, model_admin, order_id=None):
  
        opts = model_admin.model._meta
        obj = None
     
        orders_obj = OrderPartDetails.objects.select_related("part_number", "order").filter(order=order_id)
        length_orders = orders_obj.count() 
        if length_orders == 0:
            delivered = 0
        order_display = []
        orders = {}
        for each_order in orders_obj:
            orders['mrp'] = each_order.part_number.mrp
            orders['part_number'] = each_order.part_number.part_number
            
            
            orders['part_description'] = each_order.part_number.description
            orders['quantity'] = each_order.quantity
            orders['order_id'] = each_order.order_id
            orders['line_total'] = float(each_order.part_number.mrp) * float(each_order.quantity)
            available_quantity = PartsStock.objects.filter(part_number = each_order.part_number.id)
            
            
            if available_quantity:
                available_quantity[0].available_quantity
                orders['available_quantity'] = available_quantity[0].available_quantity
            else:
                orders['available_quantity'] = None
            order_obj = OrderDeliveredHistory.objects.filter(part_number_id=each_order.part_number_id, order_id=each_order.order_id).aggregate(Sum('delivered_quantity'))
            try:
                orders_det = OrderDeliveredHistory.objects.get(part_number_id=each_order.part_number_id, order_id=each_order.order_id)
    
    #             order_date  = str(orders_det.delivered_date)
                orders['delivered_date'] = orders_det.delivered_date.strftime('%Y-%m-%d %H:%M')
                orders['delivered_quantity'] = orders_det.delivered_quantity
            except Exception as ex:
                orders['delivered_date'] = ""
                orders['delivered_quantity'] = ""
                
            if order_obj["delivered_quantity__sum"] != None:
                orders['pending'] = (each_order.quantity) - int(order_obj["delivered_quantity__sum"])
            else:
                orders['pending'] = each_order.quantity
            order_display.append(orders.copy())
        context = { 
                   'opts':opts,
                    'obj':obj,
                    "data":order_display,  # New
                   'app_label' : opts.app_label,
                    'orders_length': length_orders,
                    'order_id':order_id,
                    'delivered':0                    
                   }
        template = 'admin/bajaj/orderpart/change_form.html'  # = Your new template
        form_url = ''
        return super(OrderPartAdmin, self).change_view(request, order_id, form_url, context)
           
    def change_view(self, request, order_id):
        return self.retailer_change_view(request, self, order_id)
   
#     def changelist_view(self, request, extra_context={}):
# #         self.message_user(request, "Sorry, you do not have permission to update.",
# #                                   level=messages.ERROR)
#         return super(OrderPartAdmin, self).changelist_view(request, extra_context=extra_context)
   
    
    
    
    def Actions(self, obj):
        # Added retailer by distributor/distributorstaff must be approved by the ASM/admin
        # he can also be rejected on some conditions
#         if obj.approved == constants.STATUS['APPROVED']:
#    
#             return 'Approved'
#             
#         elif obj.approved == constants.STATUS['WAITING_FOR_APPROVAL'] :
#             if self.param.groups.filter(name__in=\
#                                     ['SuperAdmins', 'Admins', 'AreaSparesManagers', 'SFAAdmins']).exists():
                
                reject_button = "<a  class='btn btn-success' data-toggle='modal'  href=\"/admin/retailer/approve_retailer/retailer_id/" + str(obj.id) + "\">Accept</a>&nbsp;<input type=\"button\"  class='btn btn-warning' data-toggle='modal'  id=\"button_reject\" value=\"Cancel\" onclick=\"popup_reject(\'" + str(obj.id) + "\'); return false;\">"
#                 reject_button = "<input type=\"button\" id=\"button_reject\" value=\"Reject\" onclick=\"popup_reject(\'"+str(obj.id)+"\',\'"+obj.retailer_name+"\',\'"+obj.email+"\',\'"+obj.distributor.name+"\'); return false;\">"
                return mark_safe(reject_button)
#             else:
#                 return 'Waiting for approval'
#         elif obj.approved == constants.STATUS['REJECTED'] :
#             if self.param.groups.filter(name__in=['SuperAdmins', 'Admins', 'AreaSparesManagers', 'SFAAdmins']).exists():
#                 return 'Rejected'
#             else:
#                 if self.param.groups.filter(name__in=['Distributors', 'DistributorStaffs']).exists():
#                     rejected_reason = "<input type=\"button\" value=\"Rejected Reason\" onclick=\"popup_rejected_reason(\'" + str(obj.id) + "\',\'" + obj.retailer_name + "\',\'" + obj.rejected_reason + "\'); return false;\">"
#                     return mark_safe(rejected_reason)
    Actions.allow_tags = True
    
    def queryset(self, request):
            """
            Returns a QuerySet of all model instances that can be edited by the
            admin site. This is used by changelist_view.
            """
            
#             list_display = ('order_link', 'retailer_name', 'dsr_id',
#                    'total_value', 'order_date')
            
            query_set = self.model._default_manager.get_query_set()
            if request.GET:
                    query_set = query_set.filter(order_placed_by=2)
            
                    self.list_display = ('order_link', 'retailer_name', 'dsr_id', 'open_orders',
                                         'pending_orders', 'shipped_orders', 'cancelled_orders')
                    self.list_display_links = ('retailer_name', 'open_orders', 'pending_orders')

            else:
#                     query_set = query_set.filter(order_placed_by=1)
                    query_set = OrderPart.objects.filter(order_placed_by=1)

                    self.list_display = ('retailer_name', 'total_value', 'order_date')
#             query_set.
            return query_set

   

    
class SparePartline(TabularInline):
    model = models.AccumulationRequest.upcs.through

class ProductCatalogAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    list_filter = ('plate__plate_name', 'plate__model__model_name')
    #search_fields = ('partner__partner_id', 'product_id',
     #               'brand', 'model', 'category',
      #              'sub_category')
    list_display = ('get_model', 'get_plate', 'part_number', 'description', 'mrp')

    def get_model(self, obj):
        return obj.plate.model.model_name
    get_model.short_description = "Models"
    get_model.admin_order_field = 'model'

    def get_plate(self, obj):
        return obj.plate.plate_name
    get_plate.short_description = "Plates"
    get_plate.admin_order_field = 'plate_name'

class PartnerAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    list_filter = ('partner_type',)
    search_fields = ('partner_id', 'name', 'partner_type')

    list_display = ('partner_id', 'name' , 'address', 'partner_type')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('partner_id',)
        form = super(PartnerAdmin, self).get_form(request, obj, **kwargs)
        return form

class AccumulationRequestAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS, Roles.LOYALTYADMINS, Roles.LOYALTYSUPERADMINS]
    search_fields = ('member__mechanic_id', 'upcs__unique_part_code')
    list_display = ('member', 'get_mechanic_name', 'get_mechanic_district',
                     'asm', 'get_upcs', 'points',
                     'total_points', 'created_date')
    
    def get_upcs(self, obj):
        upcs = obj.upcs.all()
        if upcs:
            return ' | '.join([str(upc.unique_part_code) for upc in upcs])
        else:
            return None

    get_upcs.short_description = 'UPC'

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(member__state=asm_state_list)

        return query_set

    def changelist_view(self, request, extra_context=None):
        extra_context = {'created_date_search': True
                        }
        return super(AccumulationRequestAdmin, self).changelist_view(request, extra_context=extra_context)

class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
    
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        for field in constants.MANDATORY_MECHANIC_FIELDS:
            self.fields[field].label = self.fields[field].label + ' * '

class MemberAdmin(GmModelAdmin):
    list_filter = ('form_status',)
    form = MemberForm
    search_fields = ('mechanic_id', 'permanent_id',
                     'phone_number', 'first_name',
                     'state__state_name', 'district')
    list_display = ('get_mechanic_id', 'first_name', 'date_of_birth',
                    'phone_number', 'shop_name', 'district',
                    'state', 'pincode', 'registered_by_distributor')
    readonly_fields = ('image_tag',)

    def suit_row_attributes(self, obj):
        class_map = {
            'Incomplete': 'error'
        }
        css_class = class_map.get(str(obj.form_status))
        if css_class:
            return {'class': css_class}
        
    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(state=asm_state_list)

        return query_set

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('mechanic_id', 'form_status', 'sent_sms', 'total_points', 'sent_to_sap', 'permanent_id', 'download_detail')
        form = super(MemberAdmin, self).get_form(request, obj, **kwargs)
        return form

#     def save_model(self, request, obj, form, change):
#         if not (obj.phone_number == '' or (len(obj.phone_number) < 10)):
#             obj.phone_number=utils.mobile_format(obj.phone_number)
#         super(MemberAdmin, self).save_model(request, obj, form, change)

class CommentThreadInline(TabularInline):
    model = models.CommentThread
    fields = ('created_date', 'user', 'message')
    extra = 0
    max_num = 0
    readonly_fields = ('created_date', 'user', 'message')


class RedemptionCommentForm(forms.ModelForm):
    extra_field = forms.CharField(label='comment', required=False, widget=forms.Textarea(attrs={'style':'resize: none;'}))

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('extra_field', None)
        transaction_id = self.instance
        if extra_field:
            loyalty.save_comment('redemption', extra_field, transaction_id, self.current_user)
        return super(RedemptionCommentForm, self).save(commit=commit)
    
    class Meta:
        model = models.RedemptionRequest

    
class RedemptionRequestAdmin(GmModelAdmin):
    readonly_fields = ('image_tag', 'transaction_id',)
    form = RedemptionCommentForm
    inlines = (CommentThreadInline,)
    list_filter = (
        ('created_date', DateFieldListFilter),
    )
    search_fields = ('member__phone_number', 'product__product_id', 'partner__partner_id', 'transaction_id')
    list_display = ('member', 'get_mechanic_name',
                     'delivery_address', 'get_mechanic_pincode',
                     'get_mechanic_district', 'get_mechanic_state',
                     'product', 'created_date', 'due_date',
                     'expected_delivery_date', 'status', 'partner')
    
    fieldsets = (
        (None, {
            'fields': (
            'transaction_id', 'delivery_address', 'expected_delivery_date', 'status',
            'tracking_id', 'due_date', 'approved_date', 'shipped_date',
            'delivery_date', 'pod_number', 'product', 'member',
            'partner', 'image_url', 'image_tag',
            'extra_field')
        }),
        )   
    

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.RPS).exists():
            query_set = query_set.filter(is_approved=True, packed_by=request.user.username)
        elif request.user.groups.filter(name=Roles.LPS).exists():
            query_set = query_set.filter(status__in=constants.LP_REDEMPTION_STATUS, partner__user=request.user)
        elif request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(member__state=asm_state_list)

        return query_set

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('is_approved', 'packed_by', 'refunded_points', 'resolution_flag')
        form = super(RedemptionRequestAdmin, self).get_form(request, obj, **kwargs)
        form = copy.deepcopy(form)
        if request.user.groups.filter(name=Roles.RPS).exists():
            form.base_fields['status'].choices = constants.GP_REDEMPTION_STATUS
        elif request.user.groups.filter(name=Roles.LPS).exists():
            form.base_fields['status'].choices = constants.LP_REDEMPTION_STATUS
        else:
            form.base_fields['status'].choices = constants.REDEMPTION_STATUS
        form.current_user = request.user
        return form

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status != 'Rejected':
            date = loyalty.set_date("Redemption", obj.status)
            obj.due_date = date['due_date']
            obj.expected_delivery_date = date['expected_delivery_date']
            obj.resolution_flag = False
        if 'status' in form.changed_data:
            if obj.status == 'Approved':
                obj.is_approved = True
                obj.packed_by = obj.partner.user.user.username
                obj.approved_date = datetime.datetime.now()
            elif obj.status in ['Rejected', 'Open'] :
                obj.is_approved = False
                obj.packed_by = None
            elif obj.status == 'Shipped':
                obj.shipped_date = datetime.datetime.now()
            elif obj.status == 'Delivered':
                obj.delivery_date = datetime.datetime.now()
        if 'status' in form.changed_data:
            if obj.status == 'Approved' and obj.refunded_points:
                loyalty.update_points(obj.member, redeem=obj.product.points)
                obj.refunded_points = False
            elif obj.status == 'Rejected' and not obj.refunded_points:
                loyalty.update_points(obj.member, accumulate=obj.product.points)
                obj.refunded_points = True
        super(RedemptionRequestAdmin, self).save_model(request, obj, form, change)
        if 'status' in form.changed_data and obj.status in constants.STATUS_TO_NOTIFY:
            loyalty.send_request_status_sms(obj)
        if 'partner' in form.changed_data and obj.partner:
            loyalty.send_mail_to_partner(obj)

    def suit_row_attributes(self, obj):
        class_map = {
            'Rejected': 'error',
            'Approved': 'success',
            'Delivered': 'warning',
            'Packed': 'info',
            'Shipped': 'info',
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}

class WelcomeKitCommentForm(forms.ModelForm):
    extra_field = forms.CharField(label='comment', required=False, widget=forms.Textarea(attrs={'style':'resize: none;'}))

    def save(self, commit=True):
        extra_field = self.cleaned_data.get('extra_field', None)
        transaction_id = self.instance
        if extra_field:
            loyalty.save_comment('welcome_kit', extra_field, transaction_id, self.current_user)
        return super(WelcomeKitCommentForm, self).save(commit=commit)
    
    class Meta:
        model = models.WelcomeKit
       
class WelcomeKitAdmin(GmModelAdmin):
    list_filter = ('status',)
    form = WelcomeKitCommentForm
    inlines = (CommentThreadInline,)
    search_fields = ('member__phone_number', 'partner__partner_id', 'transaction_id')
    list_display = ('member', 'get_mechanic_name',
                     'delivery_address', 'get_mechanic_pincode',
                     'get_mechanic_district', 'get_mechanic_state',
                     'created_date', 'due_date', 'expected_delivery_date', 'status', 'partner')
    readonly_fields = ('image_tag', 'transaction_id')
    fieldsets = (
    (None, {
        'fields': (
        'transaction_id', 'delivery_address',
        'expected_delivery_date', 'status',
        'tracking_id', 'due_date', 'shipped_date',
        'delivery_date', 'pod_number', 'member',
        'partner', 'image_url', 'image_tag',
        'extra_field')
    }),
    ) 
    
    def save_model(self, request, obj, form, change):
        if 'partner' in form.changed_data and obj.partner and obj.status in ['Accepted', 'Open']:
                obj.packed_by = obj.partner.user.user.username
        if 'status' in form.changed_data:
            if obj.status == 'Shipped':
                obj.shipped_date = datetime.datetime.now()
            elif obj.status == 'Delivered':
                obj.delivery_date = datetime.datetime.now()
        date = loyalty.set_date("Welcome Kit", obj.status)
        obj.due_date = date['due_date']
        obj.expected_delivery_date = date['expected_delivery_date']
        obj.resolution_flag = False
        super(WelcomeKitAdmin, self).save_model(request, obj, form, change)
        if 'status' in form.changed_data and obj.status == "Shipped":
            loyalty.send_welcome_kit_delivery(obj)
        if 'partner' in form.changed_data and obj.partner:
            loyalty.send_welcome_kit_mail_to_partner(obj)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('resolution_flag', 'packed_by')
        form = super(WelcomeKitAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def suit_row_attributes(self, obj):
        class_map = {
            'Accepted': 'success',
            'Packed': 'info',
            'Shipped': 'info',
            'Delivered': 'warning'
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}
        
    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.RPS).exists():
            query_set = query_set.filter(packed_by=request.user.username)
        elif request.user.groups.filter(name=Roles.LPS).exists():
            query_set = query_set.filter(status__in=constants.LP_REDEMPTION_STATUS, partner__user=request.user)
        elif request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list = models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set = query_set.filter(member__state=asm_state_list)

        return query_set

class LoyaltySlaAdmin(GmModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
        'status', 'action',
        ('reminder_time', 'reminder_unit'),
        ('resolution_time', 'resolution_unit'),
        ('member_resolution_time', 'member_resolution_unit'))
        }),
        )    
    def reminder_time(self):
        return str(self.reminder_time) + ' ' + self.reminder_unit
    
    def resolution_time(self):
        return str(self.resolution_time) + ' ' + self.resolution_unit
    
    def member_resolution_time(self):
        return str(self.member_resolution_time) + ' ' + self.member_resolution_unit

    list_display = ('status', 'action', reminder_time, resolution_time, member_resolution_time)
    
class ConstantAdmin(GmModelAdmin):
    search_fields = ('constant_name', 'constant_value')
    list_display = ('constant_name', 'constant_value',)
    

class TransporterAdmin(GmModelAdmin):
    list_display = ('transporter_id', 'get_transporter_username', 'get_transporter_name')

class SupervisorAdmin(GmModelAdmin):
    list_display = ('supervisor_id', 'get_supervisor_username', 'get_supervisor_name', 'get_transporter')

class ContainerTrackerAdmin(GmModelAdmin):
    list_display = ('zib_indent_num', 'lr_number', 'consignment_id', 'container_no',
                    'seal_no', 'status', 'gatein_date',
                    'get_transporter', 'submitted_by')

    def suit_row_attributes(self, obj):
        class_map = {
            'Open': 'success',
            'Closed': 'warning',
            'Inprogress': 'info',
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}

class ContainerIndentAdmin(GmModelAdmin):
    search_fields = ('indent_num', 'transporter__user__user__username')
    list_display = ('indent_num',
                    'no_of_containers',
                    'status',
                    'transporter')

    def suit_row_attributes(self, obj):
        class_map = {
            'Open': 'success',
            'Closed': 'warning',
            'Inprogress': 'info',
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}



class ContainerLRAdmin(GmModelAdmin):
    search_fields = ('zib_indent_num__indent_num',)
    list_display = ('lr_number', 'zib_indent_num',
                    'get_indent_status',
                    'consignment_id', 'container_no',
                    'seal_no', 'gatein_date',
                    'get_transporter', 'submitted_by')
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('status', 'sent_to_sap')
        form = super(ContainerLRAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def suit_row_attributes(self, obj):
        class_map = {
            'Open': 'success',
            'Closed': 'warning',
            'Inprogress': 'info',
        }
        css_class = class_map.get(str(obj.zib_indent_num.status))
        if css_class:
            return {'class': css_class}

def get_admin_site_custom(brand):
    brand_admin = BajajAdminSite(name=brand)
    
    brand_admin.register(User, UserAdmin)
    brand_admin.register(Group, GroupAdmin)
    brand_admin.register(get_model("UserProfile", brand), UserProfileAdmin)
    
    brand_admin.register(get_model("Distributor", brand), DistributorAdmin)
    brand_admin.register(get_model("Collection", brand), CollectionAdmin)
    brand_admin.register(get_model("Invoices", brand), InvoiceAdmin)
    # brand_admin.register(get_model("DistributorStaff", brand), DistributorStaffAdmin)
#     brand_admin.register(get_model("BackOrders", brand), BackOrdersAdmin)
    brand_admin.register(get_model("DistributorSalesRep", brand), DistributorSalesRepAdmin)  
    brand_admin.register(get_model("DSRWorkAllocation", brand), DSRWorkAllocationAdmin)
    brand_admin.register(get_model("PermanentJourneyPlan", brand), PermanentJourneyPlanAdmin) 
    brand_admin.register(get_model("DSRLocationDetails", brand), DSRLocationDetailsAdmin)
    brand_admin.register(get_model("PartsRackLocation", brand), PartsRackLocationAdmin)
    brand_admin.register(get_model("Retailer", brand), RetailerAdmin)
    brand_admin.register(get_model("PartModel", brand), PartModelAdmin)
    brand_admin.register(get_model("Categories", brand), CategoriesAdmin)
    brand_admin.register(get_model("MonthlyPartSalesHistory", brand), MonthlyPartSalesHistoryAdmin)
    #brand_admin.register(get_model("AverageLocationSalesHistory", brand), AverageLocationSalesHistoryAdmin)

    # brand_admin.register(get_model("SubCategories", brand), SubCategoriesAdmin)
#     brand_admin.register(get_model("PartMasterCv", brand), PartListAdmin)
    brand_admin.register(get_model("OrderPart", brand), OrderPartAdmin)
    brand_admin.register(get_model("OrderPartDetails", brand), OrderPartDetailsAdmin)
    brand_admin.register(get_model("PartPricing", brand), PartCategoryAdmin)
    brand_admin.register(get_model("FocusedPart", brand), FocusedPartAdmin)
    brand_admin.register(get_model("NationalSparesManager", brand), NSMAdmin)
    brand_admin.register(get_model("AreaSparesManager", brand), ASMAdmin)
    brand_admin.register(get_model("NationalSalesManager", brand), NationalSalesManagerAdmin)
#     brand_admin.register(get_model("AreaSalesManager", brand), AreaSalesManagerAdmin)
    brand_admin.register(get_model("DSRScorecardReport", brand), DSRScorecardReportAdmin)
    # brand_admin.register(get_model("SparePartMasterData", brand), SparePartMasterAdmin)
    brand_admin.register(get_model("Dealer", brand), DealerAdmin)
    brand_admin.register(get_model("AuthorizedServiceCenter", brand), AuthorizedServiceCenterAdmin)
    brand_admin.register(get_model("ServiceAdvisor", brand), ServiceAdvisorAdmin)
    
    brand_admin.register(get_model("BrandProductCategory", brand), BrandProductCategoryAdmin)
    brand_admin.register(get_model("ProductType", brand), ProductTypeAdmin)
    brand_admin.register(DispatchedProduct, ListDispatchedProduct)
    brand_admin.register(get_model("ProductData", brand), ProductDataAdmin)
    brand_admin.register(get_model("CouponData", brand), CouponAdmin)
    
    brand_admin.register(get_model("ASCTempRegistration", brand), ASCTempRegistrationAdmin)
    brand_admin.register(get_model("SATempRegistration", brand), SATempRegistrationAdmin)
    brand_admin.register(get_model("CustomerTempRegistration", brand), CustomerTempRegistrationAdmin)
    brand_admin.register(get_model("SMSLog", brand), SMSLogAdmin)
    brand_admin.register(get_model("EmailLog", brand), EmailLogAdmin)
    brand_admin.register(get_model("DataFeedLog", brand), FeedLogAdmin)
    brand_admin.register(get_model("FeedFailureLog", brand))
    
    brand_admin.register(get_model("EmailTemplate", brand), EmailTemplateAdmin)
    brand_admin.register(get_model("MessageTemplate", brand), MessageTemplateAdmin)
    brand_admin.register(get_model("SLA", brand), SlaAdmin)
    brand_admin.register(get_model("ServiceDeskUser", brand), ServiceDeskUserAdmin)
    brand_admin.register(get_model("Service", brand), ServiceAdmin)
    brand_admin.register(get_model("ServiceType", brand))
    brand_admin.register(get_model("Constant", brand), ConstantAdmin)
    brand_admin.register(get_model("Feedback", brand))
    brand_admin.register(get_model("Territory", brand))
    brand_admin.register(get_model("BrandDepartment", brand))
    brand_admin.register(get_model("DepartmentSubCategories", brand))
    brand_admin.register(get_model("ContainerTracker", brand), ContainerTrackerAdmin)
    brand_admin.register(get_model("Transporter", brand), TransporterAdmin)
    brand_admin.register(get_model("Supervisor", brand), SupervisorAdmin)
    brand_admin.register(get_model("ContainerIndent", brand), ContainerIndentAdmin)
    brand_admin.register(get_model("ContainerLR", brand), ContainerLRAdmin)
    brand_admin.register(get_model("PartIndexDetails", brand), ProductCatalogAdmin)


    # Disable the delete action throughout the admin site
    brand_admin.disable_action('delete_selected')
    
    brand_admin.register(get_model("RecentOrder", brand), RecentOrderAdmin)
    brand_admin.register(get_model("SFAReports", brand), SFAReportsAdmin)
    #brand_admin.register(get_model("SFAHighlights", brand), SFAHighlightsAdmin)
    #brand_admin.register(get_model("SetTarget", brand), SetTargetAdmin)
    brand_admin.register(get_model("NsmTarget", brand), NsmTargetAdmin)
    brand_admin.register(get_model("AsmTarget", brand), AsmTargetAdmin)
    brand_admin.register(get_model("DistributorTarget", brand), DistributorTargetAdmin)
    brand_admin.register(get_model("DistributorSalesRepTarget", brand), DistributorSalesRepTargetAdmin)
    brand_admin.register(get_model("RetailerTarget", brand), RetailerTargetAdmin)
    return brand_admin

brand_admin = get_admin_site_custom(GmApps.BAJAJ)

