from django.conf.urls.defaults import patterns, url
from lemon.sitemaps.views import sitemap_xml


urlpatterns = patterns('',
    url(r'^$', sitemap_xml, name='sitemap_xml'),
)
