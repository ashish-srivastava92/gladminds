from django.contrib import admin
from models.common import RegisteredDealer
from models.common import GladMindUsers,ProductTypeData,RegisteredDealer,\
                ServiceAdvisor,BrandData,ProductData,CouponData, MessageTemplate,UploadProductCSV
from models.logs import AuditLog 
from suit.widgets import NumberInput
from suit.admin import SortableModelAdmin
from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin
from suit.admin import SortableTabularInline, SortableModelAdmin
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, \
    EnclosedInput, LinkedSelect, AutosizedTextarea
from django.contrib.admin import ModelAdmin, SimpleListFilter



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
    fields = ('product_name','product_type')
#     readonly_fields= ('product_name','product_type')
    extra=1
    max_num=0
    
class BrandForm(ModelForm):
    class Meta:
        widgets = { 
            'brand_id': EnclosedInput(prepend='icon-asterisk',
                                        attrs={'class': 'input-small'}),
            'brand_name': AutosizedTextarea,
        }    

class BrandAdmin(ModelAdmin):
    form = BrandForm
    search_fields =('brand_id','brand_name')
    list_filter = ('brand_name',)
    list_display = ('brand_id','brand_name','products')
    inlines = (ProductTypeDataInline,)
    
    def products(self, obj):
        return len(obj.producttypedata_set.all())
    
class ProductTypeDataAdmin(ModelAdmin):
    readonly_fields = ('order',)
    search_fields =('product_type','product_name','brand_id__brand_id')
    list_filter = ('product_type','product_name')
    list_display = ('brand_id','product_type','product_name')
     
 
 
#######################################################################
 
##########################DEALER AND SA ADMIN###########################
class SAInlineForm(ModelForm):
    class Meta:
        widgets = {
            'service_advisor_id':EnclosedInput(
                                        attrs={'class': 'input-large'}),
            'name': EnclosedInput(prepend='icon-user',
                                        attrs={'class': 'input-large'}),
            'phone_number': EnclosedInput(
                                        attrs={'class': 'input-large'}),
        }
         
class SAInline(SortableTabularInline):
    form = SAInlineForm
    model = ServiceAdvisor
    fields = ('service_advisor_id','name','phone_number')
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
    list_filter = ('dealer_id',)
    list_display = ('dealer_id','address','serviceadvisor')
    inlines = (SAInline,)
     
    def serviceadvisor(self, obj):
        return len(obj.serviceadvisor_set.all())
    
class ServiceAdvisorAdmin(ModelAdmin):
    search_fields = ('phone_number','name','dealer_id__dealer_id')
    list_display=('dealer_id','service_advisor_id','name','phone_number') 
      
 #################################################################### 
# 
# 
# #############CUSTMERDATA AND GLADMINDS USER ADMIN###################
# 
# class CustomerInlineForm(ModelForm):
#     class Meta:
#         widgets = {
#             
#             'vin': EnclosedInput(
#                                         attrs={'class': 'input-small'}),
#         }
#  
#  
#  
# class CustomerInline(SortableTabularInline):
#     form = CustomerInlineForm
#     model = CustomerData
#     fields = ('vin','product','dealer','product_purchase_date')
#     extra = 1
# 
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
    search_fields = ('gladmind_customer_id','customer_name','phone_number','email_id','registration_date')
    list_display = ('gladmind_customer_id','customer_name','email_id','phone_number','registration_date')
#     inlines = (CustomerInline,)
      
#     def products(self, obj):
#         return len(obj.customerdata_set.all())
#     


class Couponline(SortableTabularInline):
    model = CouponData
    fields = ('unique_service_coupon','valid_days','valid_kms','status','service_type','sa_phone_number')
    extra=0
    max_num=0
    readonly_fields=('unique_service_coupon','valid_days','valid_kms','status','service_type','sa_phone_number')

class ProductDataAdmin(ModelAdmin):
    search_fields = ('vin','sap_customer_id','customer_phone_number__phone_number')
    list_filter = ('customer_phone_number__phone_number',)
    list_display = ('vin','customer_phone_number','product_type','dealer_id','invoice_date')
    inlines=(Couponline,)
     
class CouponAdmin(ModelAdmin):
    search_fields = ('unique_service_coupon','vin__vin')
    list_filter = ('status',)
    list_display = ('vin','unique_service_coupon','service_type','valid_days','valid_kms',
                    'status')
     
         
    def suit_row_attributes(self, obj):
        class_map = {
            '1': 'success',
            '2': 'warning',
            '3': 'error',
        }
        css_class = class_map.get(str(obj.status))
        if css_class:
            return {'class': css_class}
####################################################################
 
###########################AUDIT ADMIN########################
class AuditLogAdmin(ModelAdmin):
    search_fields = ('status','date','sender','reciever')
    list_display = ('date','action','message','sender','reciever','status')
##############################################################
 
######################Message Template#############################
class MessageTemplateAdmin(ModelAdmin):
    search_fields = ('template_key','template')
    list_display=('template_key','template','description') 
    readonly_fields=('template_key',)
###################################################################


admin.site.register(BrandData,BrandAdmin)
admin.site.register(ProductTypeData,ProductTypeDataAdmin)
admin.site.register(ServiceAdvisor,ServiceAdvisorAdmin)
admin.site.register(RegisteredDealer,DealerAdmin)
admin.site.register(AuditLog,AuditLogAdmin)
admin.site.register(GladMindUsers,GladMindUserAdmin)
admin.site.register(ProductData,ProductDataAdmin)
admin.site.register(CouponData,CouponAdmin)
admin.site.register(MessageTemplate,MessageTemplateAdmin)
admin.site.register(UploadProductCSV)
