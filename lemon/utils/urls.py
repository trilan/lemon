from django.utils.importlib import import_module


URLS_LOADING = False


def autodiscover(only=None, exclude=None):
    global URLS_LOADING

    if URLS_LOADING:
        return
    URLS_LOADING = True

    import imp
    from django.conf import settings

    if only:
        apps = only
    elif exclude:
        apps = list(set(settings.INSTALLED_APPS) - set(exclude))
    else:
        apps = settings.INSTALLED_APPS

    urls = []
    for app in apps:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('urls', app_path)
        except ImportError:
            continue

        urls_module = import_module('%s.urls' % app)
        urls.extend(getattr(urls_module, 'urls', []))

    URLS_LOADING = False
    return urls
