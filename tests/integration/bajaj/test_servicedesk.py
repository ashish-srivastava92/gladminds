from django.test.client import Client
from gladminds.bajaj.models import AuditLog, Feedback, SMSLog, Comment, EmailLog,\
    ServiceAdvisor, UserProfile
from integration.bajaj.base import BaseTestCase
from integration.bajaj.test_system_logic import System
from integration.bajaj.test_brand_logic import Brand
from django.test import TestCase
import datetime
from time import sleep
from django.contrib.auth.models import User
from gladminds.core.auth_helper import Roles

client = Client(SERVER_NAME='bajaj')


class TestServiceDeskFlow(BaseTestCase):
    multi_db=True
    def setUp(self):
        TestCase.setUp(self)
        BaseTestCase.setUp(self)
        self.client = Client()
        self.system = System(self)
        self.brand = Brand(self)
        brand = self.brand
        system = self.system
        self.create_user(username='gladminds', email='gladminds@gladminds.co', password='gladminds')
        brand.send_service_advisor_feed()
        system.create_sdo(username='sdo', email='gm@gm.com', password='123', phone_number="+910000000000")
        system.create_sdm(username='sdm', email='gm@gm.com', password='123', phone_number="+911234567890")
        system.create_sla(priority="Low")
        system.create_sla(priority="High")
        system.create_dealer(username='dealer', email='dealer@xyz.com', password='123', phone_number="+919999999999")
                
    def test_send_servicedesk_feedback(self):
        initiator = self.system
        SMSLog.objects.all().delete()
        initiator.post_feedback()
        sms_log_len_after = SMSLog.objects.all()
        feedback_obj = Feedback.objects.all()
        initiator.verify_result(input=feedback_obj[0].priority, output="Low")
        initiator.verify_result(input=len(sms_log_len_after), output=2)
        initiator.verify_result(input=sms_log_len_after[0].receiver, output="9999999999")
    
    def test_get_feedback_sdo(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_owner = self.system
        service_desk_owner.login(username='sdo', password='123', provider='desk', group_name=Roles.SDOWNERS)
        service_desk_owner.get_feedback_information()
        feedback_obj = Feedback.objects.all()
        system = self.system
        system.verify_result(input=feedback_obj[0].priority, output="Low")

    
    def test_get_feedback_sdm(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        service_desk_manager.get_feedback_information()
        feedback_obj = Feedback.objects.all()
        system = self.system
        system.verify_result(input=feedback_obj[0].priority, output="Low")
 
    def test_sms_assignee_after_feedback_assigned(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        SMSLog.objects.all().delete()
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response = service_desk_manager.update_feedback(status='Open')
        self.assertEqual(response.status_code, 200)
        sms_log_len_after = SMSLog.objects.all()
        system = self.system
        system.verify_result(input=sms_log_len_after[0].receiver, output="9999999999")
        system.verify_result(input=sms_log_len_after[1].receiver, output="9999999999")

    def test_sms_after_resolved(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response = service_desk_manager.update_feedback(status='Open')
        self.assertEqual(response.status_code, 200)
        service_desk_owner = self.system
        service_desk_owner.login(username='sdo', password='123', provider='desk', group_name=Roles.SDOWNERS)
        response = service_desk_owner.update_feedback(status='resolved', assign_to='sdo')
        self.assertEqual(response.status_code, 200)
        system = self.system
        feedback_obj = Feedback.objects.all()
        system.verify_result(input=feedback_obj[0].status, output="resolved")
 
    def test_updated_feedback(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response = service_desk_manager.update_feedback(status='Closed', assign_to=None)
        self.assertEqual(response.status_code, 200)
        feedback_obj = Feedback.objects.all()
        system = self.system
        system.verify_result(input=feedback_obj[0].status, output='Closed')

    def test_new_dealer(self):
        dealer = self.system
        dealer.login(username='dealer', password='123', provider='dealer', group_name='dealers')

    def test_update_due_date(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response = service_desk_manager.update_feedback()
        self.assertEqual(response.status_code, 200)
        sleep(2)
        response = service_desk_manager.update_feedback(due_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user = User.objects.get(username='GMDEALER001SA01')
        user.email = 'sa@sa.com'
        user.save()
        sleep(2)
        response = service_desk_manager.update_feedback(due_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(response.status_code, 200)
        
        
    def test_pending_time(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response=service_desk_manager.update_feedback(status='Open')
        self.assertEqual(response.status_code, 200)
        response=service_desk_manager.update_feedback(status='Pending')
        self.assertEqual(response.status_code, 200)
        sleep(50)
        response=service_desk_manager.update_feedback(status='Resolved')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Feedback.objects.get(id=1).wait_time >= 50.0)
        
    def test_assign_to_reporter_when_pending(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response=service_desk_manager.update_feedback(status='Open', assign_to='sdo')
        self.assertEqual(response.status_code, 200)
        system = self.system
        system.verify_result(input=Feedback.objects.get(id=1).assignee.user_profile.user.username,
                             output= 'sdo')
        response=service_desk_manager.update_feedback(status='Pending', reporter_status="true")
        system.verify_result(input=Feedback.objects.get(id=1).assignee.user_profile.user.username,
                             output= 'dealer')
        self.assertEqual(response.status_code, 200)
        
    def test_assign_to_previous_assignee(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response=service_desk_manager.update_feedback(status='Open', assign_to='sdo')
        self.assertEqual(response.status_code, 200)
        system = self.system
        system.verify_result(input=Feedback.objects.get(id=1).assignee.user_profile.user.username,
                             output= 'sdo')
        response=service_desk_manager.update_feedback(status='Pending', reporter_status="true")
        system.verify_result(input=Feedback.objects.get(id=1).assignee.user_profile.user.username,
                             output= 'dealer')
        self.assertEqual(response.status_code, 200)
        response=service_desk_manager.update_feedback(status='In Progress')
        system.verify_result(input=Feedback.objects.get(id=1).assignee.user_profile.user.username,
                             output= 'sdo')
        self.assertEqual(response.status_code, 200)
        
    def test_edit_comment(self):
        initiator = self.system
        initiator.post_feedback()
        service_desk_manager = self.system
        service_desk_manager.login(username='sdm', password='123', provider='desk', group_name=Roles.SDMANAGERS)
        response=service_desk_manager.update_feedback(status='Open', assign_to='sdo', comments='hello')
        system = self.system
        system.verify_result(input=Comment.objects.get(id=1).comment, output= 'hello')
        self.assertEqual(response.status_code, 200)
        response=service_desk_manager.update_comment(commentDescription='test')
        system.verify_result(input=Comment.objects.get(id=1).comment, output= 'test')
        self.assertEqual(response.status_code, 200)

