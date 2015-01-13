from django.shortcuts import render
from django.http.response import Http404


def site_info(request):
    if request.method != 'GET':
        raise Http404
    return render(request, 'site_info.html')