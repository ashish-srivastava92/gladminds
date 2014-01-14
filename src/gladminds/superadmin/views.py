from django.shortcuts import render_to_response
# from gladminds.models import Customer,Product,Service




def send_sms(request):
    return render_to_response('mobile.html')

# def page(request,page="customer"):
#     admin_data=select_template[page]
#     return render_to_response('superadmin/%s.html' % (page),{'admin_data':admin_data})
# 
#     
# def get_all_customer_data():
#     customers=Customer.objects.all()
#     return customers
# 
# def get_all_products_data():
#     products=Product.objects.all()
#     return products
# 
# def get_all_service_data():
#     services=Service.objects.all()
#     return services
# 
# select_template={
#                  'customer':get_all_customer_data,
#                  'product':get_all_products_data,
#                  'service':get_all_service_data
#                  }