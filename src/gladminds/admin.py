from django.contrib import admin
from models.common import Customer,Product,Service
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
    list_display = ('product', 'unique_service_code')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Service,ServiceAdmin)
