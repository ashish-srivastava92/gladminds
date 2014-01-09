import os
import hashlib
from tastypie.serializers import Serializer
         
def generate_unique_customer_id():
    bytes_str = os.urandom(24)
    unique_str = hashlib.md5(bytes_str).hexdigest()[:7]
    return unique_str.upper()

