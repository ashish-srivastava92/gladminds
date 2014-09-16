''' Test Case for testing out all the  coupon flows
'''

from integration.base import BaseTestCase


class TestCouponFlow(BaseTestCase):

    def setUp(self):
        super(TestCouponFlow, self).setUp()

    def test_coupon_flow(self):
        brand = self.brand
        system = self.system

        pulsar = brand.dispatch_product(type="BIKE")
        customer = pulsar.purchase(product=pulsar, purchased_date='', customer_mobile='')
        service_advisor = brand.register_service_advisor(mobile='', status='active')

        service_advisor.send_coupon_activate_sms(kms=499, service_type='', customer_id=customer.id)

        coupon = system.check_coupon_in_progress(customer_id=customer.id, service_type='1')
        customer.check_sms('')
        service_advisor.check_sms('')
        service_advisor.send_coupon_close_sms(ucn_id=coupon.id, customer_id=customer.id)
        customer.check_sms('')
        service_advisor.check_sms('')
        system.check_coupon_is_closed(customer_id=customer.id, service_type='1')
