from django.utils.importlib import import_module

from lemon.metatags.sites import MetatagsSite, site


LOADING = False


def autodiscover():
    global LOADING

    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('metatags', app_path)
        except ImportError:
            continue

        import_module("%s.metatags" % app)

    LOADING = False
