from django.test.client import Client

from gladminds.aftersell.models import common as aftersell_common
from gladminds.aftersell.models import logs
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
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')
        system.create_sdo(username='sdo', email='gm@gm.com', password='123', phone_number="+919999999999")
        system.create_sdm(username='sdm', email='gm@gm.com', password='123', phone_number="+911999999989")

    def test_send_servicedesk_feedback(self):
        initiator = self.system
        initiator.post_feedback()
        log_len_after = logs.AuditLog.objects.all()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")
        self.assertEqual(len(log_len_after),1)
        self.assertEqual(log_len_after[0].reciever, "9999999998")
 
    def test_get_feedback_sdo(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_owner = self.system
        service_desk_owner.login(username='sdo', password='123', provider='desk', group_name='SDO')
        service_desk_owner.get_feedback_information()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")
 
    def test_get_feedback_sdm(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name='SDM')
        service_desk_manager.get_feedback_information()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")
 
    def test_sms_email_assignee_after_feedback_assigned(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name='SDO')
        service_desk_manager.update_feedback(status='Open')
        log_len_after = logs.AuditLog.objects.all()
        self.assertEqual(log_len_after[0].reciever, "9999999998")
        self.assertEqual(log_len_after[1].reciever, "9999999998")
        self.assertEqual(log_len_after[2].reciever, "9999999999")
 
    def test_sms_email_after_resolved(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_owner = self.system
        service_desk_owner.login(username='sdo', password='123', provider='desk', group_name='SDO')
        service_desk_owner.update_feedback(status='resolved', assign_to='+919999999999')
 
    def test_updated_feedback(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name='SDM')
        service_desk_manager.update_feedback(status='Closed', assign_to='None')
        feedbacks = aftersell_common.Feedback.objects.filter(priority='High')
        self.assertEqual(feedbacks[0].status ,'Closed')
