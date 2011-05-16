from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class AdminDateWidget(widgets.AdminDateWidget):

    class Media:
        extend = ()
        js = (settings.STATIC_URL + 'extradmin/js/jquery.datetimepicker.js',)


class AdminTimeWidget(widgets.AdminTimeWidget):

    class Media:
        extend = ()
        js = (settings.STATIC_URL + 'extradmin/js/jquery.datetimepicker.js',)


class AdminSplitDateTime(widgets.AdminSplitDateTime):

    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(
            u'<div class="datetime"><span class="date">%s %s</span>'
            u'<span class="time">%s %s</span></div>' % (
                _(u'Date:'), rendered_widgets[0], _(u'Time:'), rendered_widgets[1])
        )


class ForeignKeyRawIdWidget(widgets.ForeignKeyRawIdWidget):

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        related_url = '../../../%s/%s/'
        related_url %= (self.rel.to._meta.app_label,
                        self.rel.to._meta.object_name.lower())
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(
                ['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        output = [forms.TextInput.render(self, name, value, attrs)]
        output.append(
            '<a href="%s%s" class="related-lookup" id="lookup_id_%s" > ' % \
                (related_url, url, name))
        output.append(
            '<img src="%simg/admin/selector-search.gif" width="16"' \
            ' height="16" alt="%s" /></a>' % \
                (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        if value:
            output.append(self.label_for_value(value))
        return mark_safe(u''.join(output))


class RelatedFieldWidgetWrapper(widgets.RelatedFieldWidgetWrapper):

    def render(self, name, value, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        try:
            related_url = reverse(
                'admin:%s_%s_add' % info, current_app=self.admin_site.name)
        except NoReverseMatch:
            info = (self.admin_site.root_path, rel_to._meta.app_label,
                    rel_to._meta.object_name.lower())
            related_url = '%s%s/%s/add/' % info
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if rel_to in self.admin_site._registry:
            output.append(
                u'<a href="%s" class="add-another" id="add_id_%s"> ' % \
                    (related_url, name))
            output.append(
                u'<img src="%simg/admin/icon_addlink.gif" width="10" ' \
                u' height="10" alt="%s"/></a>' % \
                    (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))


class PermissionSelectMultiple(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        str_values = set(force_unicode(v) for v in value)
        check_test = lambda value: value in str_values
        output = [u'<table class="permissions_select_multiple"><tr><td>']
        model_name_plural, j = '', 0
        for i, permission in enumerate(self.choices):
            if permission.model_name_plural != model_name_plural:
                if j != 0 and not (j % 3):
                    output.append(u'</tr><tr>')
                j += 1
                model_name_plural = permission.model_name_plural
                if i != 0:
                    output.append(u'</td><td>')
                output.append(u'<span>%s</span>' % model_name_plural.capitalize())
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = u''
            checkbox = forms.CheckboxInput(final_attrs, check_test=check_test)
            checkbox = checkbox.render(name, self.get_option_value(permission))
            output.append(u'<label%s>%s %s</label>' %
                          (label_for, checkbox, self.get_option_label(permission)))
        output.append(u'</tr></table>')
        return mark_safe(u'\n'.join(output))

    def get_option_value(self, permission):
        return force_unicode(self.choices.field.prepare_value(permission))

    def get_option_label(self, permission):
        opts = permission.content_type.model_class()._meta
        if permission.codename == opts.get_add_permission():
            permission_name = _(u'can add')
        elif permission.codename == opts.get_change_permission():
            permission_name = _(u'can change')
        elif permission.codename == opts.get_delete_permission():
            permission_name = _(u'can delete')
        else:
            permission_name = _(permission.name).lower()
        return conditional_escape(permission_name)
