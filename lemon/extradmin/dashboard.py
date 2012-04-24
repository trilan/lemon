from django.contrib.admin.models import LogEntry
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.utils.safestring import mark_safe

from lemon import dashboard


class LogWidget(dashboard.Widget):

    title = _(u"Admin log")
    description = _(u"Log of your last fifteen actions in admin.")
    template = 'extradmin/dashboard/log.html'

    def get_log(self, user, limit=15):
        qs = LogEntry.objects.select_related('content_type', 'user')
        return qs.filter(user=user)[:limit]

    def get_context_data(self, request):
        return {'log': self.get_log(request.user)}


class AppsWidget(dashboard.Widget):

    title = _(u"Apps")
    description = _(u"Simple navigation in admin through apps' models.")
    template = 'extradmin/dashboard/apps.html'

    def get_context_data(self, request):
        user = request.user
        admin_site = self.dashboard.admin_site
        app_dict = {}
        for model, model_admin in admin_site._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
                if any(perms.values()):
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'admin_url': mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
                        'perms': perms}
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': _(app_label).capitalize(),
                            'app_url': app_label + '/',
                            'has_module_perms': has_module_perms,
                            'models': [model_dict]}
        app_list = app_dict.values()
        app_list.sort(key=lambda x: x['name'])
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return {'app_list': app_list}
