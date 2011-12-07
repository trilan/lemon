from django.conf import settings


MEDIA_ROOT = getattr(settings, 'FILEBROWSER_MEDIA_ROOT', settings.MEDIA_ROOT)
MEDIA_URL = getattr(settings, 'FILEBROWSER_MEDIA_URL', settings.MEDIA_URL)
