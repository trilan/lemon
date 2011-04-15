from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.static import static

from lemon import extradmin
from lemon import sitemaps
from lemon.utils import urls


extradmin.autodiscover()
sitemaps.autodiscover()
urlpatterns = patterns('', *urls.autodiscover())
urlpatterns += patterns('',
    url(r'^admin/', include(extradmin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
