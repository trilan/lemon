from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _

from lemon.metatags.managers import PageManager


LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)


class Page(models.Model):

    url_path = models.CharField(_('URL path'), max_length=255, db_index=True)
    title = models.CharField(
        _(u'page title'), max_length=255, blank=True,
        help_text=_(u'Displayed in browser window title.'))
    title_extend = models.BooleanField(
        _(u'extend page title with site name'), default=True,
        help_text=_(u'For example, <strong>Page title - Site name</strong>'))
    keywords = models.TextField(
        _(u'page keywords'), blank=True,
        help_text=_(u'Keywords are terms describing web page content and '
                    u'used by search engines. Here you can enumerate some '
                    u'words divided by commas.'))
    description = models.TextField(
        _(u'page description'), blank=True,
        help_text=_(u'Here you can set short description of this page for '
                    u'search engines.'))
    enabled = models.BooleanField(
        _(u'enabled'), default=False,
        help_text=_(u'If not set, meta tags will not be used on page.'))
    language = models.CharField(
        _(u'language'), max_length=10, db_index=True,
        choices=LANGUAGES, default=get_language)
    sites = models.ManyToManyField(
        Site, null=True, blank=True, related_name='+', verbose_name=_(u'sites'))
    content_type = models.ForeignKey(ContentType, null=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = PageManager()

    class Meta:
        verbose_name = _(u'page')
        verbose_name_plural = _(u'pages')

    def __unicode__(self):
        return self.url_path

    def save(self, *args, **kwargs):
        self.update_url_path(commit=False)
        self.update_language(commit=False)
        super(Page, self).save(*args, **kwargs)
        self.update_sites()

    def update_url_path(self, commit=True):
        obj = self.content_object
        if obj:
            from lemon.metatags import site
            model_metatags = site._registry.get(obj.__class__)
            url_path = model_metatags.url_path(obj)
            if url_path:
                self.url_path = url_path
                if commit:
                    super(Page, self).save(False, False)

    def update_language(self, commit=True):
        obj = self.content_object
        if obj:
            from lemon.metatags import site
            model_metatags = site._registry.get(obj.__class__)
            language = model_metatags.language(obj)
            if language:
                self.language = language
                if commit:
                    super(Page, self).save(False, False)

    def update_sites(self):
        obj = self.content_object
        if obj:
            from lemon.metatags.sites import site
            model_metatags = site._registry.get(obj.__class__)
            sites = model_metatags.sites(obj)
            self.sites.clear()
            if sites:
                self.sites.add(*sites)


_(u'Can add page')
_(u'Can change page')
_(u'Can delete page')
