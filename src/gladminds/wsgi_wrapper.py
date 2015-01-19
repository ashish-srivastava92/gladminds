"""
This is not used anymore. but keeping it in project, perhaps we need it in future
"""

from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import WsgiMounter

class GladmindsWsgiMounter(WsgiMounter):
    """Simple mounter object for wsgi callables. Takes a dict where the keys are
    uri fragments and values are :class:`spyne.application.Application`
    instances.

    :param mounts: dict of :class:`spyne.application.Application` instances
    whose keys are url fragments.
    """
    def __init__(self, mounts=None, default = None):
        super(GladmindsWsgiMounter, self).__init__(mounts = mounts)
        self.app_default = default

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        fragments = [a for a in path_info.split('/') if len(a) > 0]

        script = ''
        if len(fragments) > 0:
            script = fragments[0]

        app = self.mounts.get(script, self.app_default)

        original_script_name = environ.get('SCRIPT_NAME', '')

        environ['SCRIPT_NAME'] = ''.join(('/', original_script_name, script))
        environ['PATH_INFO'] = ''.join(('/', '/'.join(fragments[1:])))
        
        return app(environ, start_response)