from smoke.utility import UtilityResourceTest
from time import sleep
import datetime
class TestServiceDesk(UtilityResourceTest):        
    def test_send_servicedesk_feedback(self):
        self.post_feedback('10316','123')
        sms=self.get_sms(phone_number='1111222292')
        self.check_result(result=sms[0], value="1111222292", parameter="receiver")
        result=self.get_feedbacks('10316','123')
        print result,"=================================="
        self.check_result(result=result, value="Low", parameter="priority")
    
    def test_get_feedback_sdo(self):
        self.post_feedback('10316','123')
        self.update_feedback(username="10316",password="123")
        self.get_feedbacks_as_sduser(username='sdo',password='123')
        result=self.get_feedbacks('sdo','123')
        self.check_result(result=result, value="High", parameter="priority")
    
    def test_get_feedback_sdm(self):
        self.post_feedback('10316','123')
        self.get_feedbacks_as_sduser(username='sdm',password='123')
        result=self.get_feedbacks('sdm','123')
        self.check_result(result=result, value="Low", parameter="priority")
    
    def test_sms_assignee_after_feedback_assigned(self):
        self.post_feedback('10316', '123')
        self.update_feedback(username="sdm",password="123",status='Open')
        sms=self.get_sms(phone_number='1111222292')
        self.check_result(result=sms[0], value="1111222292", parameter="receiver")
    
    def test_sms_after_resolved(self):
        self.post_feedback('10316', '123')
        self.update_feedback(username="sdm", password="123",status='Open')
        self.update_feedback(username='sdo', password='123',status='resolved', assign_to='sdo')
        result=self.get_feedbacks('10316','123')
        print result,"=================================="
        self.check_result(result=result, value="resolved", parameter="status")
        
    def test_updated_feedback(self):
        self.post_feedback('10316', '123')
        self.update_feedback(username="sdm", password="123",status='Closed') 
        result=self.get_feedbacks('10316','123')
        print result,"=================================="
        self.check_result(result=result, value="Closed", parameter="status")
    
    def test_update_due_date(self):
        self.post_feedback('10316', '123')
        self.update_feedback(username="sdm", password="123") 
        sleep(2)
        self.update_feedback(username="sdm", password="123",due_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") )