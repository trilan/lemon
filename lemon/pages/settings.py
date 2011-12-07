from django.conf import settings


TEMPLATE_DIRS = getattr(settings, 'PAGES_TEMPLATE_DIRS', settings.TEMPLATE_DIRS)
TEMPLATE_EXTENSIONS = getattr(settings, 'PAGES_TEMPLATE_EXTENSIONS', ['.html', '.txt'])
