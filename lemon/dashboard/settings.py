from django.conf import settings


DASHBOARD = {
    'STATE': (('dashboard.helpwidget',), ()),
}
DASHBOARD.update(getattr(settings, 'DASHBOARD', {}))
