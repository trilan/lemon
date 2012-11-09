from django.conf import settings


CONFIG = {
    'MARKUP_WIDGET': None,
    'MENU_LINKS': (),
}
CONFIG.update(getattr(settings, 'LEMON_CONFIG', {}))
