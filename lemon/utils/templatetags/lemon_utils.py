from django import template


register = template.Library()


@register.filter
def is_active(path, find):
    return any((item and path.startswith(item)) for item in find.split(','))
