import base64
import hashlib
import datetime
import re


def get_list_from_set(set_data):
    created_list = []
    for set_object in set_data:
        created_list.append(list(set_object)[1])
    return created_list

def generate_temp_id(prefix_value):
    for x in range(5):
        key = base64.b64encode(hashlib.sha256(str(datetime.datetime.now())).digest())
        key = re.sub("[a-z/=+]", "", key)
        if len(key) < 6:
            continue
        return "%s%s" % (prefix_value, key[:6])

def generate_mech_id():
    mechanic_id=generate_temp_id('TME')
    return mechanic_id


def debug(fn):
    '''
    Use as print utility
    :param fn:
    :type fn:
    '''
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print 'name:{0} args:{1} kwargs:{2} result: {3}'.format(fn.__name__, args, kwargs, result)
        return result
    return wrapper
