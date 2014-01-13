from django.contrib import admin
from models.common import Customer,Product,Service,RegisteredDealer,ProductPurchased
from models.logs import AuditLog 
from suit.widgets import NumberInput
from suit.admin import SortableModelAdmin
from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin

class CustomerForm(ModelForm):
    class Meta:
        widgets = {
            'customer_id': TextInput(attrs={'class': 'input-mini'}),
            'phone_number': NumberInput(),
        }

class CustomerAdmin(ModelAdmin):
    sortable = 'customer_id'
    search_fields = ('customer_id','phone_number')
    list_display = ('customer_id', 'phone_number', 'registration_date', 'is_authenticated')
    form = CustomerForm
    
class ProductAdmin(ModelAdmin):
    search_fields = ('product_id','brand_name')
    list_display = ('product_id', 'brand_name')
    
class ServiceAdmin(ModelAdmin):
    search_fields = ('unique_service_code',)
    list_filter = ('product',)
    list_display = ('product', 'unique_service_code','expiry_time', 'valid_days', 'start_kms', 'end_kms', 'is_expired', 'is_closed', 'closed_date', 'expired_date')
    
class DealerAdmin(ModelAdmin):
    search_fields = ('phone_number',)
    list_display = ('phone_number',)
    
class ProductPurchasedAdmin(ModelAdmin):
    search_fields = ('product_id','customer_id', 'sap_customer_id', 'purchased_date')
    list_display = ('product_id','customer_id')
    
class AuditLogAdmin(ModelAdmin):
    search_fields = ('status','date')
    list_display = ('date','action','message','sender','reciever','status')
    

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(RegisteredDealer,DealerAdmin)
admin.site.register(ProductPurchased,ProductPurchasedAdmin)
admin.site.register(AuditLog,AuditLogAdmin)