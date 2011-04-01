from lemon import sitemaps
from lemon.pages.models import Page


sitemaps.site.register(Page, sites_field_name='site')
