from django.contrib.contenttypes.generic import BaseGenericInlineFormSet 
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin
from lemon.extradmin import generic
from lemon.metatags.models import Page
from lemon.metatags.widgets import AdminSmallTextareaWidget


class PageInline(generic.GenericStackedInline):

    model = Page
    exclude = ('url_path', 'sites')
    extra = 1
    max_num = 1
    formfield_overrides = {
        models.TextField: {'widget': AdminSmallTextareaWidget}}


class PageAdmin(extradmin.ModelAdmin):

    list_display = ['url_path', 'title', 'title_extend', 'enabled']
    list_display_links = ('title',)
    formfield_overrides = {
        models.TextField: {'widget': AdminSmallTextareaWidget}}
    string_overrides = {
        'add_title': _(u'Add meta tags'),
        'change_title': _(u'Change meta tags'),
        'changelist_title': _(u'Choose meta tags to change'),
        'changelist_popup_title': _(u'Choose meta tags'),
        'changelist_addlink_title': _(u'Add meta tags'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d meta tags entry', '%(count)d meta tags entries', n)
    }


extradmin.site.register(Page, PageAdmin)
