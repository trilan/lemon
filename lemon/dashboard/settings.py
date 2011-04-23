from django.conf import settings


CONFIG = {
    'STATE': (('dashboard.helpwidget',), ()),
}
CONFIG.update(getattr(settings, 'DASHBOARD_CONFIG', {}))
