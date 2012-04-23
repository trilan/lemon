from django.contrib.sites.models import RequestSite
from django.utils.functional import SimpleLazyObject


def site(request):
    def get_site():
        if hasattr(request, 'site'):
            return request.site
        else:
            return RequestSite(request)
    return {'site': SimpleLazyObject(get_site)}
