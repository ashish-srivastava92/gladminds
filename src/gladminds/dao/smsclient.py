from django.conf import settings
from gladminds.utils import import_json
import json
import requests

__all__ = ['AirtelSmsClient', 'TwilioSmsClient']

def load_gateway():
    client = settings.SMS_CLIENT_DETAIL
    if settings.SMS_CLIENT is 'MOCK':
        return MockSmsClient(**client)
    elif settings.SMS_CLIENT is 'AIRTEL':
        return AirtelSmsClient(**client)
    elif settings.SMS_CLIENT is 'TWILIO':
        return TwilioSmsClient(**client)
        
class SmsClientExcetion(Exception):
    
    def __init__(self, message, args = []):
        Exception.__init__(self, message)
        self.args = args
    
    def __unicode__(self):
        return u"%s" % self.message

class SmsClientSessionExpire(Exception):{}

class SmsClientMessageFailted(Exception):{}

class MessageSentFailed(Exception):{}

class SmsClientBaseObject(object):
    
    def __init__(self, *args, **kwargs):
        """Set username and password"""
        self.login = kwargs['login']
        self.password = kwargs['pass']
        self.authenticate_url = kwargs['authenticate_url']
        self.message_url = kwargs['message_url']
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
    
    def __init__(self, *args, **kwargs):
        SmsClientBaseObject.__init__(self, *args, **kwargs)
    
    def authenticate(self):
        params = {'login':self.login, 'pass': self.password}
        return self.send_request(url = self.authenticate_url, params = params)

    def send_stateless(self, **kwargs):
        phone_number = kwargs['phone_number']
        message = kwargs['message']
        session_id = self._get_session_id()
        params = {'mob_no' : phone_number, 'text' : message, 'login' : self.login, 'pass': self.password}
        return self.send_request(url = self.message_url, params = params)
    
    def send_stateful(self, **kwargs):
        phone_number = kwargs['phone_number']
        message = kwargs['message']
        session_id = self._get_session_id()
        params = {'mob_no' : phone_number, 'text' : message, 'sessionID' : session_id}
        return self.send_request(url = self.message_url, params = params)
    
    def send_request(self, url, params):
        resp = requests.get(url = url, params = params)
        assert resp.status_code==200
#         json = import_json()
#         data = resp.content
        return resp.status_code

class MockSmsClient(SmsClientBaseObject):
    
    def __init__(self, *args, **kwargs):
        pass
    
    def authenticate(self, **kwargs):
        return {"sessionID":"23ef53u78s090df9ac0vvg011f"}
    
    def send_stateless(self, **kwargs):
        return {"jobId":695, "message":"Your message has been sent to {0}".format(kwargs['phone_number']), "messagesLeft":99999862}
    
    def send_stateful(self, **kwargs):
        return {"sessionID":"23ef53u78s090df9ac0vvg011f", "jobId":695, "message":"Your message has been successfully sent", "messagesLeft":99999862}
        
class TwilioSmsClient(SmsClientBaseObject):
    
    def __init__(self, *args, **kwargs):
        self.account_key  = kwargs['OTP_TWILIO_ACCOUNT']
        self.auth_key = kwargs['OTP_TWILIO_AUTH']
        self.sender = kwargs['OTP_TWILIO_FROM']
        self.uri = kwargs['OTP_TWILIO_URI']
    
    def authenticate(self, **kwargs):
        return {"sessionID":"23ef53u78s090df9ac0vvg011f"}
    
    def send_stateless(self, **kwargs):
        url = self.uri.format(self.account_key)
        data = {
            'From': self.sender,
            'To': str(kwargs['phone_number']),
            'Body': kwargs['message'],
        }
        response = requests.post(url = url, data=data, auth=(self.account_key, self.auth_key))
        status_code = response.status_code
        if (status_code>=400):
            raise MessageSentFailed("Not able to sent sms")
        
    def send_stateful(self, **kwargs):
        url = self.uri.format(self.account_key)
        data = {
            'From': self.sender,
            'To': str(kwargs['phone_number']),
            'Body': kwargs['message'],
        }
        response = requests.post(url = url, data=data, auth=(self.account_key, self.auth_key))