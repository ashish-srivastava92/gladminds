from gladminds.afterbuy import models as afterbuy_common

def get_product(phone_number, product_id):
    user_info = afterbuy_common.Consumer.objects.get(phone_number=phone_number)
    product_info = afterbuy_common.UserProduct.objects.get(id=product_id,consumer=user_info)
    return product_info