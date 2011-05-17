from django.conf import settings


CONFIG = {
    'MARKUP_WIDGET': None,
    'EXCLUDE_FROM_PERMISSIONS': (),
}
CONFIG.update(getattr(settings, 'EXTRADMIN_CONFIG', {}))
