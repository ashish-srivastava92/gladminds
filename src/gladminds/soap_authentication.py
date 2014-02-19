import base64
from django.contrib import auth
from spyne.model.fault import Fault

class AuthenticationError(Fault):
    __namespace__ = 'gladminds.webservice.authentication'

    def __init__(self, user_name):
        # TODO: self.transport.http.resp_code = HTTP_401

        super(AuthenticationError, self).__init__(
                faultcode='Client.AuthenticationError',
                faultstring='Invalid authentication request for %r' % user_name
            )
        
class AuthorizationError(Fault):
    __namespace__ = 'gladminds.webservice.authentication'

    def __init__(self):
        # TODO: self.transport.http.resp_code = HTTP_401

        super(AuthorizationError, self).__init__(
                faultcode='Client.AuthorizationError',
                faultstring='You are not authozied to access this resource.'
            )

class AuthenticationService(object):
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def authenticate(self):
        user = auth.authenticate(username=self.username, password=self.password)
        if user is None:
            raise AuthenticationError(self.username)
        return True