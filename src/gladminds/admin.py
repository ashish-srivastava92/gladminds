from django.contrib import admin
from models.common import RegisteredDealer
from models.common import GladMindUsers,CustomerData,RegisteredDealer,ServiceAdvisor
from models.logs import AuditLog 
from suit.widgets import NumberInput
from suit.admin import SortableModelAdmin
from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin
from suit.admin import SortableTabularInline, SortableModelAdmin
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, \
    EnclosedInput, LinkedSelect, AutosizedTextarea


class DealerInlineForm(ModelForm):
    class Meta:
        widgets = {
            'name': EnclosedInput(prepend='icon-user',
                                        attrs={'class': 'input-large'}),
            'phone_number': EnclosedInput(
                                        attrs={'class': 'input-large'}),
        }
        
class DealerInline(SortableTabularInline):
    form = DealerInlineForm
    model = ServiceAdvisor
    fields = ('name','phone_number')
    extra = 1
    
class DealerForm(ModelForm):
    class Meta:
        widgets = { 
            'dealer_code': EnclosedInput(prepend='icon-asterisk',
                                        attrs={'class': 'input-small'}),
            'address': AutosizedTextarea,
        }    

class DealerAdmin(ModelAdmin):
    form = DealerForm
    search_fields = ('dealer_code',)
    list_filter = ('dealer_code',)
    list_display = ('dealer_code','address','serviceadvisor')
    inlines = (DealerInline,)
    
    def serviceadvisor(self, obj):
        return len(obj.serviceadvisor_set.all())

class AuditLogAdmin(ModelAdmin):
    search_fields = ('status','date','sender','reciever')
    list_display = ('date','action','message','sender','reciever','status')
    
class GladMindUserAdmin(ModelAdmin):
    search_fields = ('gladmind_customer_id','phone_number')
    list_display = ('gladmind_customer_id','phone_number','registration_date')
    
    

    
class CustomersAdmin(ModelAdmin):
    search_fields = ('phone_number','sap_customer_id','product_id','unique_service_coupon',
                     'is_expired','is_closed')
    list_display = ('phone_number','sap_customer_id','product_id','unique_service_coupon'
                     ,'valid_days','valid_kms','is_expired','is_closed','closed_date'
                     ,'expired_date','product_purchase_date','actual_service_date',
                     'actual_kms','dealer','last_reminder_date','schedule_reminder_date')
    
admin.site.register(RegisteredDealer,DealerAdmin)
admin.site.register(AuditLog,AuditLogAdmin)
admin.site.register(CustomerData,CustomersAdmin)
admin.site.register(GladMindUsers,GladMindUserAdmin)

