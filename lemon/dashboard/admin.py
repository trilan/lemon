from django.conf import settings

from lemon import extradmin as admin
from lemon.dashboard import views
from lemon.dashboard.base import dashboard, Widget


class DashboardAdmin(admin.AppAdmin):

    dashboard = dashboard

    @property
    def urls(self):
        return self.dashboard.get_urls(self), 'dashboard', 'dashboard'


admin.site.register_app('dashboard', DashboardAdmin)
