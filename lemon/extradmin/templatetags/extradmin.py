from __future__ import absolute_import
from django.template import Library


register = Library()


@register.simple_tag
def permissions_form_field(form, permission_id, group_id):
    return form['value_%s_%s' % (permission_id, group_id)]


@register.filter
def group_column_width(count):
    return int(round(100.0 / (count + 2)))
