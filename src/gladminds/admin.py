import tablib
import datetime
import json
from django.contrib.admin.views.main import ChangeList, ORDER_VAR
from django.contrib import admin
from suit.admin import SortableTabularInline, SortableModelAdmin
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, \
    EnclosedInput, LinkedSelect, AutosizedTextarea
from suit.widgets import NumberInput
from suit.admin import SortableModelAdmin
from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.db import connections
from django.db import models
from django.contrib.admin.models import LogEntry
from models.common import GladMindUsers, ProductTypeData, \
    BrandData, ProductData, CouponData, MessageTemplate,\
    UploadProductCSV, CustomerTempRegistration
from gladminds.aftersell.models.common import \
    RegisteredDealer, ServiceAdvisorDealerRelationship, ServiceAdvisor
from gladminds.aftersell.models.logs import AuditLog, DataFeedLog
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export import fields, widgets
from import_export import resources
from gladminds.models.common import EmailTemplate
from gladminds.aftersell.models.common import ASCSaveForm, Feedback
from gladminds.afterbuy.models.common import UserNotification
from gladminds import utils


############################BRAND AND PRODUCT ADMIN##########################
class ProductTypeDataInlineForm(ModelForm):

    class Meta:
        widgets = {
            'product_name': EnclosedInput(prepend='icon-tags',
                                          attrs={'class': 'input-large'}),
            'product_type': EnclosedInput(
                attrs={'class': 'input-large'}),
        }


class ProductTypeDataInline(SortableTabularInline):
    form = ProductTypeDataInlineForm
    model = ProductTypeData
    fields = ('product_name', 'product_type')
#     readonly_fields= ('product_name','product_type')
    extra = 1
    max_num = 0


class BrandForm(ModelForm):

    class Meta:
        widgets = {
            'brand_id': EnclosedInput(prepend='icon-asterisk', attrs={'class': 'input-small'}),
            'brand_name': AutosizedTextarea,
        }


class BrandAdmin(ModelAdmin):
    form = BrandForm
    search_fields = ('brand_id', 'brand_name')
    list_display = ('image_tag', 'brand_id', 'brand_name', 'products')
    inlines = (ProductTypeDataInline,)
#     readonly_fields = ('image_tag',)

    def products(self, obj):
        return len(obj.producttypedata_set.all())


#######################################################################

##########################DEALER AND SA ADMIN###########################
class SAInlineForm(ModelForm):

    class Meta:
        widgets = {
            'service_advisor_id': EnclosedInput(
                attrs={'class': 'input-large'}),
            'name': EnclosedInput(prepend='icon-user',
                                  attrs={'class': 'input-large'}),
            'phone_number': EnclosedInput(
                attrs={'class': 'input-large'}),
        }


class SAInline(SortableTabularInline):
    form = SAInlineForm
    model = ServiceAdvisor
    fields = ('service_advisor_id', 'name', 'phone_number')
    extra = 1


class DealerForm(ModelForm):

    class Meta:
        widgets = {
            'dealer_id': EnclosedInput(prepend='icon-asterisk',
                                       attrs={'class': 'input-small'}),
            'address': AutosizedTextarea,
        }


class DealerAdmin(ModelAdmin):
    form = DealerForm
    search_fields = ('dealer_id',)
    list_display = ('dealer_id', 'address')
#    list_display = ('dealer_id', 'address', 'service_advisor_id')
#     inlines = (SAInline,)
#
#     def serviceadvisor(self, obj):
#         return len(obj.serviceadvisor_set.all())


class ServiceAdvisorAdmin(ModelAdmin):
    search_fields = (
        'service_advisor_id', 'phone_number', 'name', 'dealer_id__dealer_id')
    list_display = ('name', 'service_advisor_id', 'phone_number')
    exclude = ('order',)

    def dealer_id(self, obj):
        return u'<a href="/gladminds/registereddealer/%s/">%s</a>' % (obj.dealer_id.pk, obj.dealer_id)
    dealer_id.allow_tags = True


class ServiceAdvisorDealerAdmin(ModelAdmin):
    search_fields = ('dealer_id__dealer_id', 'service_advisor_id__service_advisor_id',
                     'service_advisor_id__name', 'service_advisor_id__phone_number')

    list_display = (
        'dealer_id', 'name', 'service_advisor_ids', 'phone_number', 'status')

    def dealer_id(self, obj):
        return u'<a href="/gladminds/registereddealer/%s/">%s</a>' % (obj.dealer_id.pk, obj.dealer_id)
    dealer_id.allow_tags = True

    def service_advisor_ids(self, obj):
        sa_obj = ServiceAdvisor.objects.filter(
            service_advisor_id=obj.service_advisor_id.service_advisor_id)
        return u'<a href="/aftersell/serviceadvisor/%s/">%s</a>' % (obj.service_advisor_id.pk,
                                                                    sa_obj[0].service_advisor_id)
    service_advisor_ids.allow_tags = True

    def name(self, obj):
        sa_obj = ServiceAdvisor.objects.filter(
            service_advisor_id=obj.service_advisor_id.service_advisor_id)
        if len(sa_obj) > 0:
            return sa_obj[0].name
        return None

    def phone_number(self, obj):
        sa_obj = ServiceAdvisor.objects.filter(
            service_advisor_id=obj.service_advisor_id.service_advisor_id)
        if len(sa_obj) > 0:
            return sa_obj[0].phone_number
        return None

    def changelist_view(self, request, extra_context=None):
        extra_context = {'searchable_fields':"('dealer_id', 'service_advisor_id', 'service_advisor__name',"
                        "'service_advisor_phone_number')"}
        return super(ServiceAdvisorDealerAdmin, self).changelist_view(request, extra_context=extra_context)

##############CUSTMERDATA AND GLADMINDS USER ADMIN###################
class GladMindUserForm(ModelForm):

    class Meta:
        widgets = {
            'gladmind_customer_id': EnclosedInput(prepend='icon-asterisk',
                                                  attrs={'class': 'input-small'}),
            'customer_name': EnclosedInput(prepend='icon-user',
                                           attrs={'class': 'input-small'}),
        }


class GladMindUserAdmin(ModelAdmin):
    form = GladMindUserForm
    search_fields = (
        'gladmind_customer_id', 'customer_name', 'phone_number', 'email_id')
    list_display = ('gladmind_customer_id', 'customer_name',
                    'email_id', 'phone_number', 'date_of_registration')

    def date_of_registration(self, obj):
        return obj.registration_date.strftime("%d %b %Y")


class Couponline(SortableTabularInline):
    model = CouponData
    fields = ('unique_service_coupon', 'valid_days', 'valid_kms',
              'status', 'service_type', 'sa_phone_number')
    extra = 0
    max_num = 0
    readonly_fields = ('unique_service_coupon', 'valid_days',
                       'valid_kms', 'status', 'service_type', 'sa_phone_number')


class ProductDataAdmin(ModelAdmin):
    search_fields = ('^vin', '^sap_customer_id', 'customer_phone_number__customer_name',
                     '^customer_phone_number__phone_number')
    list_display = ('vin', 'sap_customer_id', "UCN", 'customer_name',
                    'customer_phone_number', 'product_purchase_date')
    inlines = (Couponline,)
    exclude = ('order',)
    list_per_page = 50

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        utils.get_search_query_params(request, self)
        query_set = self.model._default_manager.get_query_set()
        query_set = query_set.select_related('').prefetch_related('customer_phone_number')
        query_set = query_set.filter(product_purchase_date__isnull=False)
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            query_set = query_set.order_by(*ordering)
        return query_set

    def UCN(self, obj):
        ucn_list = []
        for coupon in CouponData.objects.filter(vin=obj.id):
            ucn_list.append(coupon.unique_service_coupon)
        return ' | '.join([str(ucn) for ucn in ucn_list])

    def customer_name(self, obj):
        gm_user_obj = GladMindUsers.objects.get(
            phone_number=obj.customer_phone_number)
        name = ''
        if gm_user_obj:
            name = gm_user_obj.customer_name
        return name
    customer_name.allow_tags = True

    def service_type(self, obj):
        gm_coupon_data_obj = CouponData.objects.filter(vin=obj.id)
        coupon_service_type = ''
        if gm_coupon_data_obj:
            coupon_service_type = " | ".join(
                [str(obj.service_type) for obj in gm_coupon_data_obj])
        return coupon_service_type

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('customer_phone_number',)
        form = super(ProductDataAdmin, self).get_form(request, obj, **kwargs)
        return form
    
    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Vin' : '^vin',
                                 'Dealer Id': '^dealer_id__dealer_id',
                                 'Sap Customer ID':'^sap_customer_id',
                                 'Customer Name': 'customer_phone_number__customer_name',
                                 'Customer Phone Number': 'customer_phone_number__phone_number'}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Vin, Sap Customer Id, Customer Phone Number and Customer Name'
                        }
        return super(ProductDataAdmin, self).changelist_view(request, extra_context=extra_context)

class CouponResource(resources.ModelResource):
#     def get_export_headers(self):
#         headers = [field.column_name for field in self.get_fields() if field.column_name is not 'order']
#         return headers

    def export(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)
        for obj in queryset.iterator():
            vin_number = str(obj.vin)
            obj.vin = ProductData(vin_number)
            print obj.vin
            #sa_phone_number = str(obj.sa_phone_number)
            #obj.sa_phone_number = ServiceAdvisor(sa_phone_number)
            data.append(self.export_resource(obj))
        return data

    class Meta:
        model = CouponData


#class CouponAdmin(ExportMixin, ModelAdmin):
class CouponAdmin(ModelAdmin):
#    resource_class = CouponResource
    #list_filter = ('status',)
    search_fields = (
        '^unique_service_coupon', '^vin__vin', 'status')
    list_display = ('vin', 'unique_service_coupon', "actual_service_date",
                    'actual_kms', 'valid_days', 'valid_kms', 'status', "service_type")
    exclude = ('order',)

    def suit_row_attributes(self, obj):
        class_map = {
            '1': 'success',
            '2': 'warning',
            '3': 'error',
            '4': 'info',
            '5': 'error'
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Unique Service Coupon' : '^unique_service_coupon',
                                 'Vin': '^vin__vin',
                                 'Status': 'status'}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Unique Service Coupon, Vin and Status'
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
                search_value = str(utils.COUPON_STATUS[request.GET["q"]])
                request.GET["q"] = search_value
                request.META['QUERY_STRING'] = search_value
            except Exception:
                pass
        qs = self.model._default_manager.get_query_set()
        qs = qs.select_related('').prefetch_related('vin')
        '''
            This if condition only for landing page
        '''
        if not request.GET and not request.POST and request.path == "/gladminds/coupondata/":
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

####################################################################

###########################AUDIT ADMIN########################


class AuditLogAdmin(ModelAdmin):
    search_fields = ('status', 'sender', 'reciever', 'action')
    list_display = (
        'date', 'action', 'message', 'sender', 'reciever', 'status')

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
##############################################################

######################Message Template#############################


class MessageTemplateAdmin(ModelAdmin):
    search_fields = ('template_key', 'template')
    list_display = ('template_key', 'template', 'description')
    readonly_fields = ('template_key',)
###################################################################

######################Email Template#############################


class EmailTemplateAdmin(ModelAdmin):
    search_fields = ('template_key', 'sender', 'reciever')
    list_display = ('template_key', 'sender', 'recievers', 'subject')
    readonly_fields = ('template_key',)

    def recievers(self, obj):
        return ' | '.join(obj.reciever.split(','))

###################################################################

###########################AUDIT ADMIN########################

class FeedLogAdmin(ModelAdmin):
    search_fields = ('status', 'data_feed_id', 'action')
    list_display = ('timestamp', 'feed_type', 'action',
                    'total_data_count', 'success_data_count',
                    'failed_data_count', 'feed_remarks')

    def feed_remarks(self, obj):
        if obj.remarks and obj.file_location:
            remarks = json.loads(obj.remarks)
            update_remark = ''
            for remark, occurence in remarks.iteritems():
                update_remark = "[ {0} : {1} ].  ".format(remark, occurence)

            update_remark = update_remark[:100] + u'<a href="{0}">{1}</a>'.\
                                            format(obj.file_location, " For More...")
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


##############################################################
##################Custom Model Defined########################

class DispatchedProduct(ProductData):

    class Meta:
        proxy = True

class ListDispatchedProduct(ModelAdmin):
    search_fields = ('^vin', '^dealer_id__dealer_id')
    list_display = (
        'vin', 'product_type', 'engine', 'UCN', 'dealer_id', "invoice_date")
    exclude = ('order',)
    list_per_page = 50

    def queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        utils.get_search_query_params(request, self)
        query_set = self.model._default_manager.get_query_set()
        query_set = query_set.select_related('').prefetch_related('customer_phone_number', 'dealer_id', 'product_type')
#         query_set = query_set.filter(invoice_date__isnull=False)
        # TODO: this should be handled by some parameter to the ChangeList.
#        ordering = self.get_ordering(request)
#        if ordering:
#            query_set = query_set.order_by(*ordering)
        return query_set

    def UCN(self, obj):
        ucn_list = []
        for coupon in CouponData.objects.filter(vin=obj.id):
            ucn_list.append(coupon.unique_service_coupon)
        return ' | '.join([str(ucn) for ucn in ucn_list])
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('customer_phone_number',)
        form = super(ListDispatchedProduct, self).get_form(request, obj, **kwargs)
        return form

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Vin' : '^vin',
                                 'Dealer Id': '^dealer_id__dealer_id',}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Vin and  Dealer id'}
        return super(ListDispatchedProduct, self).changelist_view(request, extra_context=extra_context)
##############################################################
#########################ASCSaveForm#########################


class ASCSaveFormAdmin(ModelAdmin):
    search_fields = (
        'name', 'phone_number', 'email', 'pincode',
        'address', 'status', 'timestamp', 'dealer_id')

    list_display = (
        'name', 'phone_number', 'email', 'status', 'timestamp')

    def suit_row_attributes(self, obj):
        class_map = {
            '1': 'success',
            '2': 'error'
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}

class CustomerTempRegistrationAdmin(ModelAdmin):
    search_fields = (
        'product_data__vin', 'new_customer_name', 'new_number', 'temp_customer_id', 'sent_to_sap')

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
        
##############################################################

class UserNotificationAdmin(ModelAdmin):

    list_display = (
        'user', 'message', 'notification_date', 'notification_read')

class UserFeedback(ModelAdmin):

    list_display = (
        'reporter', 'assign_to', 'message', 'subject', 'priority', 'type', 'status', 'created_date', 'modified_date')

##############################################################

admin.site.register(BrandData, BrandAdmin)
admin.site.register(DispatchedProduct, ListDispatchedProduct)
admin.site.register(ServiceAdvisor, ServiceAdvisorAdmin)
admin.site.register(
    ServiceAdvisorDealerRelationship, ServiceAdvisorDealerAdmin)
admin.site.register(RegisteredDealer, DealerAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
admin.site.register(DataFeedLog, FeedLogAdmin)
admin.site.register(GladMindUsers, GladMindUserAdmin)
admin.site.register(ProductData, ProductDataAdmin)
admin.site.register(CouponData, CouponAdmin)
admin.site.register(MessageTemplate, MessageTemplateAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(ASCSaveForm, ASCSaveFormAdmin)
admin.site.register(CustomerTempRegistration, CustomerTempRegistrationAdmin)
admin.site.register(UploadProductCSV)
admin.site.register(LogEntry)
admin.site.register(UserNotification, UserNotificationAdmin)
admin.site.register(Feedback, UserFeedback)
