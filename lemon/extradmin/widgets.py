from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class AdminDateWidget(widgets.AdminDateWidget):

    @property
    def media(self):
        return forms.Media(js=[static('extradmin/js/jquery.datetimepicker.js')])


class AdminTimeWidget(widgets.AdminTimeWidget):

    @property
    def media(self):
        return forms.Media(js=[static('extradmin/js/jquery.datetimepicker.js')])


class AdminSplitDateTime(widgets.AdminSplitDateTime):

    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)


class ForeignKeyRawIdWidget(widgets.ForeignKeyRawIdWidget):

    def render(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []
        if rel_to in self.admin_site._registry:
            related_url = reverse(
                'admin:%s_%s_changelist' % (
                    rel_to._meta.app_label,
                    rel_to._meta.module_name
                ),
                current_app=self.admin_site.name,
            )

            params = self.url_parameters()
            if params:
                params = [u'%s=%s' % (k, v) for k, v in params.items()]
                params = u'&amp;'.join(params)
                url = u'?' + params
            else:
                url = u''
            if 'class' not in attrs:
                attrs['class'] = 'vForeignKeyRawIdAdminField'
            extra.append(
                u'<a href="%s%s" class="related-lookup" id="lookup_id_%s"> ' %
                    (related_url, url, name))
            extra.append(
                u'<img src="%s" width="16" height="16" alt="%s" /></a>' %
                    (static('admin/img/selector-search.gif'), _('Lookup')))
        output = [forms.TextInput.render(self, name, value, attrs)] + extra
        if value:
            output.append(self.label_for_value(value))
        return mark_safe(u''.join(output))


class RelatedFieldWidgetWrapper(widgets.RelatedFieldWidgetWrapper):

    def render(self, name, value, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.can_add_related:
            related_url = reverse('admin:%s_%s_add' % info, current_app=self.admin_site.name)
            output.append(
                u'<a href="%s" class="add-another" id="add_id_%s"> ' %
                    (related_url, name))
            output.append(
                u'<img src="%s" width="10" height="10" alt="%s"/></a>' %
                    (static('admin/img/icon_addlink.gif'), _('Add Another')))
        return mark_safe(u''.join(output))
