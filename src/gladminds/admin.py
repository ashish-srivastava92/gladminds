import json

from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from suit.widgets import EnclosedInput
from django.forms import ModelForm

from gladminds.gm.models import Brand,\
    MessageTemplate, EmailTemplate, Industry, BrandCategory


class GladmindsAdminSite(AdminSite):
    pass

admin = GladmindsAdminSite(name='bajaj')


class GladmindUserForm(ModelForm):

    class Meta:
        widgets = {
            'gladmind_customer_id': EnclosedInput(prepend='icon-asterisk',
                                                  attrs={'class': 'input-small'})
        }


class GladmindsUserAdmin(ModelAdmin):
    form = GladmindUserForm
    search_fields = (
        'gladmind_customer_id', 'phone_number')
    list_display = ('gladmind_customer_id', 'phone_number')

    def date_of_registration(self, obj):
        return obj.registration_date.strftime("%d %b %Y")


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

        
class CustomerTempRegistrationAdmin(ModelAdmin):
    search_fields = (
        'product_data__vin', 'new_customer_name', 'new_number', 'temp_customer_id', 'sent_to_sap')

    list_display = (
        'temp_customer_id','product_data', 'new_customer_name', 'new_number',
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
        'gm_user', 'message', 'notification_date', 'notification_read')

class UserFeedback(ModelAdmin):

    list_display = (
        'reporter', 'assign_to', 'message', 'subject', 'priority', 'type', 'status', 'created_date', 'modified_date')

##############################################################

admin.register(Industry)
admin.register(Brand)
admin.register(BrandCategory)
#admin.register(GladmindsUser, GladmindsUserAdmin)
admin.register(MessageTemplate)
admin.register(EmailTemplate)
