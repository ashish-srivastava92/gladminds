"""
It will have all Common Orm Functions which is using for APIS
"""
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from gladminds.gm.models import UserPreferences
from gladminds.gm.models import AppPreferences
 
def get_preferences_list(user_profile=None):
    """Returns preferences depending on user filter
    """
    data = []
    if user_profile:
        data = UserPreferences.objects.filter(user_profile=user_profile)
    else:
        data = UserPreferences.objects.all()
    return map(model_to_dict, data)
 
def get_preference(preference_key, user_profile):
    """Returns preferences depending on preferences key and userid.
    """
    try:
        data = UserPreferences.objects.get(
            key=preference_key, user_profile=user_profile)
    except:
        return {}
    return model_to_dict(data)
 
def update_preference(data, preference_key, user_profile):
    """Used for updating the preferences depending on preferences key and userid
    """
    data['key'] = preference_key
    data['user_profile'] = user_profile
    if UserPreferences.objects.filter(key=preference_key,
                                      user_profile=user_profile).exists():
        UserPreferences.objects.filter(
            key=preference_key, user_profile=user_profile).update(**data)
    else:
        save_preference(data)
 
def save_preference(data):
    """Returns preferences depending on preferences id.
    """
    data['user_profile_id'] = data['user_profile']
    del data['user_profile']
    UserPreferences.objects.create(**data)
 
def delete_preference(preference_id):
    """Used for deleting the preferences
    """
    UserPreferences.objects.get(id=preference_id).delete()
 
def get_app_preferences_list(brand=None):
    """Returns preferences depeding on brand filter
    """
    data = []
    if brand:
        data = AppPreferences.objects.filter(brand=brand)
    else:
        data = AppPreferences.objects.all()
    return map(model_to_dict, data)
 
 
def get_app_preference(preference_key, brand):
    """Returns preferences depending on preferences key and brandid.
    """
    try:
        data = AppPreferences.objects.get(
            key=preference_key, brand=brand)
    except:
        return {}
    return model_to_dict(data)
 
def update_app_preference(data, preference_key, brand):
    """Used for updating the preferences depending on preferences key and brand
    """
    data['key'] = preference_key
    data['brand'] = brand
    if AppPreferences.objects.filter(key=preference_key,
                                     brand=brand).exists():
        AppPreferences.objects.filter(
            key=preference_key, brand=brand).update(**data)
    else:
        save_app_preference(data)
 
 
def delete_app_preference(preference_id):
    """Used for deleting the preferences
    """
    AppPreferences.objects.get(id=preference_id).delete()
 
def save_app_preference(data):
    """Returns preferences depending on preferences id.
    """
    data['brand_id'] = data['brand']
    del data['brand']
    AppPreferences.objects.create(**data)
