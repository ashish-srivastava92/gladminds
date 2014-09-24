from django.test.client import Client

from integration.base_integration import GladmindsResourceTestCase
from gladminds.aftersell.models import common as aftersell_common
from gladminds.aftersell.models import logs
from integration.base import BaseTestCase
from django.test import TestCase

client = Client()


class TestServiceDeskFlow(GladmindsResourceTestCase, BaseTestCase):
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.client = Client()
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')
        self.create_service_advisor()
        self.create_register_dealer()
        self.create_dealer_service_advisor()

    def test_send_servicedesk_feedback(self):
        self.post_feedback()
        log_len_after = logs.AuditLog.objects.all()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")
        self.assertEqual(len(log_len_after),1)
        self.assertEqual(log_len_after[0].reciever, "9999999998")

    def test_get_feedback_sdo(self):
        self.post_feedback()
        self.test_servicedesk_login_sdo()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")

    def test_get_feedback_sdm(self):
        self.post_feedback()
        self.test_servicedesk_login_sdm()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")
 
    def test_sms_email_assignee_after_feedback_assigned(self):
        self.post_feedback()
        self.test_servicedesk_login_sdm()
        self.update_feedback_assigned()
        log_len_after = logs.AuditLog.objects.all()
        self.assertEqual(log_len_after[0].reciever, "9999999998")
        self.assertEqual(log_len_after[1].reciever, "9999999998")
        self.assertEqual(log_len_after[2].reciever , "9999999999")
 
    def test_sms_email_after_resolved(self):
        self.post_feedback()
        self.test_servicedesk_login_sdo()
        self.update_feedback_resolved()

    def test_updated_feedback(self):
        self.post_feedback()
        self.test_servicedesk_login_sdm()
        self.update_feedback_fields()
        feedbacks = aftersell_common.Feedback.objects.filter(priority = 'High')
        self.assertEqual(feedbacks[0].status  ,'Closed')
