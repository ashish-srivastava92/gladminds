from django.contrib import admin
from models.common import Customer,Product,Service,RegisteredDealer,ProductPurchased
from models.common import GladMindUsers,SAPData
from models.logs import AuditLog 
from suit.widgets import NumberInput
from suit.admin import SortableModelAdmin
from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin

class CustomerForm(ModelForm):
    class Meta:
        widgets = {
            'customer_id': TextInput(attrs={'class': 'input-mini'}),
            'phone_number': NumberInput()
        }

class CustomerAdmin(ModelAdmin):
    sortable = 'customer_id'
    search_fields = ('customer_id','phone_number')
    list_display = ('customer_id', 'phone_number','is_authenticated')
    form = CustomerForm
    
class ProductAdmin(ModelAdmin):
    search_fields = ('product_id','brand_name')
    list_display = ('product_id', 'brand_name')
    
class ServiceAdmin(ModelAdmin):
    search_fields = ('unique_service_code',)
    list_filter = ('product',)
    list_display = ('product', 'unique_service_code','expiry_time')
    
class DealerAdmin(ModelAdmin):
    search_fields = ('phone_number',)
    list_display = ('phone_number',)
    
class ProductPurchasedAdmin(ModelAdmin):
    search_fields = ('product_id','customer_id')
    list_display = ('product_id','customer_id')
    
class AuditLogAdmin(ModelAdmin):
    search_fields = ('status','date','sender','reciever')
    list_display = ('date','action','message','sender','reciever','status')
    
class GladMindUserAdmin(ModelAdmin):
    search_fields = ('gcid','phone_number')
    list_display = ('gcid','phone_number')
    
class SAPDataAdmin(ModelAdmin):
    search_fields = ('phone_number','customer_id','product_id','unique_service_code'
                     ,'status')
    list_display = ('phone_number','customer_id','product_id','unique_service_code',
                     'validity_days_kms','status')
    
    

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(RegisteredDealer,DealerAdmin)
admin.site.register(ProductPurchased,ProductPurchasedAdmin)
admin.site.register(AuditLog,AuditLogAdmin)

admin.site.register(SAPData,SAPDataAdmin)
admin.site.register(GladMindUsers,GladMindUserAdmin)