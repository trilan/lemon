from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from lemon.pages import fields as pages_fields
from lemon.publications.models import Publication


class URLPathField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 255)
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True
        super(URLPathField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'SlugField'

    def formfield(self, **kwargs):
        defaults = {'form_class': pages_fields.URLPathField}
        defaults.update(kwargs)
        return super(URLPathField, self).formfield(**defaults)


class Page(Publication):

    slug = URLPathField(_(u'URL'), max_length=255)
    site = models.ForeignKey(Site, verbose_name=_(u'site'))
    title = models.CharField(_(u'title'), max_length=255)
    content = models.TextField(_(u'content'))
    template = models.CharField(_(u'template'), max_length=255)

    class Meta:
        ordering = ['slug']
        verbose_name = _(u'text page')
        verbose_name_plural = _(u'text pages')
        unique_together = ('slug', 'site')

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.slug)

    def get_absolute_url(self):
        return self.slug


from django.conf import settings
if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [(
            (URLPathField,), [],
            {'max_length': ['max_length', {'default': 255}],
             'db_index': ['db_index', {'default': True}]})],
        ['^lemon\.pages\.models\.URLPathField'])
