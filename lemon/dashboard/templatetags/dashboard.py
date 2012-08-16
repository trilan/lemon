from django.template import Library
from django.utils import simplejson as json
from django.utils.safestring import mark_safe

from ..base import dashboard as default_instance


register = Library()


@register.simple_tag(takes_context=True)
def dashboard(context, instance=None):
    user = context.get('user')
    return mark_safe((instance or default_instance).render(user, context))


@register.inclusion_tag('dashboard/tags/admin_app_list.html')
def admin_app_list(app_list):
    return {'app_list': json.dumps(app_list, default=lambda x: unicode(x))}
