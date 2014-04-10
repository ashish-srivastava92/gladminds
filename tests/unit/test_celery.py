from integration.base_integration import GladmindsResourceTestCase
from django.test.utils import override_settings
from gladminds.tasks import send_service_detail


class TestCelery(GladmindsResourceTestCase):
    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='django')
    
    def test_send_sms(self):
        result = send_service_detail.delay(phone_number='99999999', message='Test Message')
        self.assertTrue(result.successful())