from django import forms
from django.contrib.auth.models import Group, Permission
from django.forms.models import ModelChoiceIterator

from lemon.extradmin.settings import CONFIG


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
        for app_label, model in CONFIG['EXCLUDE_FROM_PERMISSIONS']:
            self.permissions = self.permissions.exclude(
                content_type__app_label = app_label,
                content_type__model = model,
            )
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

    def __init__(self, queryset, *args, **kwargs):
        for app_label, model in CONFIG['EXCLUDE_FROM_PERMISSIONS']:
            queryset = queryset.exclude(
                content_type__app_label = app_label,
                content_type__model = model,
            )
        super(PermissionMultipleChoiceField, self).__init__(queryset, *args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return PermissionChoiceIterator(self)
    choices = property(_get_choices, forms.ChoiceField._set_choices)
