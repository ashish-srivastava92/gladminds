from django.shortcuts import render
from django.http.response import Http404

import logging
logger = logging.getLogger('gladminds')

def site_info(request):
    logger.info("Request coming to site_info url")
    if request.method != 'GET':
        raise Http404
    return render(request, 'site_info.html')
