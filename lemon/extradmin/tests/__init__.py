from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from lemon import extradmin
from lemon.extradmin import settings
from lemon.extradmin.admin import GroupExtrAdmin
from lemon.extradmin.forms import GroupPermissionsForm, PermissionMultipleChoiceField
from lemon.extradmin.tests.admin import ArticleAdmin, CustomTextarea
from lemon.extradmin.tests.models import Article
from lemon.extradmin.widgets import PermissionSelectMultiple


extradmin.autodiscover()


class DefaultMarkupWidgetTestCase(TestCase):

    def setUp(self):
        self.old_MARKUP_WIDGET = settings.CONFIG['MARKUP_WIDGET']
        settings.CONFIG['MARKUP_WIDGET'] = None

    def tearDown(self):
        settings.CONFIG['MARKUP_WIDGET'] = self.old_MARKUP_WIDGET

    def test_admin_site_markup_widget(self):
        self.assertIsNone(extradmin.AdminSite().markup_widget)

    def test_model_admin_markup_widget(self):
        model_admin = extradmin.ModelAdmin(Article, extradmin.AdminSite())
        self.assertIsNone(model_admin.markup_widget)


class CustomMarkupWidgetTestCase(TestCase):

    def setUp(self):
        self.old_MARKUP_WIDGET = settings.CONFIG['MARKUP_WIDGET']
        settings.CONFIG['MARKUP_WIDGET'] = 'django.forms.Textarea'

    def tearDown(self):
        settings.CONFIG['MARKUP_WIDGET'] = self.old_MARKUP_WIDGET

    def test_admin_site_markup_widget(self):
        self.assertIs(extradmin.AdminSite().markup_widget, forms.Textarea)

    def test_model_admin_markup_widget(self):
        model_admin = extradmin.ModelAdmin(Article, extradmin.AdminSite())
        self.assertIs(model_admin.markup_widget, forms.Textarea)


class MarkupFieldsTestCase(TestCase):

    def test_markup_fields(self):
        model_admin = ArticleAdmin(Article, extradmin.AdminSite())

        title_field = Article._meta.get_field('title')
        title_form_field = model_admin.formfield_for_dbfield(title_field)
        self.assertNotIsInstance(title_form_field.widget, CustomTextarea)

        content_field = Article._meta.get_field('content')
        content_form_field = model_admin.formfield_for_dbfield(content_field)
        self.assertIsInstance(content_form_field.widget, CustomTextarea)


class GroupPermissionsFormTestCase(TestCase):

    def setUp(self):
        self.editors = Group.objects.create(pk=1, name='Editors')
        self.managers = Group.objects.create(pk=2, name='Managers')

        content_type = ContentType.objects.get_for_model(Group)
        self.permissions = Permission.objects.filter(content_type=content_type)
        self.managers.permissions.add(*self.permissions)

    def tearDown(self):
        Group.objects.all().delete()

    def test_groups(self):
        form = GroupPermissionsForm()
        self.assertQuerysetEqual(
            form.groups.order_by('name'),
            [self.editors.pk, self.managers.pk],
            lambda x: x.pk,
        )

    def test_permissions(self):
        form = GroupPermissionsForm()
        self.assertQuerysetEqual(
            form.permissions.order_by('name'),
            [p.pk for p in Permission.objects.order_by('name')],
            lambda x: x.pk,
        )

    def test_initial(self):
        form = GroupPermissionsForm()
        self.assertEqual(len(form.initial), self.permissions.count())
        self.assertEqual(set(form.initial.values()), set([True]))
        keys = []
        for permission in self.permissions:
            keys.append('value_%s_%s' % (permission.pk, self.managers.pk))
        self.assertEqual(sorted(form.initial.keys()), sorted(keys))

    def test_initial_not_mutable(self):
        form = GroupPermissionsForm(initial={})
        self.assertNotEqual(form.initial, {})

    def test_save(self):
        permission = self.permissions[0]
        value_name = 'value_%s_%s' % (permission.pk, self.managers.pk)
        form = GroupPermissionsForm({value_name: 'on'})
        if form.is_valid():
            form.save()
        self.assertQuerysetEqual(
            self.managers.permissions.all(),
            [permission.pk],
            lambda x: x.pk,
        )


class GroupAdminTestCase(TestCase):

    def setUp(self):
        self.old_EXCLUDE_FROM_PERMISSIONS = settings.CONFIG['EXCLUDE_FROM_PERMISSIONS']
        settings.CONFIG['EXCLUDE_FROM_PERMISSIONS'] = (
            ('contenttypes', 'contenttype'),
        )

        self.editors = Group.objects.create(pk=1, name='Editors')
        self.managers = Group.objects.create(pk=2, name='Managers')

        content_type = ContentType.objects.get_for_model(Group)
        self.permissions = Permission.objects.filter(content_type=content_type)
        self.managers.permissions.add(*self.permissions)

        self.group_admin = GroupExtrAdmin(Group, extradmin.AdminSite())

    def tearDown(self):
        settings.CONFIG['EXCLUDE_FROM_PERMISSIONS'] = self.old_EXCLUDE_FROM_PERMISSIONS

    def test_permissions_field(self):
        form_class = self.group_admin.get_form(None)
        field = form_class.base_fields['permissions']
        self.assertIsInstance(field, PermissionMultipleChoiceField)
        self.assertIsInstance(field.widget.widget, PermissionSelectMultiple)

        queryset = Permission.objects.exclude(
            content_type__app_label = 'contenttypes',
            content_type__model = 'contenttype',
        )
        self.assertQuerysetEqual(
            field.queryset.order_by('pk'),
            [p.pk for p in queryset.order_by('pk')],
            lambda x: x.pk,
        )
