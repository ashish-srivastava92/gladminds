from django.contrib import admin
from models.common import RegisteredDealer
from models.common import GladMindUsers,CustomerData,RegisteredDealer
from models.logs import AuditLog 
from suit.widgets import NumberInput
from suit.admin import SortableModelAdmin
from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin


class DealerAdmin(ModelAdmin):
    search_fields = ('phone_number',)
    list_filter = ('dealer_id',)
    list_display = ('dealer_id','phone_number')
    

class AuditLogAdmin(ModelAdmin):
    search_fields = ('status','date','sender','reciever')
    list_display = ('date','action','message','sender','reciever','status')
    
class GladMindUserAdmin(ModelAdmin):
    search_fields = ('gladmind_customer_id','phone_number')
    list_display = ('gladmind_customer_id','phone_number','registration_date')
    
class CustomerDataAdmin(ModelAdmin):
    search_fields = ('phone_number','sap_customer_id','product_id','unique_service_code',
                     'is_expired','is_closed')
    list_display = ('phone_number','sap_customer_id','product_id','unique_service_code'
                     ,'valid_days','valid_kms','is_expired','is_closed','closed_date'
                     ,'expired_date')

admin.site.register(RegisteredDealer,DealerAdmin)
admin.site.register(AuditLog,AuditLogAdmin)
admin.site.register(CustomerData,CustomerDataAdmin)
admin.site.register(GladMindUsers,GladMindUserAdmin)
