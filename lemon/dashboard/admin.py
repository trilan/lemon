from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.admin.models import LogEntry
from django.utils import simplejson as json
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from lemon import extradmin as admin
from lemon.dashboard import views
from lemon.dashboard.base import dashboard, Widget


class DashboardAdmin(admin.AppAdmin):

    dashboard = dashboard

    @property
    def urls(self):
        return self.dashboard.get_urls(self), 'dashboard', 'dashboard'


class AdminSite(admin.AdminSite):

    index_template = 'admin/custom_dashboard_index.html'

    def __init__(self, dashboard, name=None, app_name='admin'):
        super(AdminSite, self).__init__(name, app_name)
        self.dashboard = dashboard
        self.register_app('dashboard', DashboardAdmin, dashboard=dashboard)

    def index(self, request, extra_context=None):
        context = {'dashboard': self.dashboard}
        context.update(extra_context or {})
        return super(AdminSite, self).index(request, context)


class AdminLog(Widget):

    title = _(u'Recent Actions')
    description = _(u'Log of your recent actions in admin')
    template_name = 'dashboard/admin_log.html'
    backbone_view_name = u'AdminLog'
    limit = 10

    def get_queryset(self, user):
        return LogEntry.objects.filter(user=user)[:self.limit]

    def get_entry_type(self, entry):
        if entry.is_addition():
            return 'addition'
        if entry.is_change():
            return 'change'
        if entry.is_deletion():
            return 'deletion'

    def get_entry_link(self, entry):
        return None if entry.is_deletion() else entry.get_admin_url()

    def get_entry_model(self, entry):
        model_class = entry.content_type.model_class()
        return unicode(model_class._meta.verbose_name)

    def get_raw(self, user, use_l10n=True):
        queryset = self.get_queryset(user)
        entry_list = []
        for entry in self.get_queryset(user):
            date = entry.action_time.date()
            time = entry.action_time.time()
            entry_list.append({
                'description': entry.object_repr,
                'link': self.get_entry_link(entry),
                'model': self.get_entry_model(entry),
                'date': localize(date, use_l10n=use_l10n),
                'time': localize(time, use_l10n=use_l10n),
                'type': self.get_entry_type(entry),
            })
        return entry_list

    def get_json(self, user):
        return json.dumps(self.get_raw(user))

    def render(self, context):
        context.update({'object_list': self.get_json(context['user'])})
        output = super(AdminLog, self).render(context)
        context.pop()
        return output

    def get_urls(self, app_admin):
        wrap = app_admin.admin_site.admin_view
        return patterns('',
            url(r'^entries$',
                wrap(views.LogEntryListView.as_view(app_admin=app_admin, widget=self)),
                name='admin_log_entry_list'),
        )


admin.site.register_app('dashboard', DashboardAdmin)
dashboard.register('admin_log', AdminLog)
