from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin
from lemon.extradmin import generic
from lemon.sitemaps.models import Item


class ItemForm(forms.ModelForm):

    def has_changed(self):
        return True


class ItemInline(generic.GenericStackedInline):

    form = ItemForm
    model = Item
    exclude = ('url_path', 'sites')
    extra = 1
    max_num = 1


class ItemAdmin(extradmin.ModelAdmin):

    list_display = ('url_path', 'changefreq', 'enabled')
    string_overrides = {
        'add_title': _(u'Add sitemap.xml item'),
        'change_title': _(u'Change sitemap.xml item'),
        'changelist_title': _(u'Choose sitemap.xml item to change'),
        'changelist_popup_title': _(u'Choose sitemap.xml item'),
        'changelist_addlink_title': _(u'Add sitemap.xml item'),
        'changelist_paginator_description':
            lambda n: ungettext(u'%(count)d sitemap.xml item',
                                u'%(count)d sitemap.xml items', n)
    }


extradmin.site.register(Item, ItemAdmin)
