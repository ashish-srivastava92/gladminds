from django.conf import settings
from gladminds.utils import import_json
import json
import requests

__all__ = ['AirtelSmsClient']
class SmsClientExcetion(Exception):
    
    def __init__(self, message, args = []):
        Exception.__init__(self, message)
        self.args = args
    
    def __unicode__(self):
        return u"%s" % self.message

class SmsClientSessionExpire(Exception):{}

class SmsClientMessageFailted(Exception):{}

class SmsClientBaseObject(object):
    
    def __init__(self, username, password, authenticate_url = None, message_url = None):
        """Set username and password"""
        self.username = username
        self.password = password
        self.authenticate_url = authenticate_url
        self.message_url = message_url
        self.session_id = None
        
    """Authenticate the user and return session Id"""
    def authenticate(self):
        return
        
    def send(self, type, **kwargs):
        return_data = None
        if type=="stateless":
            return_data = self.send_stateless(**kwargs)
        else:
            return_data = self.send_stateful(**kwargs)
        return return_data
    
    """"This method doesn't require http session, username and password mendatory"""
    def send_stateless(self, **kwargs): 
        return 
    
    """Send the message using Http session"""
    def send_stateful(self, **kwargs):
        return
    
    def bulk_sms(self, **kwargs):
        return 
    
    def _get_session_id(self):
        return self.session_id
    
    def _set_session_id(self, session_id):
        self.session_id = session_id

class AirtelSmsClient(SmsClientBaseObject):
    
    def __init__(self, username, password, authenticate_url, message_url):
        AirtelSmsClient.__init__(self, username, password, authenticate_url, message_url)
    
    def authenticate(self):
        params = {'login':self.username, 'pass': self.password}
        return self.send_request(url = self.authenticate_url, params = parama)

    def send_stateless(self, **kwargs):
        phone_number = kwargs['phone_number']
        message = kwargs['message']
        session_id = self._get_session_id()
        params = {'mob_no' : phone_number, 'text' : message, 'username' : self.username, 'password': self.password}
        return self.send_request(url = self.message_url, params = parama)
    
    def send_stateful(self, **kwargs):
        phone_number = kwargs['phone_number']
        message = kwargs['message']
        session_id = self._get_session_id()
        params = {'mob_no' : phone_number, 'text' : message, 'sessionID' : session_id}
        return self.send_request(url = self.message_url, params = parama)
    
    def send_request(self, url, params):
        resp = requests.get(url = url, params = params)
        assert resp.status_code==200
        json = import_json()
        data = resp.content
        return json.loads(data)

class MockSmsClient(SmsClientBaseObject):
    
    def __init__(self, username, password, authenticate_url, message_url):
        AirtelSmsClient.__init__(self, username, password, authenticate_url, message_url)
    
    def authenticate(self):
        return {"sessionID":"23ef53u78s090df9ac0vvg011f"}
    
    def send_stateless(self):
        return {"jobId":695, "message":"Your message has been successfully sent", "messagesLeft":99999862}
    
    def send_stateful(self, **kwargs):
        return {"sessionID":"23ef53u78s090df9ac0vvg011f", "jobId":695, "message":"Your message has been successfully sent", "messagesLeft":99999862}
    
        