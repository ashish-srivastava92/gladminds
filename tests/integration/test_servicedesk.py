from django.test.client import Client
import unittest
from gladminds.bajaj.models import AuditLog, Feedback
from integration.base import BaseTestCase
from integration.test_system_logic import System
from django.test import TestCase

client = Client()


class TestServiceDeskFlow(BaseTestCase):
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.client = Client()
        self.system = System(self)
        system = self.system
        self.create_user(username='test', email='test@gladminds.co', password='test')
        system.create_sdo(username='sdo', email='gm@gm.com', password='123', phone_number="+919999999999")
        system.create_sdm(username='sdm', email='gm@gm.com', password='123', phone_number="+911999999989")

    @unittest.skip("skip the test")
    def test_send_servicedesk_feedback(self):
        initiator = self.system
        initiator.post_feedback()
        log_len_after = AuditLog.objects.all()
        feedback_obj = Feedback.objects.all()
        system = self.system
        system.verify_result(input=feedback_obj[0].priority, output="High")
        system.verify_result(input=len(log_len_after), output=1)
        system.verify_result(input=log_len_after[0].receiver, output="9999999998")
 
    @unittest.skip("skip the test")
    def test_get_feedback_sdo(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_owner = self.system
        service_desk_owner.login(username='sdo', password='123', provider='desk', group_name='SDO')
        service_desk_owner.get_feedback_information()
        feedback_obj = Feedback.objects.all()
        system = self.system
        system.verify_result(input=feedback_obj[0].priority, output="High")
    
    @unittest.skip("skip the test")
    def test_get_feedback_sdm(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name='SDM')
        service_desk_manager.get_feedback_information()
        feedback_obj = Feedback.objects.all()
        system = self.system
        system.verify_result(input=feedback_obj[0].priority, output="High")
 
    @unittest.skip("skip the test")
    def test_sms_email_assignee_after_feedback_assigned(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name='SDO')
        service_desk_manager.update_feedback(status='Open')
        log_len_after = AuditLog.objects.all()
        system = self.system
        system.verify_result(input=log_len_after[0].receiver, output="9999999998")
        system.verify_result(input=log_len_after[1].receiver, output="9999999998")
        system.verify_result(input=log_len_after[2].receiver, output="9999999999")
 
    @unittest.skip("skip the test")
    def test_sms_email_after_resolved(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_owner = self.system
        service_desk_owner.login(username='sdo', password='123', provider='desk', group_name='SDO')
        service_desk_owner.update_feedback(status='resolved', assign_to='+919999999999')
 
    @unittest.skip("skip the test")
    def test_updated_feedback(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name='SDM')
        service_desk_manager.update_feedback(status='Closed', assign_to='None')
        feedbacks = Feedback.objects.filter(priority='High')
        system = self.system
        system.verify_result(input=feedbacks[0].status, output='Closed')

