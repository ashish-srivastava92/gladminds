from django.utils.log import logging
import time
logger = logging.getLogger('gladminds')

'''Decorator generator that logs the time it takes a function to execute'''
#Decorator generator
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
