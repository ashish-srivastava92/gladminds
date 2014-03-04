from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from functools import wraps
from datetime import timedelta
from datetime import datetime


def authentication_required(func):
    print "decorsting thr function %s"% func.__name__
    def wrapper(request,*args,**kwargs):
        unique_id=request.GET.get('unique_id')
        time_stamp=unique_id[5:]
        date_time_obj=datetime.strptime(time_stamp, "%Y-%m-%d %H:%M:%S.%f")
        valid_date_time=date_time_obj + timedelta(days=7)
        if valid_date_time>date_time_obj:
            return func(request, *args, **kwargs)
        else:
            return {'status':9}
    return wrapper
