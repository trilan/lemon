from django import forms

from lemon import extradmin
from lemon.extradmin import generic
from lemon.sitemaps.models import Item


class ItemForm(forms.ModelForm):

    def has_changed(self):
        return True


class ItemInline(generic.GenericStackedInline):

    form = ItemForm
    model = Item
    exclude = ('url_path', 'language', 'sites')
    extra = 1
    max_num = 1


class ItemAdmin(extradmin.ModelAdmin):

    list_display = ('url_path', 'changefreq', 'language', 'enabled')


extradmin.site.register(Item, ItemAdmin)
