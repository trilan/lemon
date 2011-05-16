from __future__ import absolute_import
from django.template import Library
from django.utils.translation import ugettext as _


register = Library()


@register.simple_tag
def permission_name(permission):
    opts = permission.content_type.model_class()._meta
    if permission.codename == opts.get_add_permission():
        return _(u'can add')
    if permission.codename == opts.get_change_permission():
        return _(u'can change')
    if permission.codename == opts.get_delete_permission():
        return _(u'can delete')
    return _(permission.name).lower()


@register.simple_tag
def permissions_form_field(form, permission_id, group_id):
    return form['value_%s_%s' % (permission_id, group_id)]


@register.filter
def group_column_width(count):
    return int(round(100.0 / (count + 2)))
