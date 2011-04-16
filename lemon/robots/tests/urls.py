from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('',
    url(r'^robots\.txt', include('lemon.robots.urls')),
)
