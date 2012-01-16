from django.template import Library
from lemon.extradmin.menu import Menu


register = Library()


@register.inclusion_tag('extradmin/main_menu.html', takes_context=True)
def main_menu(context, menu_name):
    return {'menu': Menu.with_name(menu_name),
            'user': context.get('user'),
            'request': context.get('request')}


@register.simple_tag(takes_context=True)
def main_menu_item_url(context, menu_item):
    return menu_item.get_url(context.get('user'), context.get('request')) or ''
