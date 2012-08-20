from django.conf import settings


CONFIG = {
    'MARKUP_WIDGET': None,
}
CONFIG.update(getattr(settings, 'LEMON_CONFIG', {}))
