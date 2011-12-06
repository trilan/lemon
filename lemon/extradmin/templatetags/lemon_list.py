from django.contrib.admin.templatetags.admin_list import (
    result_hidden_fields, result_headers, results)
from django.contrib.admin.views.main import PAGE_VAR, ALL_VAR
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.template import Library


register = Library()


@register.simple_tag
def lemon_paginator_href(cl, i):
    return escape(cl.get_query_string({PAGE_VAR: i-1}))


@register.simple_tag(takes_context=True)
def lemon_paginator_description(context):
    cl = context.get('cl')
    description = context.get('changelist_paginator_description')
    if not cl and not description:
        return ''
    return description(cl.result_count) % {'count': cl.result_count}


@register.filter
def pagination_required(cl):
    return (not cl.show_all or not cl.can_show_all) and cl.multi_page


@register.filter
def show_all_url(cl):
    return cl.can_show_all and not cl.show_all and cl.multi_page and \
        cl.get_query_string({ALL_VAR: ''})


def extradmin_result_headers(cl):
    """Ugly patch for ugly result_headers function"""
    for item in result_headers(cl):
        if not item.get('sortable'):
            yield item
            continue
        if item.get('class_attrib'):
            class_attrib = item['class_attrib']
            class_attrib = class_attrib.replace('class="', 'class="sortable ')
        else:
            class_attrib = ' class="sortable"'
        item['class_attrib'] = mark_safe(class_attrib)
        yield item


@register.inclusion_tag('admin/change_list_results.html')
def result_list(cl):
    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': list(extradmin_result_headers(cl)),
            'results': list(results(cl))}
