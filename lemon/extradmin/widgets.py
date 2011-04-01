from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.core.urlresolvers import reverse, NoReverseMatch
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
