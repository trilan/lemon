from django import http
from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.generic import View

from lemon.dashboard import dashboard
from lemon.dashboard.models import WidgetInstance


class WidgetsView(View):

    def get(self, request, *args, **kwargs):
        widgets = dashboard._registry.values()
        content = json.dumps([w.to_raw() for w in widgets])
        return http.HttpResponse(content, content_type='application/json')


class WidgetInstanceListView(View):

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
        return http.HttpResponse()


class WidgetInstanceView(View):

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.raw_post_data)
        except ValueError:
            return http.HttpResponseBadRequest()
        queryset = WidgetInstance.objects.filter(user=request.user)
        widget_instance = get_object_or_404(queryset, pk=args[0])
        widget_instance.update_from(data)
        return http.HttpResponse()

    def delete(self, request, *args, **kwargs):
        queryset = WidgetInstance.objects.filter(user=request.user)
        widget_instance = get_object_or_404(queryset, pk=args[0])
        widget_instance.delete()
        return http.HttpResponse()
