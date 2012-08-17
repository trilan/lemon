from django.template import Library, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist
from django.template.defaulttags import URLNode

from ..models import MenuItem


register = Library()


class MainMenuItemURLNode(URLNode):

    def __init__(self, content_type):
        self.content_type = Variable(content_type)
        self.args = ()
        self.kwargs = {}
        self.asvar = False
        self.legacy_view_name = True

    def render(self, context):
        try:
            content_type = self.content_type.resolve(context)
            opts = content_type.model_class()._meta
            app_label = opts.app_label
            module_name = opts.module_name
            self.view_name = 'admin:%s_%s_changelist' % \
                (app_label, module_name)
        except VariableDoesNotExist:
            return ''
        return super(MainMenuItemURLNode, self).render(context)


@register.inclusion_tag('lemon/main_menu.html')
def main_menu():
    queryset = MenuItem.objects.select_related('section', 'content_type')
    queryset = queryset.order_by('section__position', 'position')
    return {'menu_items': queryset}


@register.tag
def main_menu_item_url(parser, token):
    try:
        tag_name, content_type = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            '%r tag requiresa single argument' % token.contents.split()[0]
        )
    return MainMenuItemURLNode(content_type)
