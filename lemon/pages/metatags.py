from lemon import metatags
from lemon.pages.models import Page


metatags.site.register(Page, sites_field_name='site')
