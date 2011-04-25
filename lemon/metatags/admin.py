from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin
from lemon.extradmin import generic
from lemon.metatags.models import Page
from lemon.metatags.widgets import AdminSmallTextareaWidget


class PageInline(generic.GenericStackedInline):

    model = Page
    exclude = ('url_path', 'language', 'sites')
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.TextField: {'widget': AdminSmallTextareaWidget},
    }


class PageAdmin(extradmin.ModelAdmin):

    list_display = ('url_path', 'title', 'title_extend', 'language', 'enabled')
    list_display_links = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': AdminSmallTextareaWidget},
    }
    string_overrides = {
        'add_title': _(u'Add page'),
        'change_title': _(u'Change page'),
        'changelist_title': _(u'Choose page to change'),
        'changelist_popup_title': _(u'Choose page'),
        'changelist_addlink_title': _(u'Add page'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d page', '%(count)d pages', n),
    }


extradmin.site.register(Page, PageAdmin)
