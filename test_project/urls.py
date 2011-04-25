from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.static import static

from lemon import extradmin
from lemon.utils import urls


extradmin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(extradmin.site.urls)),
    url(r'^robots\.txt', include('lemon.robots.urls')),
    url(r'^sitemap\.xml', include('lemon.sitemaps.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
