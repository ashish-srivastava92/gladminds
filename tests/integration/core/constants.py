def add_slashes(data):
    if data.startswith('/'):
        data = data[1:]
    if not data.endswith('/'):
        data = data + '/'

    return data


class Constants():
        BRAND = 'testbrand'
        INDUSTRY = 'testindustry'
        PRODUCT_TYPE = 'testproducttype'


class AfterbuyUrls():
        REGISTRATION = 'consumers/registration/'
        LOGIN = 'consumers/login/'
        BRAND = 'brands/'
        INDUSTRY = 'industries/'

