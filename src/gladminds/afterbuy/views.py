from django.shortcuts import render_to_response

def home(request):
    return render_to_response('afterbuy/index.html')


def login(request):
    print "request parameters are:",request