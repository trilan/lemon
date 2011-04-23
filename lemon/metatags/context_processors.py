import re

from django.utils.functional import SimpleLazyObject
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from lemon.metatags import settings
from lemon.metatags.models import Page


class MetaContextObject(object):

    def __init__(self, url_path, site):
        metatags = self._get_metatags(url_path, site)
        if metatags and metatags.enabled:
            self.title = self._get_title(metatags, site)
            self.keywords = metatags.keywords
            self.description = metatags.description
            self.enabled = True
        else:
            self.title = self.keywords = self.description = ''
            self.enabled = False

    def _get_metatags(self, url_path, site):
        queryset = Page.objects.filter(
            url_path = url_path,
            language = get_language(),
            sites = site,
            enabled = True,
        )
        try:
            return queryset[0]
        except IndexError:
            return None

    def _get_title(self, metatags, site):
        titles = [metatags.title]
        if metatags.title_extend:
            titles.append(site.name)
        titles.reverse() if settings.TITLE_REVERSED else titles
        return mark_safe(settings.TITLE_SEPARATOR.join(titles))


def metatags(request):
    return {'metatags': SimpleLazyObject(lambda: MetaContextObject(request.path, request.site))}
