from django.template import Library, Node, TemplateSyntaxError
from django.utils.safestring import mark_safe

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


@register.simple_tag
def dashboard_templates(instance=None):
    return dashboard_media('templates', instance)


@register.simple_tag(takes_context=True)
def dashboard(context, instance=None):
    return (instance or default_instance).render_all(context)
