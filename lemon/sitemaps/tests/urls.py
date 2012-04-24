from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^sitemap\.xml', include('lemon.sitemaps.urls')),
)
