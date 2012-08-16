from django.template import Library
from django.utils import simplejson as json


register = Library()


@register.inclusion_tag('dashboard/tags/admin_app_list.html')
def admin_app_list(app_list):
    return {'app_list': json.dumps(app_list, default=lambda x: unicode(x))}
