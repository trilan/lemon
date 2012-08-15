from django.contrib.contenttypes import generic
from lemon.extradmin.options import BaseModelAdmin, InlineModelAdmin


class GenericInlineModelAdmin(generic.GenericInlineModelAdmin,
                              InlineModelAdmin,
                              BaseModelAdmin):
    pass


class GenericStackedInline(GenericInlineModelAdmin):

    template = 'admin/edit_inline/stacked.html'


class GenericTabularInline(GenericInlineModelAdmin):

    template = 'admin/edit_inline/tabular.html'
