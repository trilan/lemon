from django.conf.urls.defaults import url
from lemon.sitemaps.views import sitemap_xml


urls = [
    url(r'^sitemap\.xml$', sitemap_xml, name='sitemap_xml'),
]
