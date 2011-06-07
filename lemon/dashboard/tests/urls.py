from django.conf.urls.defaults import patterns, url, include
from .admin import first_admin_site, second_admin_site


urlpatterns = patterns('',
    url(r'^first_admin/', include(first_admin_site.urls)),
    url(r'^second_admin/', include(second_admin_site.urls)),
)
