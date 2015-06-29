import json
import logging

from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from tastypie import fields
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpBadRequest
from tastypie.utils.urls import trailing_slash

from gladminds.afterbuy import models as afterbuy_model
from gladminds.afterbuy import models as afterbuy_models
from gladminds.afterbuy.apis.brand_apis import BrandResource
from gladminds.afterbuy.apis.user_apis import ConsumerResource
from gladminds.afterbuy.apis.validations import ProductValidation
from gladminds.core.apis.authentication import AccessTokenAuthentication
from gladminds.core.apis.authorization import CustomAuthorization, \
    MultiAuthorization
from gladminds.core.apis.base_apis import CustomBaseModelResource
from gladminds.core.managers.mail import send_recycle_mail
from gladminds.core.auth_helper import GmApps
from gladminds.core.model_fetcher import get_model
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger("gladminds")


class ProductTypeResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', null=True, blank=True, full=True)
    class Meta:
        queryset = afterbuy_models.ProductType.objects.all()
        resource_name = "product-types"
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True


class ProductSpecificationResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type', null=True, blank=True,
                                     full=True)
    class Meta:
        queryset = afterbuy_models.ProductSpecification.objects.all()
        resource_name = "product-specifications"
        allowed_methods = ['get', 'post']
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True
        
class ProductFeatureResource(CustomBaseModelResource):
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type', null=True, blank=True,
                                     full=True)
    class Meta:
        queryset = afterbuy_models.ProductFeature.objects.all()
        resource_name = "product-features"
        allowed_methods = ['get', 'post']
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True

class RecommendedPartResource(CustomBaseModelResource):
    product_type = fields.ManyToManyField(ProductTypeResource, 'product_type', null=True, blank=True,
                                     full=True)
    class Meta:
        queryset = afterbuy_models.RecommendedPart.objects.all()
        resource_name = "product-parts"
        allowed_methods = ['get', 'post']
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True

class UserProductResource(CustomBaseModelResource):
    consumer = fields.ForeignKey(ConsumerResource, 'consumer', null=True, blank=True, full=True)
    product_type = fields.ForeignKey(ProductTypeResource, 'product_type', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_models.UserProduct.objects.filter(is_accepted=True)
        resource_name = "products"
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        validation = ProductValidation()
        always_return_data = True
        filtering = {
                     "consumer": ALL_WITH_RELATIONS,
                     "product_type": ALL_WITH_RELATIONS,
                     "is_deleted": ALL,
                     "brand_product_id" : ALL
                     }

    def prepend_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/coupons%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_product_coupons'), name="get_product_coupons" ),
                url(r"^(?P<resource_name>%s)/(?P<product_id>[\d]+)/recycle%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('mail_products_details'), name="mail_products_details" ),
                url(r"^(?P<resource_name>%s)/get-brands%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_brand_details'), name="get_brand_details" ),
                url(r"^(?P<resource_name>%s)/accept-product%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('user_product_acceptance'), name="user_product_acceptance" ),
                url(r"^(?P<resource_name>%s)/details%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('product_specifications'), name="product_specifications" ),
                url(r"^(?P<resource_name>%s)/add%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('add_product'), name="add_product"),
                url(r"^(?P<resource_name>%s)/brand-sync%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('brand_sync'), name="brand_sync"),
                url(r"^(?P<resource_name>%s)/get-service-details%s" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_service_details'), name="get_service_details")               
        ]

    def get_product_coupons(self, request, **kwargs):
        self.is_authenticated(request)
        product_id = request.GET['product_id']
        try:
            if product_id:
                coupons = get_model('CouponData', GmApps.BAJAJ).objects.filter(product__product_id=product_id)
                if not coupons:
                    return HttpResponse(json.dumps({'message' : 'No coupons', 'status' : 200}),
                                        content_type='application/json')
                coupon_data = {}
                coupon_data['coupon_data'] = [model_to_dict(c, exclude='product_type, id') for c in coupons]
                return HttpResponse(json.dumps(coupon_data, cls=DjangoJSONEncoder), content_type='application/json')
        except Exception as ex:
            logger.error('Exception while fetching coupon data - {0}'.format(ex))
    
    def mail_products_details(self, request, **kwargs):
        try:
            product_id = kwargs['product_id']
            product_info = afterbuy_models.UserProduct.objects.get(id=product_id)
            email_id = product_info.consumer.user.email
            try:
                afterbuy_model.Consumer.objects.get(user__email=email_id, is_email_verified=True)
                send_recycle_mail(email_id, data=product_info)
                data = {'status': 1, 'message': 'email sent successfully'}
            except Exception as ex:
                data = {'status': 0, 'message': 'email_id not active'}
        except Exception as ex:
            logger.error('Invalid details')  
            data = {'status': 0, 'message': 'email not sent'}
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def get_brand_details(self, request, **kwargs):
        self.is_authenticated(request)
        try:
            products = afterbuy_models.UserProduct.objects.filter(consumer__user=request.user).select_related('product_type')
            details = {}
            brand_details = []
            for product in products:
                brands = {}
                brands['brandId'] = product.product_type.brand.id
                brands['brandName'] = product.product_type.brand.name
                brands['brandImage'] = product.product_type.brand.image_url
                brands['brandProductId'] = product.brand_product_id
                brands['productType'] = product.product_type.product_type
                brand_details.append(brands)
            return HttpResponse(json.dumps({'status_code':200, 'brands': brand_details}), content_type='application/json')
        except Exception as ex:
            logger.error("Exception while fetching brands associated with phone number {0}".format(ex))
            return HttpBadRequest()
        
    def user_product_acceptance(self, request, **kwargs):
        self.is_authenticated(request)
        if request.method!= 'POST':
            return HttpResponse(json.dumps({"message":"method not allowed"}),
                                content_type="application/json",status=401)
        try:
            load = json.loads(request.body)
            is_accepted = load.get('is_accepted', False)
            brand_product_id = load.get('product_id')
            user_product = afterbuy_models.UserProduct.objects.get(brand_product_id=brand_product_id,
                                                                   consumer__user=request.user)
            user_product.is_accepted = is_accepted
            user_product.save()
            return HttpResponse(json.dumps({'status':200, 'message': True}),
                                content_type='application/json')
        except Exception as ex:
            logger.error("Exception while accepting the product{0}".format(ex))
            return HttpBadRequest("Incorrect Details")
        return
    
    def product_specifications(self, request, **kwargs):
        '''
        Get the product specifications
        
        Args : Product Type 
        Returns : All the features of that product type 
        '''
        self.is_authenticated(request)
        try:
            product_id = request.GET['product_id']
            product_type = afterbuy_models.ProductType.objects.filter(product_type=product_id)
            if len(product_type)==0:
                return HttpResponse(json.dumps({'message': 'Incorrect Product ID'}),
                                    content_type='application/json')
            specifications = afterbuy_models.ProductSpecification.objects.filter(product_type=product_type[0])
            features = afterbuy_models.ProductFeature.objects.filter(product_type=product_type[0])
            recommended_parts = afterbuy_models.RecommendedPart.objects.filter(product_type=product_type[0])

            result = {}
            details = []

            for specification in specifications:
                data = {}
                data['type'] = specification.product_type.product_type
                data[specification.key] = specification.value
                details.append(data)
                
            result['specifications'] =  details
            result['recommended_parts'] = [model_to_dict(c, exclude='product_type, id') for c in recommended_parts]
            result['features'] = [model_to_dict(c, exclude='product_type, id') for c in features]
            result['Overview'] = product_type[0].overview
            result['status_code'] = 200
            
            return HttpResponse(json.dumps(result),
                                content_type='application/json') 
        except Exception as ex:
            logger.error("Exception while fetching product specifications - {0}".format(ex))
            return HttpBadRequest("Incorrect Details")
    
    def brand_sync(self, request, **kwargs):
        '''
        Gets all the products from the brand database and adds it to afterbuy
        Args:
        phone_number : The phone number of the afterbuy user
        
        Returns:
        Syncs all the products of that user  
        '''
        self.is_authenticated(request)
        try:
            phone_number = request.GET['phone_number']
            products = get_model('ProductData', GmApps.BAJAJ).objects.filter(customer_phone_number__contains=phone_number)
            
            if not products:
                return HttpResponse(json.dumps({'status':200 , 'message': 'No products to be synced'}))

            for product in  products:
                try:
                    product_type = afterbuy_models.ProductType.objects.get(product_type=product.sku_code)
                except Exception as ObjectDoesNotExist:
                    product_brand =  afterbuy_models.Brand.objects.get(name='bajaj')
                    product_type = afterbuy_models.ProductType(product_type=product.sku_code,
                                                               brand=product_brand)
                    product_type.save()
                consumer = afterbuy_models.Consumer.objects.get(user=request.user)

                try:
                    user_product = afterbuy_models.UserProduct.objects.get(consumer__user=request.user,
                                                                           brand_product_id=product.product_id)
                except Exception as ObjectDoesNotExist:
                    user_product =  afterbuy_models.UserProduct(consumer=consumer,
                                                            purchase_date=product.purchase_date,
                                                            brand_product_id=product.product_id,
                                                            product_type=product_type)
                    user_product.save()
                return HttpResponse(json.dumps({'status' : 200 , 'message':'Products Synced Successfully'}),
                                        content_type='application/json')
        except Exception as ex:
            logger.error("Exception while syncing the products - {0}".format(ex))
            return HttpBadRequest("Products couldn't be synced")

    def add_product(self, request, **kwargs):
        '''
        Add product manually
        
        Args : product id, brand name , product type , year , warranty year, insurance year
        Returns : Saves the product  
        '''
        self.is_authenticated(request)
        if request.method != 'POST':
            return HttpResponse(json.dumps({'message' : 'Method not alowed'}),
                                content_type='application/json')
        try:
            load = json.loads(request.body)
            product_id = load.get('product_id')
            brand_name = load.get('brand_name')
            type = load.get('model_name')
            year = load.get('model_year')
            warranty_year = load.get('warranty_year', None)
            insurance_year = load.get('insurance_year', None)
            try:
                product_type = afterbuy_models.ProductType.objects.get(product_type=type, brand__name=brand_name)
            except Exception as ObjectDoesNotExist:
                brand = afterbuy_models.Brand.objects.get(name=GmApps.BAJAJ)
                product_type = afterbuy_models.ProductType(product_type=type,
                                                           brand=brand)
                product_type.save()
            
            consumer = afterbuy_models.Consumer.objects.get(user=request.user)
            try:
                user_product = afterbuy_models.UserProduct.objects.get(consumer__user=request.user,
                                                                       brand_product_id=product_id)
                return HttpResponse(json.dumps({'status':200 , 'message' : 'This product has been already registered'}),
                                    content_type='application/json')
            except Exception as ObjectDoesNotExist:
                user_product = afterbuy_models.UserProduct(consumer=consumer, brand_product_id=product_id,
                                                  purchase_date=year, product_type=product_type,
                                                  warranty_year=warranty_year, insurance_year=insurance_year)
                user_product.save()
                return HttpResponse(json.dumps({'status':200, 'message' : 'Product added successfully'}),
                                content_type='application/json')
        except Exception as ex:
            logger.error("Exception while afterbuy user product {0}", format(ex))
            return HttpBadRequest('Product cannot be added')
    
    def get_service_details(self, request, **kwargs):
        self.is_authenticated(request)
        try:
            product_id = request.GET['product_id']
            coupons = get_model('CouponData', GmApps.BAJAJ).objects.filter(product__product_id=product_id)

            if not coupons:
                return HttpResponse(json.dumps({'status':200 , 'message': 'No Services to be displayed'}))
            details = []
            history = []
            for coupon in coupons:
                data = {}
                if not coupon.closed_date:
                    data['serviceNumber'] = coupon.service_type
                    data['dueDate'] = str(coupon.schedule_reminder_date)
                    details.append(data)
                data = {}
                data['serviceDate'] = str(coupon.actual_service_date)
                data['ucn'] = coupon.unique_service_coupon
                history.append(data)
                    
            return HttpResponse(json.dumps({'serviceDueReminder' : details,
                                            'serviceHistory' : history}),
                                content_type='application/json')
        except Exception as ex:
            logger.error("Exception while fetching service details for : {0} {1}".format(product_id, ex))
            return HttpBadRequest("Service Details couldn't be fetched")

class ProductInsuranceInfoResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_models.ProductInsuranceInfo.objects.all()
        resource_name = "insurances"
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        allowed_methods = ['get', 'post', 'put']
        authentication = AccessTokenAuthentication()
        always_return_data = True
        filtering = {
                     "product": ALL,
                     "is_expired": ALL,
                     "expiry_date": ALL
                     }


class InvoiceResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', null=True, blank=True, full=True)

    class Meta:
        queryset = afterbuy_models.Invoice.objects.all()
        resource_name = "invoices"
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        authentication = AccessTokenAuthentication()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "product": ALL
                     }


class LicenseResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.License.objects.all()
        resource_name = 'licenses'
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        authentication = AccessTokenAuthentication()
        allowed_methods = ['get', 'post', 'put']
        always_return_data =True
        filtering = {
                     "product" : ALL
                     }


class RegistrationCertificateResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.RegistrationCertificate.objects.all()
        resource_name = 'registrations'
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        authentication = AccessTokenAuthentication()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "product": ALL
                     }


class PollutionCertificateResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.PollutionCertificate.objects.all()
        resource_name = 'pollution'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "product": ALL
                     }


class SupportResource(CustomBaseModelResource):
    brand = fields.ForeignKey(BrandResource, 'brand', full=True, null=True)
    brand_product_category = fields.ForeignKey(BrandResource, 'brand_product_category', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.Support.objects.all()
        resource_name = 'support'
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "brand": ALL,
                     "brand_product_category": ALL
                     }


class ProductSupportResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.ProductSupport.objects.all()
        resource_name = 'product-support'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "product": ALL,
                     }


class SellInformationResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.SellInformation.objects.all()
        resource_name = 'sell-information'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "product": ALL,
                     }


class UserProductImagesResource(CustomBaseModelResource):
    product = fields.ForeignKey(UserProductResource, 'product', full=True, null=True)

    class Meta:
        queryset = afterbuy_models.UserProductImages.objects.all()
        resource_name = 'product-images'
        authentication = AccessTokenAuthentication()
        authorization = MultiAuthorization(Authorization(), CustomAuthorization())
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        filtering = {
                     "product": ALL,
                     }


class InterestResource(CustomBaseModelResource):

    class Meta:
        queryset = afterbuy_model.Interest.objects.all()
        resource_name = "interests"
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
