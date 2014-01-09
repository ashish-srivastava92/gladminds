
from django.shortcuts import render_to_response
from gladminds.models import Customer

def page(request,page="customer"):
    customers_data=[]
    if page=='customer':
        customers_data=get_all_customer_data()
    return render_to_response('superadmin/%s.html' % (page),{'customers_data':customers_data})

    
def get_all_customer_data():
    customers=Customer.objects.all()
    return customers
