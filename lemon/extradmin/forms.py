from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory
from django.forms.models import ModelForm, BaseInlineFormSet
from django.forms.models import ModelFormMetaclass, _get_foreign_key
from django.forms.models import ModelChoiceIterator
from django.utils.translation import ugettext_lazy as _

from lemon.extradmin.fields import ContentTypeChoiceField
from lemon.extradmin.models import MenuItem


class MenuItemForm(forms.ModelForm):

    admin_site = None

    class Meta(object):
        fields = ['content_type', 'name', 'position']

    def __init__(self, *args, **kwargs):
        model = self._meta.model
        
        qs = ContentType.objects.all()
        
        content_type = ContentTypeChoiceField(self.admin_site, qs,
                                              label=_('content type'))
        self.base_fields['content_type'] = content_type
        super(MenuItemForm, self).__init__(*args, **kwargs)


formfield_callback = lambda f: f.formfield()


def contenttype_inlineformset_factory(parent_model, model, admin_site,
                                      formfield_callback,
                                      extra=3, can_order=False,
                                      can_delete=True, max_num=0):
    fk = _get_foreign_key(parent_model, model)
    Meta = type('Meta', (MenuItemForm.Meta,), {'model': model})
    class_name = model.__name__ + 'Form'
    form_class_attrs = {
        'admin_site': admin_site,
        'Meta': Meta,
        'formfield_callback': formfield_callback
    }
    form = ModelFormMetaclass(class_name, (MenuItemForm,), form_class_attrs)
    FormSet = formset_factory(form, BaseInlineFormSet, extra=extra,
                              max_num=max_num,
                              can_order=can_order, can_delete=can_delete)
    FormSet.model = model
    FormSet.fk = fk
    return FormSet


class GroupPermissionsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        values = Group.permissions.through.objects.all()
        values = values.values_list('permission_id', 'group_id')
        initial = {}
        for value in values:
            initial['value_%s_%s' % value] = True
        kwargs['initial'] = initial
        super(GroupPermissionsForm, self).__init__(*args, **kwargs)
        self.groups = Group.objects.all()
        self.permissions = Permission.objects.select_related('content_type')
        for permission in self.permissions:
            for group in self.groups:
                name = 'value_%s_%s' % (permission.pk, group.pk)
                self.fields[name] = forms.BooleanField(required=False)

    def save(self):
        group_ids = {}
        for name, checked in self.cleaned_data.items():
            _, permission_id, group_id = name.split('_')
            permission_ids = group_ids.setdefault(group_id, [])
            if checked:
                permission_ids.append(permission_id)
        permissions_field = Group._meta.get_field_by_name('permissions')[0]
        for group in self.groups:
            permission_ids = group_ids.get(str(group.pk), [])
            permissions_field.save_form_data(group, permission_ids)


class PermissionChoiceIterator(ModelChoiceIterator):

    def __iter__(self):
        permissions = []
        for permission in self.queryset.all():
            model_class = permission.content_type.model_class()
            model_name_plural = model_class._meta.verbose_name_plural
            setattr(permission, 'model_name_plural', model_name_plural)
            permissions.append(permission)
        permissions.sort(key=lambda x: x.model_name_plural)
        for permission in permissions:
            yield permission


class PermissionMultipleChoiceField(forms.ModelMultipleChoiceField):

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return PermissionChoiceIterator(self)
    choices = property(_get_choices, forms.ChoiceField._set_choices)
