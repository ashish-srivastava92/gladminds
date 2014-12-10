import time

from tastypie.http import HttpUnauthorized
from django.utils.log import logging

from gladminds.core.service_handler import ServiceHandler
from django.http.response import HttpResponse

logger = logging.getLogger('gladminds')
service_handler = ServiceHandler()

'''Decorator generator that logs the time it takes a function to execute'''
def log_time(func_to_decorate):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func_to_decorate(*args, **kwargs)
        elapsed = (time.time() - start)
        logger.info("[TIMING]:%s - %s" % (func_to_decorate.__name__, elapsed))
        return result
    wrapper.__doc__ = func_to_decorate.__doc__
    wrapper.__name__ = func_to_decorate.__name__
    return wrapper


'''Checks that service is enabled depending on the url passed'''
def check_service(service_name):
    def check_service_wrapper(func_to_decorate):
        def wrapper(*args, **kwargs):
            if service_handler.check_service_enabled(service_name):
                result = func_to_decorate(*args, **kwargs)
                logger.info("Brand is allowed to use this service")
                return result
            else:
                return HttpResponse("Not Authorized")
        wrapper.__doc__ = func_to_decorate.__doc__
        wrapper.__name__ = func_to_decorate.__name__
        return wrapper
    return check_service_wrapper
