from django.contrib.admin import AdminSite, TabularInline
from django.contrib.auth.models import User, Group
from django.contrib.admin import ModelAdmin
from suit.admin import SortableTabularInline
from django.contrib.admin.views.main import ChangeList, ORDER_VAR

from gladminds.bajaj.models import BrandProductCategory, ProductType,\
UserProfile, Dealer, AuthorizedServiceCenter,\
ServiceAdvisor, ProductData, CouponData, \
ASCTempRegistration, SATempRegistration, CustomerTempRegistration,\
SMSLog, EmailLog, DataFeedLog, MessageTemplate, EmailTemplate, SLA
from gladminds.core import utils

class BajajAdminSite(AdminSite):
    pass

class UserProfileAdmin(ModelAdmin):
    search_fields = ('user__username', 'phone_number')
    list_display = ('user', 'phone_number', 'status', 'address',
                    'state', 'country', 'pincode', 'date_of_birth', 'gender')
        
class DealerAdmin(ModelAdmin):
    search_fields = ('dealer_id',)
    list_display = ('dealer_id', 'user')
     
class DealerAdmin(ModelAdmin):
    search_fields = ('dealer_id',)
    list_display = ('dealer_id', 'user')

class AuthorizedServiceCenterAdmin(ModelAdmin):
    search_fields = ('asc_id', 'dealer__dealer_id')
    list_display = ('asc_id', 'user', 'dealer')

class ServiceAdvisorAdmin(ModelAdmin):
    search_fields = ('service_advisor_id', 'dealer__dealer_id', 'asc__asc_id')
    list_display = ('service_advisor_id', 'user', 'dealer', 'asc', 'status')

class BrandProductCategoryAdmin(ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'description')

class ProductTypeAdmin(ModelAdmin):
    search_fields = ('product_name', 'product_type')
    list_display = ('product_type_id', 'product_name',\
                    'product_type', 'image_url', 'is_active')

class DispatchedProduct(ProductData):

    class Meta:
        proxy = True

class ListDispatchedProduct(ModelAdmin):
    search_fields = ('^product_id', '^dealer_id__dealer_id')
    list_display = (
        'product_id', 'product_type', 'engine', 'UCN', 'dealer_id', "invoice_date")
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
        coupons = CouponData.objects.filter(product=obj.id)
        if coupons:
            return ' | '.join([str(ucn.unique_service_coupon) for ucn in coupons])
        else:
            return None
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ListDispatchedProduct, self).get_form(request, obj, **kwargs)
        return form

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Product Id' : '^product_id',
                                 'Dealer Id': '^dealer_id__dealer_id',}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Vin and  Dealer id'}
        return super(ListDispatchedProduct, self).changelist_view(request, extra_context=extra_context)


class Couponline(TabularInline):
    model = CouponData
    fields = ('unique_service_coupon', 'service_type', 'status', 'mark_expired_on', 'extended_date')
    extra = 0
    max_num = 0
    readonly_fields = ('unique_service_coupon','service_type', 'status', 'mark_expired_on', 'extended_date')


class ProductDataAdmin(ModelAdmin):
    search_fields = ('^product_id', '^customer_id', '^customer_phone_number',
                     '^customer_name')
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
        coupons = CouponData.objects.filter(product=obj.id)
        if coupons:
            return ' | '.join([str(ucn.unique_service_coupon) for ucn in coupons])
        else:
            return None

    def service_type(self, obj):
        gm_coupon_data_obj = CouponData.objects.filter(product=obj.id)
        coupon_service_type = ''
        if gm_coupon_data_obj:
            coupon_service_type = " | ".join(
                [str(obj.service_type) for obj in gm_coupon_data_obj])
        return coupon_service_type
    
    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Product Id' : '^product_id',
                                 'Customer ID':'^customer_id',
                                 'Customer Name': '^customer_name',
                                 'Customer Phone Number': '^customer_phone_number'}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Product Id, Customer Id, Customer Phone Number and Customer Name'
                        }
        return super(ProductDataAdmin, self).changelist_view(request, extra_context=extra_context)


class CouponAdmin(ModelAdmin):
    search_fields = (
        '^unique_service_coupon', '^product__product_id', 'status')
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
            sa = ServiceAdvisor.objects.filter(service_advisor_id=obj.service_advisor.service_advisor_id).select_related('dealer', 'authorizedservicecenter')[0]
            if sa.dealer:
                return sa.dealer.dealer_id + ' (D)'
            elif sa.asc:
                return sa.asc.asc_id + ' (A)'
            else:
                return None

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {'Unique Service Coupon' : '^unique_service_coupon',
                                 'Product Id': '^product__product_id',
                                 'Status': 'status'}
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Unique Service Coupon, Product Id and Status'
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
        qs = qs.select_related('').prefetch_related('product')
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

class SMSLogAdmin(ModelAdmin):
    search_fields = ('status', 'sender', 'receiver', 'action')
    list_display = (
        'created_date', 'action', 'message', 'sender', 'receiver')
    
    def action(self, obj):
        return obj.action
    
    def has_add_permission(self, request):
        return False
    
class EmailLogAdmin(ModelAdmin):
    search_fields = ('subject', 'sender', 'receiver')
    list_display = (
        'created_date', 'subject', 'message', 'sender', 'receiver', 'cc')

class FeedLogAdmin(ModelAdmin):
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

class ASCTempRegistrationAdmin(ModelAdmin):
    search_fields = (
        'name', 'phone_number', 'email', 'dealer_id')

    list_display = (
        'name', 'phone_number', 'email', 'pincode',
        'address', 'timestamp', 'dealer_id')
    
class SATempRegistrationAdmin(ModelAdmin):
    search_fields = (
        'name', 'phone_number')

    list_display = (
        'name', 'phone_number', 'status')
     
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

class MessageTemplateAdmin(ModelAdmin):
    search_fields = ('template_key', 'template')
    list_display = ('template_key', 'template', 'description')

class EmailTemplateAdmin(ModelAdmin):
    search_fields = ('template_key', 'sender', 'receiver', 'subject')
    list_display = ('template_key', 'sender', 'receivers', 'subject')

    def receivers(self, obj):
        return ' | '.join(obj.receiver.split(','))

class SlaAdmin(ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
        'priority', ('response_time', 'response_unit'), ('reminder_time', 'reminder_unit'), ('resolution_time', 'resolution_unit'))
        }),
        )


brand_admin = BajajAdminSite(name='bajaj')

brand_admin.register(User)
brand_admin.register(Group)
brand_admin.register(UserProfile, UserProfileAdmin)

brand_admin.register(Dealer, DealerAdmin)
brand_admin.register(AuthorizedServiceCenter, AuthorizedServiceCenterAdmin)
brand_admin.register(ServiceAdvisor, ServiceAdvisorAdmin)

brand_admin.register(BrandProductCategory, BrandProductCategoryAdmin)
brand_admin.register(ProductType, ProductTypeAdmin)
brand_admin.register(DispatchedProduct, ListDispatchedProduct)
brand_admin.register(ProductData, ProductDataAdmin)
brand_admin.register(CouponData, CouponAdmin)

brand_admin.register(SMSLog, SMSLogAdmin)
brand_admin.register(EmailLog, SMSLogAdmin)
brand_admin.register(DataFeedLog, FeedLogAdmin)

brand_admin.register(ASCTempRegistration, ASCTempRegistrationAdmin)
brand_admin.register(SATempRegistration, SATempRegistrationAdmin)
brand_admin.register(CustomerTempRegistration, CustomerTempRegistrationAdmin)

brand_admin.register(EmailTemplate, EmailTemplateAdmin)
brand_admin.register(MessageTemplate, MessageTemplateAdmin)
brand_admin.register(SLA, SlaAdmin)


