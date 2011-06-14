from lemon.dashboard import Dashboard
from lemon.dashboard.admin import DashboardAdmin, AdminSite, AdminLog

from .dashboard import FirstHelpWidget, SecondHelpWidget, ThirdHelpWidget


first_dashboard = Dashboard('first_dashboard')
first_dashboard.register('first_help_widget', FirstHelpWidget)
first_dashboard.register('second_help_widget', SecondHelpWidget)
first_dashboard.register('third_help_widget', ThirdHelpWidget)

second_dashboard = Dashboard('second_dashboard')
second_dashboard.register('third_help_widget', ThirdHelpWidget)

third_dashboard = Dashboard('third_dashboard')
third_dashboard.register('admin_log', AdminLog)

first_admin_site = AdminSite(first_dashboard, 'first_admin')
second_admin_site = AdminSite(second_dashboard, 'second_admin')
third_admin_site = AdminSite(third_dashboard, 'third_dashboard')
