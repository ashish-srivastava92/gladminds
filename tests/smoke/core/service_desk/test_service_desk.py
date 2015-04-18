from smoke.utility import UtilityResourceTest
from time import sleep
import datetime
class TestServiceDesk(UtilityResourceTest):        
    def test_send_servicedesk_feedback(self):
        self.post_feedback('10316','123')
        sms=self.get_sms(phone_number='1111222292')
        self.check_result(result=sms[0], value="1111222292", parameter="receiver")
        result=self.get_feedbacks('10316','123')
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
        self.update_feedback(username='sdo', password='123',status='resolved')
        result=self.get_feedbacks('10316','123')
        self.check_result(result=result, value="resolved", parameter="status")
        
    def test_updated_feedback(self):
        self.post_feedback('10316', '123')
        self.update_feedback(username="sdm", password="123")
        self.update_feedback(username="sdo",password="123",status='Closed') 
        result=self.get_feedbacks('10316','123')
        self.check_result(result=result, value="Closed", parameter="status")
    
    def test_update_due_date(self):
        self.post_feedback('10316', '123')
        self.update_feedback(username="sdm", password="123") 
        sleep(4)
        self.update_feedback(username="sdm", password="123",due_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def test_pending_time(self):
        self.post_feedback('10316','123')
        self.update_feedback(username='sdm',password='123',status='Open')
        self.update_feedback(username='sdm',password='123',status='Pending')
        sleep(50)
        self.update_feedback(username='sdm',password='123',status='Resolved')
        result=self.get_feedbacks('sdm','123')
        raise
        self.assertTrue(result['wait_time'] >= 50.0)
    
    def test_assign_to_reporter_when_pending(self):
        self.post_feedback('10316','123')
        self.update_feedback(username='sdm', password='123',status='Open', assign_to='sdo')
        result=self.get_feedbacks('sdm','123')
        self.check_result(result=result['assignee']['user'],parameter='user',inner_parameter='username',value= 'sdo')
        self.update_feedback(username='sdm', password='123',status='Pending', reporter_status="true")
        result=self.get_feedbacks('sdm','123')
        self.check_result(result=result['assignee']['user'],parameter='user',inner_parameter='username',value= '10316')
   
    def test_assign_to_previous_assignee(self):
        self.post_feedback('10316','123')
        self.update_feedback(username='sdm', password='123',status='Open', assign_to='sdo')
        result=self.get_feedbacks('sdm','123')
        self.check_result(result=result['assignee']['user'],parameter='user',inner_parameter='username',value= 'sdo')
        self.update_feedback(username='sdm', password='123',status='Pending', reporter_status="true")
        result=self.get_feedbacks('sdm','123')
        self.check_result(result=result['assignee']['user'],parameter='user',inner_parameter='username',value= '10316')
        self.update_feedback(username='sdm', password='123',status='In Progress')
        result=self.get_feedbacks('sdm','123')
        self.check_result(result=result['assignee']['user'],parameter='user',inner_parameter='username',value= 'sdo')
        
    def test_edit_comment(self):
        self.post_feedback('10316','123')
        self.update_feedback(username='sdm', password='123',status='Open', assign_to='sdo', comments='hello')
        result=self.get_comments()
        comment_id=str(result['id'])
        self.check_result(result=result,parameter='comment',value= 'hello')
        result=self.get_feedbacks('10316','123')
        ticket_id=str(result['id'])
        self.update_comments(username='sdm',password='123',commentDescription='test',ticket_id=ticket_id,comment_id=comment_id)
        result=self.get_comments()
        self.check_result(result=result,parameter='comment', value= 'test')
