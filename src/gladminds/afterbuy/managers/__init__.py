from gladminds.afterbuy import models as afterbuy_common

def get_product(product_id):
    product_info = afterbuy_common.UserProduct.objects.get(id=product_id)
    return product_info