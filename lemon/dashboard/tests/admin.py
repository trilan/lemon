from lemon.dashboard import Dashboard
from lemon.dashboard.admin import DashboardAdmin
from lemon.extradmin import AdminSite

from .dashboard import FirstHelpWidget, SecondHelpWidget, ThirdHelpWidget


first_dashboard = Dashboard('first_dashboard')
first_dashboard.register('first_help_widget', FirstHelpWidget)
first_dashboard.register('second_help_widget', SecondHelpWidget)
first_dashboard.register('third_help_widget', ThirdHelpWidget)


class FirstDashboardAdmin(DashboardAdmin):

    dashboard = first_dashboard


first_admin_site = AdminSite('first_admin')
first_admin_site.register_app('dashboard', FirstDashboardAdmin)


second_dashboard = Dashboard('second_dashboard')
second_dashboard.register('third_help_widget', ThirdHelpWidget)


class SecondDashboardAdmin(DashboardAdmin):

    dashboard = second_dashboard


second_admin_site = AdminSite('second_admin')
second_admin_site.register_app('dashboard', SecondDashboardAdmin)
