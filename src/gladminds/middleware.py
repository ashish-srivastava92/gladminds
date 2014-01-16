import logging
logger = logging.getLogger(__name__)

__all__ = ['GladmindsMiddleware']

"""
Gladminds middleware to identify the user type (i.e Customer, Service Advisor and Admin). 
And set the it into request object
"""
class GladmindsMiddleware(object):
    
    def __init__(self, *args, **kwargs):
        pass
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass