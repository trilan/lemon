from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _

from lemon.sitemaps.managers import ItemManager


LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)

CHANGEFREQ_CHOCES = (
    ('N', _(u'never')),
    ('A', _(u'always')),
    ('H', _(u'hourly')),
    ('D', _(u'daily')),
    ('W', _(u'weekly')),
    ('M', _(u'monthly')),
    ('Y', _(u'yearly')),
)


class Item(models.Model):

    url_path = models.CharField(_(u'URL path'), max_length=255, db_index=True)
    priority = models.FloatField(
        _(u'page priority'), blank=True, null=True, default=0.5,
        help_text=_(u'The priority of this URL relative to other URLs on '
                    u'your site. Valid values range from 0.0 to 1.0. This '
                    u'value does not affect how your pages are compared to '
                    u'pages on other sites - it only lets the search engines '
                    u'know which pages you deem most important for the '
                    u'crawlers.<br /> More info you can read in '
                    u'<a href="http://www.sitemaps.org/protocol.php" '
                    u'target="_blank">Sitemap protocol description</a>.'))
    changefreq = models.CharField(
        _(u'page change frequency'), max_length=1,
        choices=CHANGEFREQ_CHOCES, default='M',
        help_text=_(u'How frequently the page is likely to change. This '
                    u'value provides general information to search engines '
                    u'and may not correlate exactly to how often they crawl '
                    u'the page.<br /> The value <strong>always</strong> '
                    u'should be used to describe documents that change each '
                    u'time they are accessed. The value '
                    u'<strong>never</strong> should be used to describe '
                    u'archived URLs.<br /> More info you can read in '
                    u'<a href="http://www.sitemaps.org/protocol.php" '
                    u'target="_blank">Sitemap protocol description</a>.'))
    lastmod = models.DateTimeField(
        _(u'last modification date'), blank=True, null=True,
        default=datetime.now)
    enabled = models.BooleanField(
        _(u'enabled'), default=True,
        help_text=_(u'If disabled, this item will not shown in sitemap.xml.'))
    language = models.CharField(
        _(u'language'), max_length=10, db_index=True,
        choices=LANGUAGES, default=get_language)
    sites = models.ManyToManyField(
        Site, null=True, blank=True, verbose_name=_(u'sites'))
    content_type = models.ForeignKey(ContentType, null=True, editable=False)
    object_id = models.PositiveIntegerField(null=True, editable=False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = ItemManager()

    class Meta:
        verbose_name = _(u'sitemap.xml item')
        verbose_name_plural = _(u'sitemap.xml items')

    def __unicode__(self):
        return self.url_path

    def save(self, *args, **kwargs):
        self.update_url_path(commit=False)
        self.update_language(commit=False)
        super(Item, self).save(*args, **kwargs)
        self.update_sites()

    def update_url_path(self, commit=True):
        obj = self.content_object
        if obj:
            from lemon.sitemaps import site
            model_sitemap = site._registry.get(obj.__class__)
            url_path = model_sitemap.url_path(obj)
            if url_path:
                self.url_path = url_path
                if commit:
                    super(Item, self).save(False, False)

    def update_language(self, commit=True):
        obj = self.content_object
        if obj:
            from lemon.sitemaps import site
            model_sitemap = site._registry.get(obj.__class__)
            language = model_sitemap.language(obj)
            if language:
                self.language = language
                if commit:
                    super(Item, self).save(False, False)

    def update_sites(self):
        obj = self.content_object
        if obj:
            from lemon.sitemaps import site
            model_sitemap = site._registry.get(obj.__class__)
            sites = model_sitemap.sites(obj)
            self.sites.clear()
            if sites:
                self.sites.add(*sites)


_(u'Can add sitemap.xml item')
_(u'Can change sitemap.xml item')
_(u'Can delete sitemap.xml item')
