from django.shortcuts import render_to_response
from django.contrib.auth.views import login_required
from django.template.context import RequestContext
from django.http.response import HttpResponseRedirect

@login_required(login_url='/dealers/')
def action(request, params):
    if request.method == 'GET':
        return render_to_response('dealer/advisor_actions.html', context_instance=RequestContext(request))
    elif request.method == 'POST':
        #TODO: Implement the submit functionality
        pass
    
@login_required(login_url='/dealers/')
def redirect(request):
    return HttpResponseRedirect('/dealers/' + str(request.user))