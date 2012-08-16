from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.admin import sites
from django.contrib.contenttypes import views as contenttype_views
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.functional import update_wrapper
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from lemon.extradmin import ModelAdmin
from lemon.extradmin.settings import CONFIG
from lemon.extradmin.options import AppAdmin
from lemon.dashboard import Dashboard


class AdminSite(sites.AdminSite):

    def __init__(self, name='admin', app_name='admin'):
        super(AdminSite, self).__init__(name, app_name)
        self._app_registry = {}
        self.dashboard = Dashboard(self)

    def register(self, model_or_iterable, admin_class=None, **options):
        if not admin_class:
            admin_class = ModelAdmin
        super(AdminSite, self).register(
            model_or_iterable, admin_class, **options)

    def register_app(self, app_name, admin_class=None, **options):
        if admin_class is None:
            admin_class = AppAdmin
        if app_name in self._app_registry:
            raise sites.AlreadyRegistered(
                'The app %s is already registered' % app_name
            )
        if options:
            options['__module__'] = __name__
            admin_class = type('%sAdmin' % app_name, (admin_class,), options)
        self._app_registry[app_name] = admin_class(app_name, self)

    def unregister_app(self, app_name, admin_class=None):
        if app_name not in self._app_registry:
            raise sites.NotRegistered(
                'The app %s is not registered' % app_name
            )
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
            url(r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
                wrap(contenttype_views.shortcut),
                name='view_on_site'),
        )
        urlpatterns += patterns('',
            url(r'^dashboard/', include(self.dashboard.urls)),
        )

        for app_name, app_admin in self._app_registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/' % app_name, include(app_admin.urls)),
            )
        urlpatterns += patterns('',
            url(r'^(?P<app_label>\w+)/$',
                wrap(self.app_index),
                name='app_list'),
        )

        for model, model_admin in self._registry.iteritems():
            urlpatterns += patterns('',
                url(r'^%s/%s/' % (
                        model._meta.app_label,
                        model._meta.module_name
                    ),
                    include(model_admin.urls)),
            )

        return urlpatterns

    def index(self, request, extra_context=None):
        context = {'dashboard': self.dashboard.render(request)}
        context.update(extra_context or {})
        return super(AdminSite, self).index(request, context)

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
            raise ImproperlyConfigured(
                'MARKUP_WIDGET should be a string with path to the form widget'
            )
        return self._markup_widget

    def get_markup_widget(self, request):
        return self.markup_widget


site = AdminSite()
