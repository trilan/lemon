from django.conf import settings

from lemon import extradmin as admin
from lemon.dashboard import views
from lemon.dashboard.base import dashboard, Widget


class DashboardAdmin(admin.AppAdmin):

    dashboard = dashboard

    @property
    def urls(self):
        return self.dashboard.get_urls(self), 'dashboard', 'dashboard'


class AdminSite(admin.AdminSite):

    index_template = 'admin/custom_dashboard_index.html'

    def __init__(self, dashboard, name=None, app_name='admin'):
        super(AdminSite, self).__init__(name, app_name)
        self.dashboard = dashboard
        self.register_app('dashboard', DashboardAdmin, dashboard=dashboard)

    def index(self, request, extra_context=None):
        context = {'dashboard': self.dashboard}
        context.update(extra_context or {})
        return super(AdminSite, self).index(request, context)


admin.site.register_app('dashboard', DashboardAdmin)
