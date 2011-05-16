from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import ugettext_lazy as _


class File(models.Model):

    site = models.OneToOneField(Site, verbose_name=_(u'site'))
    content = models.TextField(_(u'file content'))

    objects = models.Manager()

    class Meta:
        verbose_name = _(u'robots.txt file')
        verbose_name_plural = _(u'robots.txt files')

    def __unicode__(self):
        return u'/'.join([self.site.domain, u'robots.txt'])
