import re
from django import template
from django.template.loader import render_to_string
from lemon.filebrowser.utils import get_query_string, string_to_list, string_to_dict


DOT = '.'


register = template.Library()


class QueryStringNode(template.Node):
    
    def __init__(self, remove=None, add=None):
        self.add = string_to_dict(add)
        self.remove = string_to_list(remove)
    
    def render(self, context):
        query = context.get('query')
        if not query:
            return ''
        return get_query_string(query.copy(), self.remove, self.add)


@register.tag
def query_string(parser, token):
    bits = token.split_contents()
    tag_name = bits[0]
    if len(bits) > 1:
        remove = bits[1]
        if not (remove[0] == remove[-1] and remove[0] in ('"', "'")):
            raise template.TemplateSyntaxError(
                u"%r tag's arguments should be in quotes" % tag_name)
        if len(bits) > 2:
            add = bits[2]
            if not (add[0] == add[-1] and add[0] in ('"', "'")):
                raise template.TemplateSyntaxError(
                    u"%r tag's arguments should be in quotes" % tag_name)
            return QueryStringNode(remove[1:-1], add[1:-1])
        return QueryStringNode(remove[1:-1])
    return QueryStringNode()


@register.inclusion_tag('filebrowser/tags/paginator.html', takes_context=True)
def pagination(context):
    page = context['page']
    page_num = page.number - 1
    paginator = page.paginator

    if not paginator.num_pages or paginator.num_pages == 1:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            page_range = []
            if page_num > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(
                    page_num - ON_EACH_SIDE, page_num + 1))
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(range(
                    page_num + 1, page_num + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(
                    paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))
    return {
        'page_range': page_range,
        'page_num': page_num,
        'results_var': context['results_var'],
        'query': context['query'],
    }


class IncludeEditorStuffNode(template.Node):

    def __init__(self, editor):
        self.editor = editor

    def render(self, context):
        editor = self.editor.resolve(context)
        if not isinstance(editor, basestring) or not re.match(r'^\w+$', editor):
            return ''
        template_name = 'filebrowser/editors/%s.html' % editor
        try:
            return render_to_string(template_name, context_instance=context)
        except template.TemplateDoesNotExist:
            return ''


@register.tag
def include_editor_stuff(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(
            '%r tag takes only one argument: the editor identifier.' % bits[0])
    editor = parser.compile_filter(bits[1])
    return IncludeEditorStuffNode(editor)
