from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin import sites
from django.contrib.contenttypes.views import shortcut
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import update_wrapper
from django.utils.importlib import import_module

from lemon.extradmin.menu import Menu
from lemon.extradmin.options import ModelAdmin, AppAdmin
from lemon.extradmin.settings import CONFIG


class AdminSite(sites.AdminSite):

    def __init__(self, name=None, app_name='admin', menu_name=None):
        super(AdminSite, self).__init__(name, app_name)
        self.menu = Menu(menu_name or name or app_name)
        self._app_registry = {}

    def register(self, model_or_iterable, admin_class=None, **options):
        if not admin_class:
            admin_class = ModelAdmin
        super(AdminSite, self).register(model_or_iterable, admin_class, **options)

    def register_app(self, app_name, admin_class=None, **options):
        if not admin_class:
            admin_class = AppAdmin
        if app_name in self._app_registry:
            raise sites.AlreadyRegistered('The app %s is already registered' % app_name)
        if options:
            options['__module__'] = __name__
            admin_class = type('%sAdmin' % app_name, (admin_class,), options)
        self._app_registry[app_name] = admin_class(app_name, self)

    def unregister_app(self, app_name, admin_class=None):
        if app_name not in self._app_registry:
            raise sites.NotRegistered('The app %s is not registered' % app_name)
        del self._app_registry[app_name]

    def get_urls(self):
        if settings.DEBUG:
            self.check_dependencies()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.index),
                name='index'),
            url(r'^logout/$',
                wrap(self.logout),
                name='logout'),
            url(r'^password_change/$',
                wrap(self.password_change, cacheable=True),
                name='password_change'),
            url(r'^password_change/done/$',
                wrap(self.password_change_done, cacheable=True),
                name='password_change_done'),
            url(r'^jsi18n/$',
                wrap(self.i18n_javascript, cacheable=True),
                name='jsi18n'),
            url(r'r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
                wrap(shortcut)),
        )

        for app_name, app_admin in self._app_registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/' % app_name, include(app_admin.urls)),
            )
        for model, model_admin in self._registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/%s/' % (model._meta.app_label, model._meta.module_name),
                    include(model_admin.urls)),
            )
        return urlpatterns

    @property
    def markup_widget(self):
        if hasattr(self, '_markup_widget'):
            return self._markup_widget
        markup_widget = CONFIG['MARKUP_WIDGET']
        if markup_widget is None:
            self._markup_widget = markup_widget
        elif markup_widget and isinstance(markup_widget, basestring):
            module_name, attr_name = markup_widget.rsplit('.', 1)
            try:
                module = import_module(module_name)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing widget %s: %s'
                                           % (markup_widget, e))
            try:
                self._markup_widget = getattr(module, attr_name)
            except AttributeError, e:
                raise ImproperlyConfigured('Error importing widget %s: %s'
                                           % (markup_widget, e))
        else:
            ImproperlyConfigured('MARKUP_WIDGET should be a string with path to '
                                 'the form widget')
        return self._markup_widget


site = AdminSite()
