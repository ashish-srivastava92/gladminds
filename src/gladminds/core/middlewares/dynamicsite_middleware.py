from django.conf import settings
from django.utils.cache import patch_vary_headers

from gladminds.core.utils import make_tls_property

import logging
logger = logging.getLogger('gladminds')

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
        BRAND.value = self.get_fields(self.domain)
        if BRAND.value not in settings.BRANDS:
            BRAND.value = settings.GM_BRAND
        
        if settings.ENV=='test':
            BRAND.value = 'bajaj'

        try:
            if BRAND.value not in settings.GM_BRAND:
                request.urlconf = 'gladminds.{0}.urls'.format(BRAND.value)
        except KeyError:
            # use default urlconf (settings.ROOT_URLCONF)
            pass
        logger.info('BRAND is {0}, HOST is {1}'.format(BRAND.value,
                                                       request.get_host()))

    def process_response(self, request, response):
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response

    def get_fields(self, domain):
        fields = domain.split('.')
        if fields[0] in ['local', 'dev', 'qa', 'staging']:
            fields = fields[1:]
        return fields[0]

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
