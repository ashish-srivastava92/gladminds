from django import template
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse, resolve
from suit.templatetags.suit_menu import Menu, get_admin_site
from django.conf import settings
from importlib import import_module
try:
    from django.utils.six import string_types
except ImportError:
    # For Django < 1.4.2
    string_types = basestring,

import warnings
from suit.config import get_config

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, WSGIRequest):
        return None

    # Try to get app list
    template_response = get_admin_site(context.current_app).index(request)
    try:
        app_list = template_response.context_data['app_list']
    except Exception:
        return

    return CustomMenu(context, request, app_list).get_app_list()

class CustomMenu(Menu):
    app_activated = False
    def __init__(self, context, request, app_list):
        super(CustomMenu, self).__init__(context, request, app_list)
    
    
    def init_config(self):
        self.conf_exclude = get_config('MENU_EXCLUDE')
        self.conf_open_first_child = get_config('MENU_OPEN_FIRST_CHILD')
        self.conf_icons = get_config('MENU_ICONS')
        self.conf_menu_order = get_config('MENU_ORDER')
        self.conf_menu = get_config('MENU')
        
        for menu in self.conf_menu:
            try:
                import_module('gladminds.{0}.admin'.format(settings.BRAND))
                menu['app'] = settings.BRAND
            except:
                menu['app'] = 'core'
