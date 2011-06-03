from django import http
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.generic import View

from lemon.dashboard.models import WidgetInstance


class AppAdminMixin(object):

    app_admin = None

    def get_app_admin(self):
        if self.app_admin is None:
            raise ImproperlyConfigured(
                "DashboardMixin requires either a definition of "
                "'app_admin' or an implementation of 'get_app_admin'")
        return self.app_admin


class WidgetsView(AppAdminMixin, View):

    def get(self, request, *args, **kwargs):
        widgets = self.get_app_admin().dashboard._registry.values()
        content = json.dumps([w.to_raw() for w in widgets])
        return http.HttpResponse(content, content_type='application/json')


class WidgetInstanceListView(AppAdminMixin, View):

    def get(self, request, *args, **kwargs):
        content = WidgetInstance.objects.filter(user=request.user).to_json()
        return http.HttpResponse(content, content_type='application/json')

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.raw_post_data)
        except ValueError:
            return http.HttpResponseBadRequest()
        data['user'] = request.user
        try:
            widget_instance = WidgetInstance.objects.create(**data)
        except IntegrityError:
            return http.HttpResponseBadRequest()
        WidgetInstance.objects.adjust(widget_instance.user,
                                      widget_instance.dashboard,
                                      widget_instance)
        return http.HttpResponse(status=201, content_type='application/json')


class WidgetInstanceView(AppAdminMixin, View):

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.raw_post_data)
        except ValueError:
            return http.HttpResponseBadRequest()
        queryset = WidgetInstance.objects.filter(user=request.user)
        widget_instance = get_object_or_404(queryset, pk=args[0])
        widget_instance.update_from(data)
        return http.HttpResponse(status=204, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        queryset = WidgetInstance.objects.filter(user=request.user)
        widget_instance = get_object_or_404(queryset, pk=args[0])
        widget_instance.delete()
        return http.HttpResponse(status=204, content_type='application/json')
