from django.contrib.admin import AdminSite, TabularInline
from django.contrib.auth.models import User, Group
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList, ORDER_VAR
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin import DateFieldListFilter

from gladminds.bajaj import models
from gladminds.bajaj.services.loyalty import send_welcome_sms
from gladminds.core import utils, constants
from gladminds.core.loaders.module_loader import get_model
from gladminds.core.auth_helper import GmApps, Roles
from gladminds.core.admin_helper import GmModelAdmin

class BajajAdminSite(AdminSite):
    pass


class UserProfileAdmin(ModelAdmin):
    search_fields = ('user__username', 'phone_number')
    list_display = ('user', 'phone_number', 'status', 'address',
                    'state', 'country', 'pincode', 'date_of_birth', 'gender')
    
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
    search_fields = ('product_type',)
    list_display = ('id', 'product_type',\
                    'image_url', 'is_active')

class DispatchedProduct(models.ProductData):

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
        coupons = models.CouponData.objects.filter(product=obj.id)
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
    model = models.CouponData
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
            sa = models.ServiceAdvisor.objects.filter(service_advisor_id=obj.service_advisor.service_advisor_id).select_related('dealer', 'authorizedservicecenter')[0]
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
    
class ServiceDeskUserAdmin(ModelAdmin):
    list_display = ('user_profile', 'name', 'phone_number', 'email')

class NSMAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.ASMS, Roles.NSMS]
    search_fields = ('nsm_id', 'name', 'phone_number', 'territory')
    list_display = ('nsm_id', 'name', 'email', 'phone_number','territory')

class ASMAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.ASMS]
    search_fields = ('asm_id', 'nsm__name',
                     'phone_number', 'state')
    list_display = ('asm_id', 'name', 'email',
                     'phone_number', 'state', 'nsm')

class DistributorAdmin(GmModelAdmin):
    search_fields = ('distributor_id', 'asm__asm_id',
                     'phone_number', 'city')
    list_display = ('distributor_id', 'name', 'email',
                    'phone_number', 'city', 'asm')

class MechanicAdmin(GmModelAdmin):
    list_filter = ('form_status',)
    search_fields = ('mechanic_id',
                     'phone_number', 'first_name',
                     'state', 'district')
    list_display = ('mechanic_id','first_name', 'date_of_birth',
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

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('mechanic_id','form_status', 'sent_sms', 'total_points')
        form = super(MechanicAdmin, self).get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        if not obj.id:
            send_welcome_sms(obj)
            obj.sent_sms=True
        obj.phone_number=utils.mobile_format(obj.phone_number)
        super(MechanicAdmin, self).save_model(request, obj, form, change)    

class SparePartMasterAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.ASMS, Roles.NSMS, Roles.LOYALTYSUPERADMINS]
    search_fields = ('part_number', 'category',
                     'segment_type', 'supplier',
                     'product_type__product_type')
    list_display = ('part_number', 'description',
                    'product_type', 'category',
                    'segment_type',  'part_model', 'supplier')

class SparePartUPCAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.ASMS, Roles.NSMS, Roles.LOYALTYSUPERADMINS]
    search_fields = ('part_number__part_number', 'unique_part_code')
    list_display = ('unique_part_code', 'part_number')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('is_used',)
        form = super(SparePartUPCAdmin, self).get_form(request, obj, **kwargs)
        return form

class SparePartPointAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.ASMS, Roles.NSMS, Roles.LOYALTYSUPERADMINS]
    search_fields = ('part_number__part_number', 'points', 'territory')
    list_display = ('part_number', 'points', 'valid_from',
                    'valid_till', 'territory', 'price', 'MRP')

class SparePartline(TabularInline):
    model = models.AccumulationRequest.upcs.through

class AccumulationRequestAdmin(GmModelAdmin):
    groups_update_not_allowed = [Roles.ASMS, Roles.NSMS, Roles.LOYALTYSUPERADMINS]
    list_filter = (
        ('created_date', DateFieldListFilter),
    )
    search_fields = ('member__phone_number', 'points')
    list_display = ( 'member',  'get_mechanic_name', 'get_mechanic_city',
                     'asm', 'get_upcs', 'points',
                     'total_points', 'created_date')

    def get_mechanic_name(self, obj):
        return obj.member.first_name
    
    def get_mechanic_city(self, obj):
        return obj.member.district
    
    def get_upcs(self, obj):
        upcs = obj.upcs.all()
        if upcs:
            return ' | '.join([str(upc.unique_part_code) for upc in upcs])
        else:
            return None
    
    get_mechanic_name.short_description = 'Name'
    get_mechanic_city.short_description = 'City'
    get_upcs.short_description = 'UPC'

brand_admin = BajajAdminSite(name=GmApps.BAJAJ)

brand_admin.register(User, UserAdmin)
brand_admin.register(Group, GroupAdmin)
brand_admin.register(models.UserProfile, UserProfileAdmin)

brand_admin.register(models.Dealer, DealerAdmin)
brand_admin.register(models.AuthorizedServiceCenter, AuthorizedServiceCenterAdmin)
brand_admin.register(models.ServiceAdvisor, ServiceAdvisorAdmin)

brand_admin.register(models.BrandProductCategory, BrandProductCategoryAdmin)
brand_admin.register(models.ProductType, ProductTypeAdmin)
brand_admin.register(DispatchedProduct, ListDispatchedProduct)
brand_admin.register(models.ProductData, ProductDataAdmin)
brand_admin.register(models.CouponData, CouponAdmin)

brand_admin.register(models.SMSLog, SMSLogAdmin)
brand_admin.register(models.EmailLog, SMSLogAdmin)
brand_admin.register(models.DataFeedLog, FeedLogAdmin)

brand_admin.register(models.NationalSalesManager, NSMAdmin)
brand_admin.register(models.AreaSalesManager, ASMAdmin)
brand_admin.register(models.Distributor, DistributorAdmin)
brand_admin.register(models.Mechanic, MechanicAdmin)

brand_admin.register(models.SparePartMasterData, SparePartMasterAdmin)
brand_admin.register(models.SparePartUPC, SparePartUPCAdmin)
brand_admin.register(models.SparePartPoint, SparePartPointAdmin)
brand_admin.register(models.AccumulationRequest, AccumulationRequestAdmin)

brand_admin.register(models.ASCTempRegistration, ASCTempRegistrationAdmin)
brand_admin.register(models.SATempRegistration, SATempRegistrationAdmin)
brand_admin.register(models.CustomerTempRegistration, CustomerTempRegistrationAdmin)

brand_admin.register(models.EmailTemplate, EmailTemplateAdmin)
brand_admin.register(models.MessageTemplate, MessageTemplateAdmin)
brand_admin.register(models.SLA, SlaAdmin)
brand_admin.register(models.ServiceDeskUser, ServiceDeskUserAdmin)
