import base64
from django.contrib.auth import authenticate
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

class BasicAuthentication(object):
    def __init__(self, auth = None):
        self.auth = auth
        
    def is_authenticated(self):
        auth_detail = self.auth
        if not auth_detail:
            raise AuthorizationError()
        try:
            (auth_type, data) = auth_detail.split()
            if auth_type.lower() != 'basic':
                raise AuthorizationError()
            user_pass = self.decode_base64(data = data)
        except:
            raise AuthorizationError()
        bits = user_pass.split(':', 1)
        if len(bits) != 2:
            raise AuthorizationError()

        user = authenticate(username=bits[0], password=bits[1])
        if user is None:
            raise AuthenticationError(bits[0])
        return True

    def decode_base64(self, data = None):
        print "data:", data
        """Decode base64, padding being optional.
        :param data: Base64 data as an ASCII byte string
        :returns: The decoded byte string.
        """
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'='* missing_padding
        return base64.decodestring(data)