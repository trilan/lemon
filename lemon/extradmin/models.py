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


_(u'Can add menu section')
_(u'Can change menu section')
_(u'Can delete menu section')

_(u'Can add menu item')
_(u'Can change menu item')
_(u'Can delete menu item')

_(u'Can add group')
_(u'Can change group')
_(u'Can delete group')

_(u'Can add user')
_(u'Can change user')
_(u'Can delete user')

_(u'Can add site')
_(u'Can change site')
_(u'Can delete site')
