from django.contrib.admin.models import LogEntry
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

    def get_context_data(self, context):
        return {'log': self.get_log(context['user'])}


class AppsWidget(dashboard.Widget):

    title = _(u"Apps")
    description = _(u"Simple navigation in admin through apps' models.")
    template = 'extradmin/dashboard/apps.html'
