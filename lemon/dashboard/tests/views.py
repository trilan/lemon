from django.http import HttpResponse
from django.views.generic import View

from lemon.dashboard.views import AppAdminMixin


class AppAdminView(AppAdminMixin, View):

    def get(self, request, *args, **kwargs):
        app_admin = self.get_app_admin()
        return HttpResponse()
