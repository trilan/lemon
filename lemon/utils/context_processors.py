from django.contrib.sites.models import RequestSite
from django.utils.functional import LazyObject


class ContextLazyObject(LazyObject):
    
    def __init__(self, func):
        self.__dict__['_setupfunc'] = func
        self._wrapped = None
    
    def _setup(self):
        self._wrapped = self._setupfunc()


def site(request):
    def get_site():
        if hasattr(request, 'site'):
            return request.site
        else:
            return RequestSite(request)
    return {'site': ContextLazyObject(get_site)}
