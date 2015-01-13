from django.contrib.admin.options import ModelAdmin
from suit.admin import SortableTabularInline
from suit.widgets import EnclosedInput, AutosizedTextarea
from django.forms.models import ModelForm
from django.contrib.admin.views.main import ORDER_VAR, ChangeList
from gladminds.core import utils
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from gladminds.core.model_fetcher import models
from gladminds.core.auth_helper import Roles


class GmModelAdmin(ModelAdmin):
    groups_update_not_allowed = [Roles.READONLY]
    
    def changelist_view(self, request, extra_context=None):
        searchable_fields=[]
        for field in self.search_fields:
            searchable_fields.append(field.split('__')[0].replace('_', ' ').title())
        extra_context = {
                         'searchable_fields': ', '.join(searchable_fields),
                        }
        return super(GmModelAdmin, self).changelist_view(request, extra_context=extra_context)     

    def change_view(self, request, object_id, form_url='', extra_context=None):
        model = self.model
        opts = model._meta
        if request.method == 'POST' and not "_saveasnew" in request.POST:
            if request.user.groups.filter(name__in=self.groups_update_not_allowed).exists():
                post_url_continue = reverse('admin:%s_%s_changelist' %
                                   (opts.app_label, opts.model_name),
                                   current_app=self.admin_site.name)
                self.message_user(request, "Sorry, you do not have permission to update.",
                                  level=messages.ERROR)
                return HttpResponseRedirect(post_url_continue)
        return super(GmModelAdmin, self).change_view(request, object_id,
                                                     form_url=form_url,
                                                     extra_context=extra_context)
