from django.conf import settings
from django.core import urlresolvers
from django.http import Http404

from lemon.pages.views import page


class PageMiddleware(object):

    def process_response(self, request, response):
        if response.status_code != 404:
            return response
        if hasattr(request, 'urlconf'):
            urlresolvers.set_urlconf(request.urlconf)
        try:
            return page(request, request.path_info)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
        finally:
            urlresolvers.set_urlconf(None)
