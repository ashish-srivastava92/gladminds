from django.db.utils import IntegrityError
from django.db import transaction
from tastypie import fields, http
from tastypie.bundle import Bundle
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse

from gladminds.core.apis.base_apis import CustomBaseResource, CustomApiObject
from django.forms.models import model_to_dict
from gladminds.core.loaders.module_loader import get_model


class PreferencesBaseResource(CustomBaseResource):
    """
    It is a preferences resource
    """

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Overriding the details_uri_kwargs and setting kwargs to Null
        It will be using for POST methods
        """
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id
        return kwargs

    def obj_update(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        q = filters.get(self._meta.filter_key, None)
        preference_key = kwargs["pk"]
        data = bundle.data
        data['key'] = preference_key
        data[self._meta.filter_key] = q
        self.update_preference(bundle.data, preference_key, q)

    def obj_delete(self, bundle, **kwargs):
        preference_id = kwargs["pk"]
        self.delete_preference(preference_id)

    def get_object_list(self, request):
        filters = {}
        if hasattr(request, 'GET'):
            filters = request.GET.copy()
        q = filters.get(self._meta.filter_key, None)
        data = self.get_preferences_list(filter_key=q)
        return map(CustomApiObject, data)

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        q = filters.get(self._meta.filter_key, None)
        # We can use select_related it will solve the performance issue
        serialized_obj = self.get_preference(kwargs["pk"], q)
        return CustomApiObject(serialized_obj)

    @transaction.atomic
    def save_preferences(self, bundle, **kwargs):
        """
        This saves the preferences
        """
        data = bundle.data
        try:
            if data['key'].find(' ') != -1:
                raise ImmediateHttpResponse(
                response=http.HttpBadRequest('key cannot have blank spaces!'))
        except Exception as e:
            raise ImmediateHttpResponse(
                response=http.HttpBadRequest('Key is missing!'))
        try:
            self.save_preference(data)
        except IntegrityError as e:
            raise ImmediateHttpResponse(
                response=http.HttpBadRequest(e.message))
        except Exception as e:
            raise Exception()

    def obj_create(self, bundle, **kwargs):
        """
        Overriding the obj_create
        """
        self.save_preferences(bundle, **kwargs)
        return bundle

    def get_preferences_list(self, filter_key=None):
        """Returns preferences depeding on brand filter
        """
        data = []
        if filter_key:
            data = get_model(self._meta.model).objects.filter(**{self._meta.filter_key: filter_key})
        else:
            data = get_model(self._meta.model).objects.all()
        return map(model_to_dict, data)

    def get_preference(self, preference_key, filter_key):
        """Returns preferences depending on preferences key and brandid.
        """
        try:
            data = get_model(self._meta.model).get(
                {'key': preference_key, self._meta.filter_key: filter_key})
        except:
            return {}
        return model_to_dict(data)

    def update_preference(self, data, preference_key, filter_key):
        """Used for updating the preferences depending on preferences key and brand
        """
        data['key'] = preference_key
        data[self._meta.filter_key] = filter_key
        if get_model(self._meta.model).objects.filter(**{'key': preference_key,
                                         self._meta.filter_key: filter_key}).exists():
            get_model(self._meta.model).objects.filter(**{'key': preference_key,
                                         self._meta.filter_key: filter_key}).update(**data)
        else:
            self.save_preference(data)

    def delete_preference(self, preference_id):
        """Used for deleting the preferences
        """
        get_model(self._meta.model).objects.get(id=preference_id).delete()

    def save_preference(self, data):
        """Returns preferences depending on preferences id.
        """
        data['{0}_id'.format(self._meta.filter_key)] = data[self._meta.filter_key]
        del data[self._meta.filter_key]
        get_model(self._meta.model).objects.create(**data)


class BrandPreferenceResource(PreferencesBaseResource):
    """
    It is a preferences resource
    """
    id = fields.IntegerField(attribute="id")
    brand = fields.IntegerField(attribute="brand")
    key = fields.CharField(attribute='key')
    value = fields.CharField(attribute='value', null=True)

    class Meta:
        resource_name = 'brand-preferences'
        filter_key = 'brand'
        model = 'BrandPreference'
        authorization = Authorization()
        object_class = CustomApiObject


class UserPreferenceResource(PreferencesBaseResource):
    """
    It is a preferences resource
    """
    id = fields.IntegerField(attribute="id")
    brand = fields.IntegerField(attribute="user")
    key = fields.CharField(attribute='key')
    value = fields.CharField(attribute='value', null=True)

    class Meta:
        resource_name = 'user-preferences'
        filter_key = 'user'
        model = 'UserPreference'
        authorization = Authorization()
        object_class = CustomApiObject
