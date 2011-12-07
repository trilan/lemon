from django.template import Library
from django.utils.safestring import mark_safe
from django.utils import simplejson as json

from lemon.dashboard import dashboard as default_instance


register = Library()


def dashboard_media(type, instance=None):
    instance = instance or default_instance
    media = getattr(instance.media, 'render_%s' % type)()
    if media:
        return mark_safe(u'\n'.join(media))
    return u''


@register.simple_tag
def dashboard_css(instance=None):
    return dashboard_media('css', instance)


@register.simple_tag
def dashboard_js(instance=None):
    return dashboard_media('js', instance)


@register.simple_tag(takes_context=True)
def dashboard(context, instance=None):
    return (instance or default_instance).render_all(context)


@register.inclusion_tag('dashboard/tags/admin_app_list.html')
def admin_app_list(app_list):
    return {'app_list': json.dumps(app_list, default=lambda x: unicode(x))}
