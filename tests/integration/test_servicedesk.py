from django.core import mail
from django.conf import settings 
from django.contrib.auth.models import User, Group
from django.test.client import Client

from integration.base_integration import GladmindsResourceTestCase
from provider.oauth2.models import Client as auth_client
from provider.oauth2.models import AccessToken
from gladminds.models import common
from gladminds.aftersell.models import common as aftersell_common
from gladminds.mail import send_feedback_received,send_servicedesk_feedback
from gladminds.aftersell.models import logs
 
import json
client = Client()

class TestServiceDesk_Flow(GladmindsResourceTestCase):
    def setUp(self):
        super(TestServiceDesk_Flow, self).setUp()
        self.access_token = 'testaccesstoken'
        user = User.objects.create_user(username='gladminds', email='gm@gm.com', password='gladminds')
        user.save()
        user_group = Group.objects.get(name='dealers')
        user.groups.add(user_group)
        user_obj=User.objects.filter(username='gladminds')
        user_info = common.GladMindUsers(user=user_obj[0],phone_number='+9199999998')
        user_info.save()
        user_servicedesk = User.objects.create_user(username='sdo', email='gm@gm.com', password='123')
        user_servicedesk.save()
        user_group = Group.objects.create(name='SDM')
        user_group.save()
        user_servicedesk.groups.add(user_group)
        user_servicedesk_owner = User.objects.create_user(username='sdoo', email='gm@gm.com', password='123')
        user_servicedesk_owner.save()
        user_group = Group.objects.create(name='SDO')
        user_group.save()
        user_servicedesk_owner.groups.add(user_group)
        dealer_obj = self.get_delear_obj(dealer_id='gladminds')
        service_advisor = self.get_service_advisor_obj(service_advisor_id='SA001Test', name='UMOTO', phone_number='+914444861111')
        self.get_dealer_service_advisor_obj(dealer_id=dealer_obj, service_advisor_id=service_advisor, status='Y')
        service_advisor1 = self.get_service_advisor_obj(service_advisor_id='SA002Test', name='UMOTOR', phone_number='+919999999998')
        self.get_dealer_service_advisor_obj(dealer_id=dealer_obj, service_advisor_id=service_advisor1, status='Y')
        data = {'username':'gladminds', 'password':'gladminds'}  
        response = client.post("/aftersell/dealer/login/", data=data)
        data = {"messsage":"test","priority":"High","advisorMobile":"+919999999998",
                "type":"Problem", "subject":"hello",'comments':"sssss", "rootcause":"ssss", "resolution":"ssssss" }
        response = client.post("/aftersell/servicedesk/helpdesk", data=data)
        self.assertEqual(response.status_code, 200)
    
    def test_new_dealer(self):
        data = {'username':'gladminds', 'password':'gladminds'}  
        response = client.post("/aftersell/dealer/login/", data=data)
        self.assertEqual(response.status_code, 302)

    def test_send_servicedesk_feedback(self):
        log_len_after = logs.AuditLog.objects.all()
        feedback_obj = aftersell_common.Feedback.objects.all()
        self.assertEqual(feedback_obj[0].priority, "High")
        self.assertEqual(len(log_len_after),1)
        self.assertEqual(log_len_after[0].reciever, "9999999998")
        
    def test_get_feedback_sdo(self):
        data = {'username':'sdo', 'password':'123'}  
        response = client.post("/aftersell/desk/login/", data=data)
        self.assertEqual(response.status_code, 302)
        response = client.get("/aftersell/servicedesk/")
        self.assertEqual(response.status_code, 200)
        
    def test_get_feedback_sdm(self):
        data = {'username':'sdoo', 'password':'123'}  
        response = client.post("/aftersell/desk/login/", data=data)
        self.assertEqual(response.status_code, 302)
        user_servicedesk_info = User.objects.filter(username='sdoo')
        service_desk = aftersell_common.ServiceDeskUser(user = user_servicedesk_info[0], phone_number = '+919727071081', email_id = 'srv.sngh@gmail.com',  designation = 'SDM' )
        service_desk.save()
        response = client.get("/aftersell/servicedesk/")
        self.assertEqual(response.status_code, 200)    
            
         
    def test_sms_email_assignee_after_feedback_assigned(self):
        log_len_after = logs.AuditLog.objects.all()
        user_servicedesk_info = User.objects.filter(username='sdo')
        service_desk = aftersell_common.ServiceDeskUser(user = user_servicedesk_info[0], phone_number = '+917760814041', email_id = 'srv.sngh@gmail.com',  designation = 'SDM' )
        service_desk.save()
        data = {"Assign_To":"+917760814041","status":"Open","Priority":"High","comments":"ssss", "rootcause":"ssss", "resolution":"ssssss","due_date":'12/08/1922', 'reporter_status':False}
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        log_len_after = logs.AuditLog.objects.all()
        self.assertEqual(log_len_after[1].reciever, "9999999998")
        self.assertEqual(log_len_after[2].reciever , "7760814041")
        
        
    def test_sms_email_after_resolved(self):
        log_len_after = logs.AuditLog.objects.all()
        user_servicedesk_info = User.objects.filter(username='sdo')
        service_desk = aftersell_common.ServiceDeskUser(user = user_servicedesk_info[0], phone_number = '+917760814041', email_id = 'srv.sngh@gmail.com',  designation = 'SDM' )
        service_desk.save()
        user_servicedesk_info = User.objects.filter(username='sdoo')
        service_desk = aftersell_common.ServiceDeskUser(user = user_servicedesk_info[0], phone_number = '+919727071081', email_id = 'srv.sngh@gmail.com',  designation = 'SDM' )
        service_desk.save()
        data = {"Assign_To":"+917760814041","status":"Resolved","Priority":"High","comments":"ssss", "rootcause":"ssss", "resolution":"ssssss","due_date":'12/08/1922', 'reporter_status':False}
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        log_len_after = logs.AuditLog.objects.all()
        self.assertEqual(log_len_after[1].reciever, "9999999998")
        self.assertEqual(log_len_after[2].reciever , "9999999998") 
        self.assertEqual(log_len_after[3].reciever , "7760814041")   
        
        
    def test_sms_email_after_status_resolved_not_assign_to_anyone(self):
        log_len_after = logs.AuditLog.objects.all()
        user_servicedesk_info = User.objects.filter(username='sdo')
        service_desk = aftersell_common.ServiceDeskUser(user = user_servicedesk_info[0], phone_number = '+917760814041', email_id = 'srv.sngh@gmail.com',  designation = 'SDM' )
        service_desk.save()
        user_servicedesk_info = User.objects.filter(username='sdoo')
        service_desk = aftersell_common.ServiceDeskUser(user = user_servicedesk_info[0], phone_number = '+919727071081', email_id = 'srv.sngh@gmail.com',  designation = 'SDM' )
        service_desk.save()
        data = {"Assign_To":'',"status":"Resolved","Priority":"High","comments":"ssss", "rootcause":"ssss", "resolution":"ssssss","due_date":'12/08/1922', 'reporter_status':False}
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        log_len_after = logs.AuditLog.objects.all()
        self.assertEqual(log_len_after[1].reciever, "9999999998")
        
            
    def test_updated_feedback(self):
        log_len_after = logs.AuditLog.objects.all()
        data = {"Assign_To":'',"status":"Closed","Priority":"High","comments":"ssss","rootcause":"ssss", "resolution":"ssssss","due_date":'12/08/1922', 'reporter_status':False}
        response = client.post("/aftersell/feedbackdetails/1/", data=data)
        feedbacks = aftersell_common.Feedback.objects.filter(priority = 'High')
        log_len_after = logs.AuditLog.objects.all()
        self.assertEqual(feedbacks[0].priority  ,'High')     
              
               
class GladmindsUrlsTest(GladmindsResourceTestCase):
    def setUp(self):
        super(GladmindsUrlsTest, self).setUp()       
                 