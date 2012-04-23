from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin import sites
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from lemon.extradmin import widgets, ModelAdmin
from lemon.extradmin import settings
from lemon.dashboard import Dashboard
from lemon.filebrowser.sites import FileBrowserSite


class AdminSite(sites.AdminSite):

    def __init__(self, name='admin', app_name='admin'):
        super(AdminSite, self).__init__(name, app_name)
        self.file_browser_site = FileBrowserSite(self)
        self.dashboard = Dashboard(self)

    def register(self, model_or_iterable, admin_class=None, **options):
        if not admin_class:
            admin_class = ModelAdmin
        super(AdminSite, self).register(
            model_or_iterable, admin_class, **options)

    def get_urls(self):
        urls = super(AdminSite, self).get_urls()
        return patterns('',
            url(r'^filebrowser/', include(self.file_browser_site.urls)),
            url(r'^dashboard/', include(self.dashboard.urls)),
        ) + urls

    @never_cache
    def index(self, request, extra_context=None):
        context = {
            'dashboard': self.dashboard.render(request),
            'title': _(u"Site administration"),
        }
        context.update(extra_context or {})
        return render_to_response(
            self.index_template or 'admin/index.html', context,
            context_instance=RequestContext(request, current_app=self.name))

    @property
    def markup_widget(self):
        if hasattr(self, '_markup_widget'):
            return self._markup_widget
        markup_widget = settings.CONFIG['MARKUP_WIDGET']
        if markup_widget is None:
            self._markup_widget = markup_widget
        elif markup_widget and isinstance(markup_widget, basestring):
            module_name, attr_name = markup_widget.rsplit('.', 1)
            try:
                module = import_module(module_name)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing widget %s: %s'
                                           % (markup_widget, e))
            try:
                self._markup_widget = getattr(module, attr_name)
            except AttributeError, e:
                raise ImproperlyConfigured('Error importing widget %s: %s'
                                           % (markup_widget, e))
        else:
            ImproperlyConfigured('MARKUP_WIDGET should be a string with path to '
                                 'the form widget')
        return self._markup_widget


site = AdminSite()
