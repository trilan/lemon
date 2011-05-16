from django.conf import settings
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import get_language, ugettext_lazy as _

from lemon.publications.models import Publication


LANGUAGES = tuple((code, _(name)) for code, name in settings.LANGUAGES)


class Page(Publication):

    sites = models.ManyToManyField(Site, verbose_name=_(u'sites'))
    language = models.CharField(_(u'language'), max_length=10, db_index=True,
                                choices=LANGUAGES, default=get_language)
    url_path = models.SlugField(_(u'URL path'), max_length=255)
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'))
    template = models.CharField(_(u'template'), max_length=255)

    class Meta:
        ordering = ['url_path']
        verbose_name = _(u'text page')
        verbose_name_plural = _(u'text pages')

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.url_path)

    def get_absolute_url(self):
        return self.url_path


_(u'Can add text page')
_(u'Can change text page')
_(u'Can delete text page')
