from django.shortcuts import render_to_response

def send_sms(request):
    return render_to_response('mobile.html')
