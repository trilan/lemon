from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin import sites
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from lemon.extradmin import widgets, ModelAdmin
from lemon.dashboard import Dashboard
from lemon.filebrowser.sites import FileBrowserSite


class AdminSite(sites.AdminSite):

    def __init__(self, name=None, app_name='admin'):
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
        return patterns(
            '',
            url(r'^filebrowser/', include(self.file_browser_site.urls)),
            url(r'^dashboard/', include(self.dashboard.urls)),
        ) + urls

    @never_cache
    def index(self, request, extra_context=None):
        context = {
            'dashboard': self.dashboard.render(request),
            'root_path': self.root_path,
            'title': _(u"Site administration"),
        }
        context.update(extra_context or {})
        return render_to_response(
            self.index_template or 'admin/index.html', context,
            context_instance=RequestContext(request, current_app=self.name))


site = AdminSite()
