from django.conf import settings


CONFIG = {
    'STATE': ((), ()),
}
CONFIG.update(getattr(settings, 'DASHBOARD_CONFIG', {}))
