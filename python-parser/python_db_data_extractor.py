from gladminds.models.common import ProductData
all_product_data_obj = ProductData.objects.all()

with open('data.txt', "w") as fo:
    for obj in all_product_data_obj:
        obj_req = '{0},{1} \n'.format(obj.vin, obj.sap_customer_id)
        fo.write(obj_req)