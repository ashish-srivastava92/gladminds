from django.contrib.admin.options import ModelAdmin
from suit.admin import SortableTabularInline
from suit.widgets import EnclosedInput, AutosizedTextarea
from django.forms.models import ModelForm
from django.contrib.admin.views.main import ORDER_VAR, ChangeList
from django.core.exceptions import PermissionDenied
from gladminds.core import utils
from gladminds.bajaj import models
from django.core.urlresolvers import reverse
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.http.response import HttpResponseRedirect


class GmModelAdmin(ModelAdmin):
    groups_update_not_allowed = []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta
        if request.method == 'POST' and not "_saveasnew" in request.POST:
            if request.user.groups.filter(name__in=self.groups_update_not_allowed).exists():
                post_url_continue = reverse('admin:%s_%s_changelist' %
                                   (opts.app_label, opts.model_name),
                                   current_app=self.admin_site.name)
                return HttpResponseRedirect(post_url_continue)
        return super(GmModelAdmin, self).change_view(request, object_id,
                                                     form_url=form_url,
                                                     extra_context=extra_context)

class ServiceAdvisorAdmin(ModelAdmin):
    search_fields = (
        'service_advisor_id', 'phone_number', 'name', 'dealer_id__dealer_id')
    list_display = ('name', 'service_advisor_id', 'phone_number')
    exclude = ('order',)

    def dealer_id(self, obj):
        return u'<a href="/gladminds/dealer/%s/">%s</a>' % (obj.dealer_id.pk, obj.dealer_id)
    dealer_id.allow_tags = True


class ServiceAdvisorDealerAdmin(ModelAdmin):
    search_fields = ('dealer_id__dealer_id', 'service_advisor_id__service_advisor_id',
                     'service_advisor_id__name', 'service_advisor_id__phone_number')

    list_display = (
        'dealer_id', 'name', 'service_advisor_ids', 'phone_number', 'status')

    def dealer_id(self, obj):
        return u'<a href="/gladminds/dealer/%s/">%s</a>' % (obj.dealer_id.pk, obj.dealer_id)
    dealer_id.allow_tags = True

    def service_advisor_ids(self, obj):
        sa_obj = models.ServiceAdvisor.objects.filter(
            service_advisor_id=obj.service_advisor_id.service_advisor_id)
        return u'<a href="/aftersell/serviceadvisor/%s/">%s</a>' % (obj.service_advisor_id.pk,
                                                                    sa_obj[0].service_advisor_id)
    service_advisor_ids.allow_tags = True

    def name(self, obj):
        sa_obj = models.ServiceAdvisor.objects.filter(
            service_advisor_id=obj.service_advisor_id.service_advisor_id)
        if len(sa_obj) > 0:
            return sa_obj[0].name
        return None

    def phone_number(self, obj):
        sa_obj = models.ServiceAdvisor.objects.filter(
            service_advisor_id=obj.service_advisor_id.service_advisor_id)
        if len(sa_obj) > 0:
            return sa_obj[0].phone_number
        return None

    def changelist_view(self, request, extra_context=None):
        extra_context = {'searchable_fields':"('dealer_id', 'service_advisor_id', 'service_advisor__name',"
        "'service_advisor_phone_number')"}
        return super(ServiceAdvisorDealerAdmin, self).changelist_view(request, extra_context=extra_context)


class Couponline(SortableTabularInline):
    model = models.CouponData
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
        for coupon in models.CouponData.objects.filter(vin=obj.id):
            ucn_list.append(coupon.unique_service_coupon)
        return ' | '.join([str(ucn) for ucn in ucn_list])

    def customer_name(self, obj):
        gm_user_obj = models.UserProfile.objects.get(
            phone_number=obj.customer_phone_number)
        name = ''
        if gm_user_obj:
            name = gm_user_obj.customer_name
        return name
    customer_name.allow_tags = True

    def service_type(self, obj):
        gm_coupon_data_obj = models.CouponData.objects.filter(vin=obj.id)
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
        custom_search_mapping = {
                                     'Vin' : '^vin',
                                     'Dealer Id': '^dealer_id__dealer_id',
                                     'Sap Customer ID':'^sap_customer_id', 
                                     'Customer Name': 'customer_phone_number__customer_name',
                                     'Customer Phone Number': 'customer_phone_number__phone_number'
                                }
        
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Vin, Sap Customer Id, Customer Phone Number and Customer Name'
                        }
        return super(ProductDataAdmin, self).changelist_view(request, extra_context=extra_context)


class CouponAdmin(ModelAdmin):
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
        custom_search_mapping = {
                                     'Unique Service Coupon' : '^unique_service_coupon',
                                     'Vin': '^vin__vin',
                                     'Status': 'status' 
                                }
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


class MessageTemplateAdmin(ModelAdmin):
    search_fields = ('template_key', 'template')
    list_display = ('template_key', 'template', 'description')
    readonly_fields = ('template_key',)
###################################################################

######################Email Template#############################


class EmailTemplateAdmin(ModelAdmin):
    search_fields = ('template_key', 'sender', 'receiver')
    list_display = ('template_key', 'sender', 'receivers', 'subject')
    readonly_fields = ('template_key',)

    def receivers(self, obj):
        return ' | '.join(obj.receiver.split(','))

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
    model = models.ServiceAdvisor
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


class DispatchedProduct(models.ProductData):

    class Meta:
        proxy = True
        app_label = 'DispatchedProduct'


class ListDispatchedProduct(ModelAdmin):
    search_fields = ('^vin','^dealer_id__dealer_id')
    
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
        for coupon in models.CouponData.objects.filter(vin=obj.id):
            ucn_list.append(coupon.unique_service_coupon)
        return ' | '.join([str(ucn) for ucn in ucn_list])
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('customer_phone_number',)
        form = super(ListDispatchedProduct, self).get_form(request, obj, **kwargs)
        return form

    def changelist_view(self, request, extra_context=None):
        custom_search_mapping = {
                                     'Vin' : '^vin',
                                     'Dealer Id': '^dealer_id__dealer_id',
                                }
        extra_context = {'custom_search': True, 'custom_search_fields': custom_search_mapping,
                         'searchable_fields': 'Vin and  Dealer id'
                        }
        
        return super(ListDispatchedProduct, self).changelist_view(request, extra_context=extra_context)
##############################################################
#########################ASCTempRegistration#########################


class ASCTempRegistrationAdmin(ModelAdmin):
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


class BrandAdmin(ModelAdmin):
    search_fields = ('name', 'industry__name')
    list_display = ('name', 'industry')


class IndustryAdmin(ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
