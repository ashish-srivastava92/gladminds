import copy
import datetime, logging
from django import forms
from django.contrib.admin import AdminSite, TabularInline
from django.contrib.auth.models import User, Group
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList, ORDER_VAR
from django.contrib.admin import DateFieldListFilter
from django import forms
from django.utils.html import mark_safe

from gladminds.bajaj import models
from gladminds.bajaj.models import Distributor, DistributorStaff, DistributorSalesRep, \
                        Retailer, UserProfile, SparePartPoint, State,AreaSparesManager
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

logger = logging.getLogger('gladminds')

PROFILE_CHOICES = (
        ('distributor', 'Wholesale Distributors'),
    )

class BajajAdminSite(AdminSite):
    pass


class UserProfileAdmin(GmModelAdmin):
    search_fields = ('user__username', 'phone_number',)
    list_display = ('user', 'phone_number', 'status', 'address',
                    'state', 'country', 'pincode', 'date_of_birth', 'gender')
    readonly_fields = ('image_tag',)

class ZonalServiceManagerAdmin(GmModelAdmin):
    search_fields = ('zsm_id',)
    list_display = ('zsm_id', 'get_user', 'get_profile_number', 'regional_office')
    
class AreaServiceManagerAdmin(GmModelAdmin):
    search_fields = ('asm_id','zsm__zsm_id')
    list_display = ('asm_id', 'get_user', 'get_profile_number', 'get_profile_address','area', 'zsm')
    
class AreaSalesManagerAdmin(GmModelAdmin):
    search_fields = ('state__state_name','rm__region')
    list_display = ('get_user', 'get_profile_number','get_state')
    
class DealerAdmin(GmModelAdmin):
    search_fields = ('dealer_id','asm__asm_id')
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
    list_display = ('id', 'product_type',\
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
                                 'Dealer Id': 'dealer_id__dealer_id',}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping
                        }
        return super(ListDispatchedProduct, self).changelist_view(request, extra_context=extra_context)


class Couponline(TabularInline):
    model = models.CouponData
    fields = ('unique_service_coupon', 'service_type', 'status', 'mark_expired_on', 'extended_date')
    extra = 0
    max_num = 0
    readonly_fields = ('unique_service_coupon','service_type', 'status', 'mark_expired_on', 'extended_date')


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
                    'actual_kms', 'status', 'service_type','service_advisor', 'associated_with')
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
                        continue # No 'admin_order_field', skip it
                    ordering.append(pfx + order_field)
                except (IndexError, ValueError):
                    continue # Invalid ordering specified, skip it.

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
            query_set=query_set.filter(feed_type__in=['ContainerTracker Feed', 'CTS Feed'])
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

'''Admin View for loyalty'''
class NSMAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('nsm_id', 'name', 'phone_number')
    list_display = ('nsm_id', 'name', 'email', 'phone_number','get_territory')

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
    list_display = ('asm_id', 'name', 'email',
                     'phone_number', 'get_state', 'nsm')
    
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
    list_display = ('name', 'email', 'phone_number','get_territory')

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
     

    

'''Admin View for loyalty'''
class NSMAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('nsm_id', 'name', 'phone_number')
    list_display = ('nsm_id', 'name', 'email', 'phone_number','get_territory')

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
    list_display = ('asm_id', 'name', 'email',
                     'phone_number', 'get_state', 'nsm')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('asm_id',)
        form = super(ASMAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.phone_number = utils.mobile_format(obj.phone_number)
        super(ASMAdmin, self).save_model(request, obj, form, change)

         
class DistributorForm(forms.ModelForm):
#     distributor_id = forms.CharField(max_length=30,required=True)
    name_distributorship = forms.CharField(label = 'Name of Distributorship', max_length=300)
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    mobile1 = forms.CharField(max_length=15)
    mobile2 = forms.CharField(max_length=15)
    email = forms.CharField(max_length=50)
    email_Bajaj = forms.CharField(max_length=50)
    date_birth = forms.DateTimeField(label = 'Date of birth')
    profile = forms.ChoiceField(choices = PROFILE_CHOICES, required=True)
    image_url = forms.FileField(max_length=200, required=False)
    plot_no = forms.CharField(max_length=20)
    street_name = forms.CharField(max_length=30)
    locality = forms.CharField(max_length=30)
    city = forms.CharField(max_length=20)
    pincode = forms.CharField(max_length=15)
    phone_number = forms.CharField(max_length=15, label = 'Phone (Land line)')
    
    states = State.objects.all()
#     print states
#      op_status = models.CharField(verbose_name="Status",max_length=135, blank=False,choices=status_choices)
    states = forms.ChoiceField(choices =((st.state_code, st.state_name) for st in states ))
                                          
    # multiple_states = forms.ChoiceField(choices = ((st.state_code, st.state_name) \
    #                                         for st in states ), label = 'states')
#     state = forms.CharField(max_length = 20)
    districts = forms.CharField(max_length = 20)
    DISTRICTS= (
    ('R', 'kasargod'),
    ('B', 'Kannur'),
#     ('G', 'White'),
)
    districts = forms.MultipleChoiceField(choices = DISTRICTS)
    
    
    def image_tag(self):
        return u'<img src="{0}/{1}" width="200px;"/>'.format('/static', self.image_url)
    image_tag.short_description = 'User Image'
    image_tag.allow_tags = True
    
    
    
#     def save(self, commit=True):
#         extra_field = self.cleaned_data.get('extra_field', None)
#         # ...do something with extra_field here...
#         return super(YourModelForm, self).save(commit=commit)
#     
    
    class Meta:
        model = Distributor
        exclude = ['sent_to_sap', 'phone_number',
                   'user', 'mobile', 'profile', 'language', 'territory']
        
class DistributorAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    form = DistributorForm
    search_fields = ('name', 'email',)
    list_display = ('distributor_code', 'distributor_name', 'head', 'city', 'phone',
                    'mail')
    fieldsets = (
            ('User Information', {
              'fields': ('distributor_id','name_distributorship', 'first_name', 'last_name', 'mobile1',
                'mobile2', 'email', 'email_Bajaj', 'date_birth', 'profile', 'image_url',)
            }),
            ('Location', {
              'fields': ('plot_no', 'locality','phone_number','street_name','city',
               'pincode')
            }),
            ('Territory', {
              'fields': ( 'states','districts')
            }),
          )
   
#     readonly_fields = ('image_tag',)
    
    
    def save_model(self, request, obj, form, Change):
#         print "teeena"
        # try:
        #     distributor = Distributor.objects.filter()[0]
        #     obj.distributor_id = str(int(distributor.distributor_id) + \
        #                             constants.DISTRIBUTOR_SEQUENCE_INCREMENT)
        # except:
        #     obj.distributor_id = str(constants.DISTRIBUTOR_SEQUENCE)
#         print request
#         print obj

        super(DistributorAdmin, self).save_model(request, obj, form, Change)
        try:
            send_email(sender = constants.FROM_EMAIL_ADMIN, receiver = obj.email, 
                   subject = constants.ADD_DISTRIBUTOR_SUBJECT, body = '',
                   message= constants.ADD_DISTRIBUTOR_MESSAGE)
        except Exception as e:
            print e
            logger.error('Mail is not sent. Exception occurred',e)
    
    def distributor_code(self, obj):
        print obj.distributor_id,"idddddddddddddddd"
        return obj.distributor_id
    distributor_code.admin_order_field = 'distributor_id'
    
    def distributor_name(self, obj):
        print self,"selffffffffffffffff"
        print obj.name
#         print 
#         print self.cleaned_data.get('name_distributorship'),"dbhjbsd"
        return obj.name
    distributor_name.short_description = 'Name of Distributorship'
    
    def head(self,obj):
        return obj.user.user.first_name
    head.short_description = 'Distributor Head'
    
    def city(self,obj):

        return obj.city
    city.short_description = 'locality'
    
    def phone(self,obj):
        return obj.phone_number
    phone.short_description = 'Phone/ Mobile'
    
    def mail(self, obj):
        return obj.email
    mail.short_description = 'Email'
    
    def staff_status(self, obj):
        if obj.user.user.is_staff == True:
            return '<html><img src = /static/img/active.gif></html>'
        else:
            return '<html><img src = /static/img/not_active.gif></html>'
    staff_status.allow_tags = True
    
    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set=query_set.filter(state=asm_state_list)
        return query_set

    def changelist_view(self, request, extra_context=None):
        return super(DistributorAdmin, self).changelist_view(request)
    
class DistributorSalesRepForm(forms.ModelForm):
    class Meta:
        model = get_model('DistributorSalesRep')
        exclude = ['distributor']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DistributorSalesRepForm, self).__init__(*args, **kwargs)
        
class DSRScorecardReportAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ()
    list_display = ()
        
class DistributorSalesRepAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('distributor_sales_code', )
    list_display = ('sales_representative_code', 'sales_representative_name', 'is_active')
    form = DistributorSalesRepForm
    
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
        if DistributorStaff.objects.filter(user__user = request.user).exists():
            distributorstaff = DistributorStaff.objects.get(user__user = request.user)
            obj.distributor = Distributor.objects.get(id = distributorstaff.distributor.id)
        else:
            obj.distributor = Distributor.objects.get(user__user = request.user)
        try:
            dsr = DistributorSalesRep.objects.filter()[0]
            obj.distributor_sales_code = str(int(dsr.distributor_sales_code) + \
                                            constants.DSR_SEQUENCE_INCREMENT)
        except:
            obj.distributor_sales_code = str(constants.DSR_SEQUENCE)
        super(DistributorSalesRepAdmin, self).save_model(request, obj, form, change)
        try:
            send_email(sender = constants.FROM_EMAIL_ADMIN, receiver = obj.email, 
                   subject = constants.ADD_DSR_SUBJECT, body = '',
                   message= constants.ADD_DSR_MESSAGE)
        except Exception as e:
            logger.error('Mail is not sent. Exception occurred',e)
            
    def sales_representative_code(self, obj):
        return obj.distributor_sales_code
    
    def sales_representative_name(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    
    def distributor_code(self, obj):
        return obj.distributor.distributor_code
    
    def distributor_name(self, obj):
        return obj.distributor.name
    
class DistributorStaffForm(forms.ModelForm):
    class Meta:
        model = get_model('DistributorStaff')
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DistributorStaffForm, self).__init__(*args, **kwargs)
        self.fields['distributor'].queryset = Distributor.objects.filter(user_id = self.request.user.id)
    
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
            send_email(sender = constants.FROM_EMAIL_ADMIN, receiver = obj.email, 
                   subject = constants.ADD_DISTRIBUTOR_STAFF_SUBJECT, body = '',
                   message= constants.ADD_DISTRIBUTOR_STAFF_MESSAGE)
        except Exception as e:
            logger.error('Mail is not sent. Exception occurred',e)
    
    def staff_name(self, obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    
class RetailerForm(forms.ModelForm):
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
    search_fields = ('retailer_name', 'retailer_town', 'billing_code','territory')
    list_display = ('retailer_code', 'billing_code', 'name', 'contact', 'city','phone',
                    'mail','status')
    exclude = []
    
    def pincode(self, obj):
        return obj.user.pincode
    pincode.admin_order_field = 'user__pincode'
    
    def billcode(self,obj):
        return obj.billing_code
    billcode.short_description = 'Retailer billing code'
    
    def name(self,obj):
        return obj.retailer_name
    name.short_description = 'Name of the shop'
    
    def contact(self,obj):
        return obj.user.user.first_name + ' ' + obj.user.user.last_name
    contact.short_description = 'Contact Person'
    
    def city(self, obj):
        return obj.retailer_town
    city.short_description = 'locality'
    
    def phone(self, obj):
        return obj.user.phone_number + ' ' + obj.mobile
    phone.short_description = 'Phone / Mobile'
    
    def mail(self, obj):
        return obj.email
    mail.short_description = 'Email'
    
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(RetailerAdmin, self).get_form(request, obj, **kwargs)
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)
        return ModelFormMetaClass
    
    def get_actions(self, request):
        #in case of administrator only, grant him the approve retailer option
        if self.param.groups.filter(name__in =['SuperAdmins', 'Admins', 'AreaSalesManagers']).exists():
            self.actions.append('approve')
        actions = super(RetailerAdmin, self).get_actions(request)
        return actions
    
    def queryset(self, request):
        query_set = self.model._default_manager.get_query_set()
        if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set=query_set.filter(state=asm_state_list)
        return query_set

    def changelist_view(self, request, extra_context=None):
        self.param = request.user
        return super(RetailerAdmin, self).changelist_view(request)
    
    def approve(self, request, queryset):
        queryset.update(approved=constants.STATUS['APPROVED'])
        for retailer in queryset:
            try:
                send_email(sender = constants.FROM_EMAIL_ADMIN, receiver = retailer.email, 
                       subject = constants.APPROVE_RETAILER_SUBJECT, body = '',
                       message = constants.APPROVE_RETAILER_MESSAGE)
            except Exception as e:
                logger.error('Mail is not sent. Exception occurred ',e)
    approve.short_description = 'Approve Selected Retailers'
    
    
#     def save_model(self, request, obj, form, change):
#         print request.user.groups.all()
# #         if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
#         if request.user.groups.filter(name__in=[Roles.DISTRIBUTORS,Roles.DISTRIBUTORSALESREP]).exists():
# #         if self.param.groups.filter(name__in =['Distributors','DisitrbutorSalesReps']).exists():
#             obj.approved = constants.STATUS['WAITING_FOR_APPROVAL']
#             #get latest retailer code, add increment and assign it, else assign the sequence first number
#             try:
#                 retailer = Retailer.objects.filter().order_by("-id")[0]
#                 obj.retailer_code = str(int(retailer.retailer_code) + \
#                                         constants.RETAILER_SEQUENCE_INCREMENT)
#             except:
#                 obj.retailer_code = str(constants.RETAILER_SEQUENCE)
#                 
#           
#     #         if request.user.groups.filter(name=Roles.DISTRIBUTORSALESREP,Roles.DISTRIBUTORS).exists():
#             
#             # if dsr is added by distributorstaff, then show the concerned distributor of distributorstaff
#             # else show the distributor
#             # if DistributorStaff.objects.filter(user__user = request.user).exists():
#             #     distributorstaff = DistributorStaff.objects.get(user__user = request.user)
#             #     obj.distributor = Distributor.objects.get(id = distributorstaff.distributor.id)
#             # else:
#     #         obj.distributor = Distributor.objects.get(user__user = request.user)
#             super(RetailerAdmin, self).save_model(request, obj, form, change) 
#     
    
    
    def save_model(self, request, obj, form, change):
        
        print request.user.groups.all()
#         if request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
        if request.user.groups.filter(name__in=[Roles.DISTRIBUTORS,Roles.DISTRIBUTORSALESREP,Roles.SUPERADMINS]).exists():
#         if self.param.groups.filter(name__in =['Distributors','DisitrbutorSalesReps']).exists():
            obj.approved = constants.STATUS['WAITING_FOR_APPROVAL']
        
#         obj.approved = constants.STATUS['WAITING_FOR_APPROVAL']
        #get latest retailer code, add increment and assign it, else assign the sequence first number
            try:
                retailer = Retailer.objects.filter()[0]
                obj.retailer_code = str(int(retailer.retailer_code) + \
                                        constants.RETAILER_SEQUENCE_INCREMENT)
            except:
                obj.retailer_code = str(constants.RETAILER_SEQUENCE)
            # if dsr is added by distributorstaff, then show the concerned distributor of distributorstaff
            # else show the distributor
            
#             if DistributorStaff.objects.filter(user__user = request.user).exists():
#                 distributorstaff = DistributorStaff.objects.get(user__user = request.user)
#                 obj.distributor = Distributor.objects.get(id = distributorstaff.distributor.id)
#             else:
#                 obj.distributor = Distributor.objects.get(user__user = request.user)
            super(RetailerAdmin, self).save_model(request, obj, form, change)
        
    def status(self, obj):
        #Added retailer by distributor/distributorstaff must be approved by the ASM/admin
        #he can also be rejected on some conditions
        if obj.approved == constants.STATUS['APPROVED']:
            return 'Approved'
        elif obj.approved == constants.STATUS['WAITING_FOR_APPROVAL'] :
            if self.param.groups.filter(name__in = \
                                    ['SuperAdmins', 'Admins', 'AreaSalesManagers']).exists():
                
                reject_button = "<a  class='btn btn-success' data-toggle='modal'  href=\"/admin/retailer/approve_retailer/retailer_id/"+str(obj.id)+"\">Approve</a>&nbsp;<input type=\"button\"  class='btn btn-danger' data-toggle='modal'  id=\"button_reject\" value=\"Reject\" onclick=\"popup_reject(\'"+str(obj.id)+"\',\'"+obj.retailer_name+"\',\'"+obj.email+"\',\'"+obj.distributor.name+"\'); return false;\">"
#                 reject_button = "<input type=\"button\" id=\"button_reject\" value=\"Reject\" onclick=\"popup_reject(\'"+str(obj.id)+"\',\'"+obj.retailer_name+"\',\'"+obj.email+"\',\'"+obj.distributor.name+"\'); return false;\">"
                return mark_safe(reject_button)
            else:
                return 'Waiting for approval'
        elif obj.approved == constants.STATUS['REJECTED'] :
            if self.param.groups.filter(name__in =['SuperAdmins', 'Admins', 'AreaSalesManagers']).exists():
                return 'Rejected'
            else:
                if self.param.groups.filter(name__in =['Distributors', 'DistributorStaffs']).exists():
                    rejected_reason = "<input type=\"button\" value=\"Rejected Reason\" onclick=\"popup_rejected_reason(\'"+str(obj.id)+"\',\'"+obj.retailer_name+"\',\'"+obj.rejected_reason+"\'); return false;\">"
                    return mark_safe(rejected_reason)
    status.allow_tags = True
    
class CollectionAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('retailer',)
    list_display = ('retailer', 'payment_date','payment_mode','payment_amount','invoice_date','invoice_amount','invoice_number')
    
class SparePartMasterAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number', 'description',
                     'product_type__product_type')
    list_display = ('part_number', 'description',
                    'part_model', 'price')
    
    def price(self, obj):
        price = SparePartPoint.objects.get(part_number = obj.id)
        return price.price
    
class PartModelAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('name',)
    list_display = ('name', 'active')
    
class CategoriesAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('category_name',)
    list_display = ('category_name','active',)
    
# class SubCategoriesAdmin(GmModelAdmin):
#     groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
#     search_fields = ('subcategory_name', 'category')
#     list_display = ('subcategory_name', 'category', 'active')
    
class PartPricingAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    search_fields = ('part_number', 'description')
    list_display = ('part_no', 'Part_Description','Category', 'Applicable_Model',
                    'Price', 'Available', 'Pending',
                    'Current', 'active')
    
    def part_no(self, obj):
        return obj.part_number
    part_no.short_description='Parts #'
    part_no.admin_order_field='part_number'
    
    def Part_Description(self, obj):
        return obj.description
    Part_Description.short_description='Part Description'
    
    def Category(self, obj):
        return obj.subcategory
    Category.short_description='Category'
    
    def Applicable_Model(self, obj):
        return obj.subcategory.part_model
    Applicable_Model.short_description='Applicable_Model'
    
    def Price(self, obj):
        return obj.mrp
    Price.short_description='Price'
    
    def Available(self, obj):
        return obj.available_quantity
    Available.short_description='Available Qut.'
    
    def Pending(self, obj):
        return '0'
    Pending.short_description='Pending Order Qut.'
    
    def Current(self, obj):
        return obj.current_month_should
    Current.short_description='Current Month should'
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("price_list",)
        form = super(PartPricingAdmin, self).get_form(request, obj, **kwargs)
        return form
    
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
            self.list_display=('part_number', 'points', 'valid_from',
                    'valid_till', 'territory', 'price', 'MRP')
        else:
            self.list_display=('part_number', 'points', 'valid_from',
                    'valid_till', 'territory')
        return super(SparePartPointAdmin, self).changelist_view(request, extra_context=extra_context)
    
    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser and not request.user.groups.filter(name=Roles.LOYALTYSUPERADMINS).exists():
            self.exclude = ('price', 'MRP')
        form = super(SparePartPointAdmin, self).get_form(request, obj, **kwargs)
        return form
    
class OrderPartAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    # search_fields = ('retailer_name',)
    # list_display = ('retailer', 'dsr', 'part', 'price', 'quantity', 'total_price',
    #                 'accept', 'order_date')
    # list_filter = ['order_date']
    
    def get_actions(self, request):
        #in case of administrator only, grant him the approve retailer option
        # if self.param.groups.filter(name__in =['distributors']).exists():
        self.actions.append('accept')
        actions = super(OrderPartAdmin, self).get_actions(request)
        return actions
    
    def accept(self, request, queryset):
        queryset.update(accept = True)
    accept.short_description = 'Accept selected orders'
    
class SparePartline(TabularInline):
    model = models.AccumulationRequest.upcs.through

class ProductCatalogAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    list_filter = ('is_active',)
    search_fields = ('partner__partner_id', 'product_id',
                    'brand', 'model', 'category',
                    'sub_category')

    list_display = ('partner', 'product_id', 'points', 'price',
                    'description', 'variation',
                    'brand', 'model', 'category',
                    'sub_category')
    readonly_fields = ('image_tag',)

class PartnerAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS]
    list_filter = ('partner_type',)
    search_fields = ('partner_id', 'name', 'partner_type')

    list_display = ('partner_id', 'name' , 'address','partner_type')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('partner_id',)
        form = super(PartnerAdmin, self).get_form(request, obj, **kwargs)
        return form

class AccumulationRequestAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.AREASPARESMANAGERS, Roles.NATIONALSPARESMANAGERS, Roles.LOYALTYADMINS, Roles.LOYALTYSUPERADMINS]
    search_fields = ('member__mechanic_id', 'upcs__unique_part_code')
    list_display = ( 'member',  'get_mechanic_name', 'get_mechanic_district',
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
            asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set=query_set.filter(member__state=asm_state_list)

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
    list_display = ('get_mechanic_id','first_name', 'date_of_birth',
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
            asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set=query_set.filter(state=asm_state_list)

        return query_set

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('mechanic_id','form_status', 'sent_sms', 'total_points', 'sent_to_sap', 'permanent_id', 'download_detail')
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
    list_display = ('member',  'get_mechanic_name',
                     'delivery_address', 'get_mechanic_pincode',
                     'get_mechanic_district', 'get_mechanic_state',
                     'product', 'created_date','due_date',
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
            query_set=query_set.filter(is_approved=True, packed_by=request.user.username)
        elif request.user.groups.filter(name=Roles.LPS).exists():
            query_set=query_set.filter(status__in=constants.LP_REDEMPTION_STATUS, partner__user=request.user)
        elif request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set=query_set.filter(member__state=asm_state_list)

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
        form.current_user=request.user
        return form

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status!='Rejected':
            date = loyalty.set_date("Redemption", obj.status)
            obj.due_date = date['due_date']
            obj.expected_delivery_date = date['expected_delivery_date']
            obj.resolution_flag = False
        if 'status' in form.changed_data:
            if obj.status=='Approved':
                obj.is_approved=True
                obj.packed_by=obj.partner.user.user.username
                obj.approved_date=datetime.datetime.now()
            elif obj.status in ['Rejected', 'Open'] :
                obj.is_approved=False
                obj.packed_by=None
            elif obj.status=='Shipped':
                obj.shipped_date=datetime.datetime.now()
            elif obj.status=='Delivered':
                obj.delivery_date=datetime.datetime.now()
        if 'status' in form.changed_data:
            if obj.status=='Approved' and obj.refunded_points:
                loyalty.update_points(obj.member, redeem=obj.product.points)
                obj.refunded_points = False
            elif obj.status=='Rejected' and not obj.refunded_points:
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
    list_display = ('member',  'get_mechanic_name',
                     'delivery_address', 'get_mechanic_pincode',
                     'get_mechanic_district', 'get_mechanic_state',
                     'created_date','due_date', 'expected_delivery_date', 'status', 'partner')
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
                obj.packed_by=obj.partner.user.user.username
        if 'status' in form.changed_data:
            if obj.status=='Shipped':
                obj.shipped_date=datetime.datetime.now()
            elif obj.status=='Delivered':
                obj.delivery_date=datetime.datetime.now()
        date = loyalty.set_date("Welcome Kit", obj.status)
        obj.due_date = date['due_date']
        obj.expected_delivery_date = date['expected_delivery_date']
        obj.resolution_flag = False
        super(WelcomeKitAdmin, self).save_model(request, obj, form, change)
        if 'status' in form.changed_data and obj.status=="Shipped":
            loyalty.send_welcome_kit_delivery(obj)
        if 'partner' in form.changed_data and obj.partner:
            loyalty.send_welcome_kit_mail_to_partner(obj)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('resolution_flag','packed_by')
        form = super(WelcomeKitAdmin, self).get_form(request, obj, **kwargs)
        form.current_user=request.user
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
            query_set=query_set.filter(packed_by=request.user.username)
        elif request.user.groups.filter(name=Roles.LPS).exists():
            query_set=query_set.filter(status__in=constants.LP_REDEMPTION_STATUS, partner__user=request.user)
        elif request.user.groups.filter(name=Roles.AREASPARESMANAGERS).exists():
            asm_state_list=models.AreaSparesManager.objects.get(user__user=request.user).state.all()
            query_set=query_set.filter(member__state=asm_state_list)

        return query_set

class LoyaltySlaAdmin(GmModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
        'status','action',
        ('reminder_time', 'reminder_unit'),
        ('resolution_time', 'resolution_unit'), 
        ('member_resolution_time','member_resolution_unit'))
        }),
        )    
    def reminder_time(self):
        return str(self.reminder_time) + ' ' + self.reminder_unit
    
    def resolution_time(self):
        return str(self.resolution_time) + ' ' + self.resolution_unit
    
    def member_resolution_time(self):
        return str(self.member_resolution_time) + ' ' + self.member_resolution_unit

    list_display = ('status','action', reminder_time, resolution_time, member_resolution_time)
    
class ConstantAdmin(GmModelAdmin):
    search_fields = ('constant_name',  'constant_value')
    list_display = ('constant_name',  'constant_value',)
    

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
    search_fields = ('indent_num','transporter__user__user__username')
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
        self.exclude = ('status','sent_to_sap')
        form = super(ContainerLRAdmin, self).get_form(request, obj, **kwargs)
        form.current_user=request.user
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
    #brand_admin.register(get_model("DistributorStaff", brand), DistributorStaffAdmin)
    brand_admin.register(get_model("DistributorSalesRep", brand), DistributorSalesRepAdmin)
    brand_admin.register(get_model("Retailer", brand), RetailerAdmin)
    brand_admin.register(get_model("PartModel", brand), PartModelAdmin)
    brand_admin.register(get_model("Categories", brand), CategoriesAdmin)
    #brand_admin.register(get_model("SubCategories", brand), SubCategoriesAdmin)
    brand_admin.register(get_model("PartPricing", brand), PartPricingAdmin)
    brand_admin.register(get_model("OrderPart", brand), OrderPartAdmin)
    
    brand_admin.register(get_model("NationalSparesManager", brand), NSMAdmin)
    brand_admin.register(get_model("AreaSparesManager", brand), ASMAdmin)
    brand_admin.register(get_model("NationalSalesManager", brand), NationalSalesManagerAdmin)
#     brand_admin.register(get_model("AreaSalesManager", brand), AreaSalesManagerAdmin)
    brand_admin.register(get_model("DSRScorecardReport", brand), DSRScorecardReportAdmin)
    #brand_admin.register(get_model("SparePartMasterData", brand), SparePartMasterAdmin)
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
    #Disable the delete action throughout the admin site
    brand_admin.disable_action('delete_selected')
    return brand_admin

brand_admin = get_admin_site_custom(GmApps.BAJAJ)
