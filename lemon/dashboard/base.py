import sys

from django.conf.urls import patterns, url, handler404, handler500
from django.core.urlresolvers import RegexURLResolver
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST

from lemon.dashboard.models import DashboardState


class _URLConfModule(object):

    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns
        self.handler404 = handler404
        self.handler500 = handler500


class Dashboard(object):

    def __init__(self):
        self._registry = {}

    def register(self, widget_class):
        name = '%s.%s' % (widget_class.app_label, widget_class.__name__.lower())
        widget = widget_class(self)
        self._registry[name] = widget

    def unregister(self, widget_class):
        name = '%s.%s' % (widget_class.app_label, widget_class.__name__.lower())
        if name in self._registry:
            del self._registry[name]

    def get_urls(self, app_admin):
        wrap = app_admin.admin_site.admin_view
        return patterns('',
            url(r'^$',
                wrap(self.available_widgets_view),
                name='available_widgets'),
            url(r'^add$',
                wrap(self.add_widget_view),
                name='add_widget'),
            url(r'^delete$',
                wrap(self.delete_widget_view),
                name='delete_widget'),
            url(r'^store$',
                wrap(self.store_view),
                name='store'),
            url(r'^(\w+)/(\w+)/(.*)$',
                wrap(self.widget_view),
                name='widget'),
        )

    def available_widgets_view(self, request):
        state = DashboardState.objects.get_for_user(request.user)
        data = json.loads(state.data)
        available_widgets = self._registry.copy()
        for column in data['columns']:
            for cell in column:
                if cell['name'] in available_widgets:
                    del available_widgets[cell['name']]
        return render_to_response(
            'dashboard/available_widgets.html',
            {'object_list': available_widgets},
            context_instance=RequestContext(request))

    @method_decorator(require_POST)
    def add_widget_view(self, request):
        name = json.loads(request.raw_post_data)
        if name not in self._registry:
            raise Http404
        state = DashboardState.objects.get_for_user(request.user)
        if not state.has_widget(name):
            state.add_widget(0, name)
        return HttpResponse('[]', mimetype='application/json')

    @method_decorator(require_POST)
    def delete_widget_view(self, request):
        name = json.loads(request.raw_post_data)
        if name not in self._registry:
            raise Http404
        state = DashboardState.objects.get_for_user(request.user)
        state.delete_widget(name)
        return HttpResponse('[]', mimetype='application/json')

    @method_decorator(require_POST)
    def store_view(self, request):
        new_data = json.loads(request.raw_post_data)
        state = DashboardState.objects.get_for_user(request.user)
        data = json.loads(state.data)
        columns = []
        for new_column in new_data['columns']:
            column = []
            for new_widget in new_column:
                if new_widget in self._registry:
                    column.append({'name': new_widget, 'state': {}})
            columns.append(column)
        data['columns'] = columns
        state.data = json.dumps(data)
        state.save()
        return HttpResponse('[]', mimetype='application/json')

    def widget_view(self, request, app_label, widget_name, path):
        name = '%s.%s' % (app_label, widget_name)
        if name not in self._registry:
            raise Http404
        state = DashboardState.objects.get_for_user(request.user)
        data = json.loads(state.data)
        names = []
        for column in data['columns']:
            for row in column:
                names.append(row['name'])
        if name not in names:
            raise Http404
        widget = self._registry[name]
        urls = widget.urls
        if urls is None:
            raise Http404
        resolver = RegexURLResolver(r'^', _URLConfModule(urls))
        callback, args, kwargs = resolver.resolve(path)
        return callback(request, *args, **kwargs)

    def render(self, user, context):
        state = DashboardState.objects.get_for_user(user)
        data = json.loads(state.data)
        new_columns = []
        for column in data['columns']:
            new_column = []
            for row in column:
                widget = self._registry.get(row['name'])
                if widget:
                    row = row.copy()
                    row['id'] = 'widget_%s' % row['name'].replace('.', '_')
                    row['widget'] = widget
                    row['content'] = widget.render(context, row['state'])
                    new_column.append(row)
            new_columns.append(new_column)
        data = {'columns': new_columns}
        return render_to_string('dashboard/dashboard.html', {
            'data': data,
        }, context_instance=context)


class WidgetMetaclass(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(WidgetMetaclass, cls).__new__(cls, name, bases, attrs)
        if 'app_label' not in attrs:
            widget_module = sys.modules[new_class.__module__]
            new_class.app_label = widget_module.__name__.split('.')[-2]
        return new_class


class BaseWidget(object):

    title = None
    description = None
    template = None

    def __init__(self, dashboard):
        self.dashboard = dashboard

    def get_context_data(self, context):
        return {}

    def render(self, context, state):
        if self.template is not None:
            data = self.get_context_data(context)
            data['state'] = state
            data['id'] = 'widget_%s_%s_content' % (
                self.app_label,
                self.__class__.__name__.lower(),
            )
            return render_to_string(self.template, data, context)
        return ''

    def get_urls(self):
        return None

    def _get_urls(self):
        if not hasattr(self, '_urls'):
            urls = self.get_urls()
            if urls and isinstance(urls, (tuple, list)):
                self._urls = patterns('', *urls)
            else:
                self._urls = None
        return self._urls
    urls = property(_get_urls)


class Widget(BaseWidget):

    __metaclass__ = WidgetMetaclass


dashboard = Dashboard()
