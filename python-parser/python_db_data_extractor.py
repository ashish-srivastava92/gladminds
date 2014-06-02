from gladminds.models.common import ProductData
all_product_data_obj = ProductData.objects.all()

with open('data.txt', "w") as fo:
    for obj in all_product_data_obj:
        obj_req = '{0},{1} \n'.format(obj.vin, obj.sap_customer_id)
        fo.write(obj_req)
        
        
from gladminds.models import common

sap_ids = [ str(i) for i in range(8000275, 8000696)]

for sap_id in sap_ids:
    product_obj = common.ProductData.objects.filter(sap_customer_id = sap_id)
    print product_obj 
    if product_obj:
        product_obj = product_obj[0] 
        user_id = product_obj.customer_phone_number
        product_obj.customer_phone_number = None
        common.GladMindUsers.delete(id = user_id.id)
        product_obj.customer_phone_number = None
        product_obj.sap_customer_id = None
        product_obj.product_purchase_date = None
        product_obj.engine = None
        