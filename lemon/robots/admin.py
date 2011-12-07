from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from lemon import extradmin
from lemon.robots.models import File


class FileAdmin(extradmin.ModelAdmin):

    ordering = ['site__domain']
    list_display = ['file_name', 'site_name']

    def file_name(self, obj):
        return unicode(obj)
    file_name.short_description = _(u'file')
    file_name.admin_order_field = 'site__domain'

    def site_name(self, obj):
        url = reverse('admin:sites_site_change', args=(obj.site.pk,))
        name = u'%s (%s)' % (obj.site.name, obj.site.domain)
        return u'<a href="%s">%s</a>' % (url, name)
    site_name.short_description = _(u'site')
    site_name.allow_tags = True
    site_name.admin_order_field = 'site'


extradmin.site.register(File, FileAdmin)
