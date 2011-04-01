from django.conf import settings
from django.contrib.sites.models import SITE_CACHE, Site, RequestSite


DOMAIN_CACHE = {}


class LazySite(object):

    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_site'):
            domain = request.get_host().split(':')[0]
            try:
                site = SITE_CACHE[DOMAIN_CACHE[domain]]
            except KeyError:
                site = self._get_site(domain)
                if site:
                    DOMAIN_CACHE[domain] = site.pk
                    SITE_CACHE[site.pk] = site
                else:
                    site = RequestSite(request)
            request._cached_site = site
        return request._cached_site
    
    def _get_site(self, domain):
        try:
            return Site.objects.get(domain=domain)
        except (Site.DoesNotExist, Site.MultipleObjectsReturned):
            try:
                return Site.objects.get(pk=settings.SITE_ID)
            except Site.DoesNotExist:
                return None


class RequestSiteMiddleware(object):

    def process_request(self, request):
        request.__class__.site = LazySite()
