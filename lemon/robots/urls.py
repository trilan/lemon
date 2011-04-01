from django.conf.urls.defaults import url
from lemon.robots.views import robots_txt


urls = [
    url(r'^robots\.txt$', robots_txt, name='robots_txt'),
]
