from django.conf import settings
from gladminds.core.utils import make_tls_property

BRAND = settings.__dict__['_wrapped'].__class__.BRAND = make_tls_property()


class DynamicSitesMiddleware(object):
    """
    Sets settings.BRAND based on request's domain.
    Also handles hostname redirects, and ensures the
    proper subdomain is requested for the site
    """
    def process_request(self, request):
        self.request = request
        self.domain, self.port = self.get_domain_and_port()
        BRAND.value = self.domain.split('.')[0]
        if BRAND.value not in settings.BRANDS:
            BRAND.value = 'gm'

    def get_domain_and_port(self):
        """
        Django's request.get_host() returns the requested host and possibly the
        port number.  Return a tuple of domain, port number.
        Domain will be lowercased
        """
        host = self.request.get_host()
        if ':' in host:
            domain, port = host.split(':')
            return (domain.lower(), port)
        else:
            return (host.lower(),
                self.request.META.get('SERVER_PORT'))
