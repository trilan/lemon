from lemon.dashboard import Dashboard
from lemon.dashboard.admin import DashboardAdmin, AdminSite

from .dashboard import FirstHelpWidget, SecondHelpWidget, ThirdHelpWidget


first_dashboard = Dashboard('first_dashboard')
first_dashboard.register('first_help_widget', FirstHelpWidget)
first_dashboard.register('second_help_widget', SecondHelpWidget)
first_dashboard.register('third_help_widget', ThirdHelpWidget)

second_dashboard = Dashboard('second_dashboard')
second_dashboard.register('third_help_widget', ThirdHelpWidget)

first_admin_site = AdminSite(first_dashboard, 'first_admin')
second_admin_site = AdminSite(second_dashboard, 'second_admin')
