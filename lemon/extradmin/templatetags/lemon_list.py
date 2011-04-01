from django.contrib.admin.views.main import PAGE_VAR, ALL_VAR
from django.utils.html import escape
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
