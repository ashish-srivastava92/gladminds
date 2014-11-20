import os
import boto
from boto.s3.key import Key

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from tastypie.serializers import Serializer
from uuid import uuid4
from django.views.decorators.http import require_http_methods

serializerObj = Serializer()

_KEYS_ALLOWED = ['consumers', 'products', 'brands', 'users']

@csrf_exempt
@require_http_methods(["POST"])
def upload_files(request):
    keys = request.FILES.keys()
    if len(keys) != 1:
        return HttpResponse(serializerObj.to_json({"message":"only 1 image upload allowed"}), content_type="application/json", status=400)
    if  keys[0] not in _KEYS_ALLOWED:
        return HttpResponse(serializerObj.to_json({"message":"key not found. Allowed keys: {0}".format(','.join(_KEYS_ALLOWED))}), content_type="application/json", status=400)
    try:
        conn = boto.connect_s3()
        bucket_name = settings.AWS_STORAGE_BUCKET_MAP.get(settings.BRAND,
                                                          settings.BRAND)
        bucket = conn.get_bucket(bucket_name, validate=False)
        full_key = os.path.join(settings.ENV, keys[0], str(uuid4())+request.FILES[keys[0]]._name)
        k = Key(bucket)
        data = request.FILES[keys[0]].read()
        k.key = full_key
        k.set_contents_from_string(data)
        k.set_acl('public-read')
    except Exception as e:
        return HttpResponse(serializerObj.to_json({"message":e.message}), content_type="application/json", status=500)
    return HttpResponse(serializerObj.to_json({"uid":full_key}), content_type="application/json")
