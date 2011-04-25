# -*- coding: UTF-8 -*-

from django.conf import settings


CONFIG = {
    'TITLE_SEPARATOR': u' — ',
    'TITLE_REVERSED': False,
}
CONFIG.update(getattr(settings, 'METATAGS_CONFIG', {}))
TITLE_SEPARATOR = getattr(settings, 'METATAGS_TITLE_SEPARATOR', u' — ')
TITLE_REVERSED = getattr(settings, 'METATAGS_TITLE_REVERSED', False)
