from django.db import models
from django.db.models import Sum

class DealerManager(models.Manager):
    def active(self):
        result_list = []
        return result_list
    
class ServiceAdvisorManager(models.Manager):
    def active(self, phone_number):
        return super(ServiceAdvisorManager, self).get_query_set().filter(user__phone_number=phone_number, status='Y')
    
    def active_under_dealer(self, dealer):
        return super(ServiceAdvisorManager, self).get_query_set().filter(dealer=dealer, status='Y')

    def active_under_asc(self, asc):
        return super(ServiceAdvisorManager, self).get_query_set().filter(asc=asc, status='Y')
    
    def get_dealer_asc_obj(self, reporter):
        service_advisor_obj = super(ServiceAdvisorManager, self).select_related('dealer, asc').get(user=reporter.user_profile)
        if service_advisor_obj.dealer:
            return service_advisor_obj.dealer
        else:
            return service_advisor_obj.asc


class CustomerTempRegistrationManager(models.Manager):
    def get_updated_customer_id(self, customer_id):
        if customer_id and customer_id.find('T') == 0:
            temp_customer_obj = super(CustomerTempRegistrationManager, self).get_query_set().filter(temp_customer_id=customer_id)
            if temp_customer_obj:
                customer_id = temp_customer_obj[0].product_data.customer_id
        return customer_id

class MechanicManager(models.Manager):
    def get_mechanic(self, phone_number):
        return super(MechanicManager, self).get_query_set().filter(user__phone_number=phone_number)

class SpareUPCDataManager(models.Manager):

    def get_spare_parts(self, spare_product_codes):
        return super(SpareUPCDataManager, self).get_query_set().filter(unique_part_code__in=spare_product_codes,is_used=False)

class SparePointDataManager(models.Manager):

    def get_part_number(self, valid_product_number):
        return super(SparePointDataManager, self).get_query_set().filter(part_number__in=valid_product_number)
