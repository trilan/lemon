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


extradmin.site.register(Page, PageAdmin)
