from django import forms
from django.test import TestCase

from lemon import extradmin
from lemon.extradmin import settings
from lemon.extradmin.tests.admin import ArticleAdmin, CustomTextarea
from lemon.extradmin.tests.models import Article


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
