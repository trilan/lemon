from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lemon import extradmin
from lemon.publications.admin import PublicationAdmin
from lemon.pages.models import Page
from lemon.pages.forms import PageAdminForm


class PageAdmin(PublicationAdmin):

    form = PageAdminForm
    date_hierarchy = None
    search_fields = ['title', 'content']
    markup_fields = ('content',)
    fieldsets = (
        (None, {
            'fields': ('url_path', 'title', 'content', 'template', 'language', 'sites')
        }),
    ) + PublicationAdmin.fieldsets
    list_display = ('url_path', 'title', 'author_name', 'language', 'enabled')
    list_display_links = ('title',)
    list_filter = ('enabled', 'language', 'sites')
    tabs = True


extradmin.site.register(Page, PageAdmin)

section = extradmin.site.menu.section('content')
section.add_item('text pages', model=Page, title=_(u'Text pages'))

if 'lemon.metatags' in settings.INSTALLED_APPS:
    from lemon import metatags
    metatags.site.register(Page,
        language_field_name = 'language',
        sites_field_name = 'sites'
    )

if 'lemon.sitemaps' in settings.INSTALLED_APPS:
    from lemon import sitemaps
    sitemaps.site.register(Page,
        language_field_name = 'language',
        sites_field_name='sites',
    )
