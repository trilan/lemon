from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import Library, Variable, Node
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template.defaulttags import URLNode

from ..models import MenuItem
from ..settings import CONFIG


register = Library()


class MainMenuItemURLNode(Node):

    def __init__(self, content_type):
        self.content_type = Variable(content_type)

    def render(self, context):
        try:
            content_type = self.content_type.resolve(context)
        except VariableDoesNotExist:
            return ''
        opts = content_type.model_class()._meta
        app_label = opts.app_label
        module_name = opts.module_name
        view_name = 'admin:%s_%s_changelist' % \
            (app_label, module_name)
        try:
            return reverse(view_name)
        except NoReverseMatch:
            return ''


@register.inclusion_tag('lemon/main_menu.html')
def main_menu():
    queryset = MenuItem.objects.select_related('section', 'content_type')
    queryset = queryset.order_by('section__position', 'position')
    return {'menu_items': queryset, 'menu_links': CONFIG['MENU_LINKS']}


@register.tag
def main_menu_item_url(parser, token):
    try:
        tag_name, content_type = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            '%r tag requires a single argument' % token.contents.split()[0]
        )
    return MainMenuItemURLNode(content_type)
