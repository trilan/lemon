from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MenuSection(models.Model):

    name = models.CharField(_('section name'), max_length=50)
    position = models.PositiveIntegerField(_('position'), default=0)

    class Meta:
        ordering = ['position']
        verbose_name = _('menu section')
        verbose_name_plural = _('menu sections')

    def __unicode__(self):
        return self.name


class MenuItem(models.Model):

    name = models.CharField(_('item name'), max_length=50)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'))
    section = models.ForeignKey(MenuSection, related_name='sections',
                                verbose_name=_('section'))
    position = models.PositiveIntegerField(_('position'), default=0)

    class Meta:
        ordering = ['position']
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

    def __unicode__(self):
        return self.name
