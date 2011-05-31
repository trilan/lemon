from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils.safestring import mark_safe

from lemon.dashboard.models import WidgetInstance
from lemon.dashboard.utils import find_template_source, Media, MediaDefiningClass


class BaseDashboard(object):

    template_name = 'dashboard/dashboard.html'

    def __init__(self):
        self._registry = {}

    @property
    def media(self):
        media = Media()
        for widget in self._registry.values():
            media = media + widget.media
        return media

    def register(self, label, widget_class):
        self._registry[label] = widget_class(label, self)

    def unregister(self, label):
        if label in self._registry:
            del self._registry[label]

    def get_urls(self, app_admin):
        from lemon.dashboard import views
        wrap = app_admin.admin_site.admin_view
        urlpatterns = patterns('',
            url(r'^widgets$',
                wrap(views.WidgetsView.as_view()),
                name='widget_list'),
            url(r'^widget_instances$',
                wrap(views.WidgetInstanceListView.as_view()),
                name='widget_instance_list'),
            url(r'^widget_instances/(\d+)$',
                wrap(views.WidgetInstanceView.as_view()),
                name='widget_instance'),
        )
        for widget in self._registry.values():
            widget_urls = widget.get_urls(app_admin)
            if not widget_urls:
                continue
            urlpatterns += patterns('',
                url(r'^%s/' % widget.label, include(widget_urls)),
            )
        return urlpatterns

    def render(self, context):
        queryset = WidgetInstance.objects.filter(user=context.get('user'))
        widget_instances = queryset.to_json()
        widgets = json.dumps([w.to_raw() for w in self._registry.values()])
        return render_to_string(self.template_name, {
            'dashboard_widgets_url': reverse(
                'admin:dashboard:widget_list',
                current_app=context.current_app),
            'dashboard_widget_instances_url': reverse(
                'admin:dashboard:widget_instance_list',
                current_app=context.current_app),
            'widget_instances': widget_instances,
            'widgets': widgets,
        })

    def render_all(self, context):
        output = [self.render(context)]
        for widget in self._registry.values():
            content = widget.render(context)
            if content:
                output.append(content)
        return mark_safe(u'\n'.join(output))


class Dashboard(BaseDashboard):

    __metaclass__ = MediaDefiningClass

    class Media:
        templates = ('dashboard/templates.html',)


class Widget(object):

    __metaclass__ = MediaDefiningClass

    title = None
    description = None
    backbone_view_name = 'WidgetInstance'
    template_name = None

    def __init__(self, label, dashboard):
        self.label = label
        self.dashboard = dashboard

    def render(self, context):
        if self.template_name:
            return render_to_string(self.template_name, context)
        return u''

    def get_urls(self, app_admin):
        return None

    def to_raw(self):
        return {
            'id': self.label,
            'title': self.title,
            'viewName': self.backbone_view_name,
            'description': self.description
        }


dashboard = Dashboard()
