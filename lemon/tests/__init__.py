from django import forms
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from ..options import ModelAdmin
from ..settings import CONFIG
from ..sites import AdminSite
from .admin import ArticleAdmin, AuthorInline, LinkInline, CustomTextarea
from .models import Article


class DefaultMarkupWidgetTestCase(TestCase):

    def setUp(self):
        self.old_MARKUP_WIDGET = CONFIG['MARKUP_WIDGET']
        CONFIG['MARKUP_WIDGET'] = None
        self.request = RequestFactory().get('/')

    def tearDown(self):
        CONFIG['MARKUP_WIDGET'] = self.old_MARKUP_WIDGET

    def test_admin_site_markup_widget(self):
        admin_site = AdminSite()
        self.assertIsNone(admin_site.get_markup_widget(self.request))

    def test_model_admin_markup_widget(self):
        model_admin = ModelAdmin(Article, AdminSite())
        self.assertIsNone(model_admin.get_markup_widget(self.request))


class CustomMarkupWidgetTestCase(TestCase):

    def setUp(self):
        self.old_MARKUP_WIDGET = CONFIG['MARKUP_WIDGET']
        CONFIG['MARKUP_WIDGET'] = 'django.forms.Textarea'
        self.request = RequestFactory().get('/')

    def tearDown(self):
        CONFIG['MARKUP_WIDGET'] = self.old_MARKUP_WIDGET

    def test_admin_site_markup_widget(self):
        admin = AdminSite()
        self.assertIs(admin.get_markup_widget(self.request), forms.Textarea)

    def test_model_admin_markup_widget(self):
        model_admin = ModelAdmin(Article, AdminSite())
        markup_widget = model_admin.get_markup_widget(self.request)
        self.assertIs(markup_widget, forms.Textarea)


class MarkupFieldsTestCase(TestCase):

    def test_markup_fields(self):
        model_admin = ArticleAdmin(Article, AdminSite())

        title_field = Article._meta.get_field('title')
        title_form_field = model_admin.formfield_for_dbfield(title_field)
        self.assertNotIsInstance(title_form_field.widget, CustomTextarea)

        content_field = Article._meta.get_field('content')
        content_form_field = model_admin.formfield_for_dbfield(content_field)
        self.assertIsInstance(content_form_field.widget, CustomTextarea)


class AdminTabsTestCase(TestCase):

    def get_request(self):
        request = RequestFactory().get('/')
        request.user = User.objects.create(username='admin', is_superuser=True)
        return request

    def get_tabs(self, admin_class):
        admin = admin_class(Article, AdminSite())
        return admin.get_tabs(self.get_request())

    def test_returns_false_if_tabs_are_disabled(self):
        class Admin(ArticleAdmin):
            tabs = False

        self.assertFalse(self.get_tabs(Admin))

    def test_returns_false_by_default(self):
        class Admin(ArticleAdmin):
            pass

        self.assertFalse(self.get_tabs(Admin))

    def test_returns_list_if_tabs_are_enabled(self):
        class Admin(ArticleAdmin):
            tabs = True

        tabs = self.get_tabs(Admin)
        self.assertEqual(len(tabs), 2)
        self.assertEqual(len(tabs[0]['contents']), 1)
        self.assertEqual(len(tabs[1]['contents']), 1)
        self.assertIsInstance(tabs[0]['contents'][0], AuthorInline)
        self.assertIsInstance(tabs[1]['contents'][0], LinkInline)

    def test_returns_list_if_tabs_are_list_of_inlines(self):
        class Admin(ArticleAdmin):
            tabs = [AuthorInline, LinkInline]

        tabs = self.get_tabs(Admin)
        self.assertEqual(len(tabs), 2)
        self.assertEqual(len(tabs[0]['contents']), 1)
        self.assertEqual(len(tabs[1]['contents']), 1)
        self.assertIsInstance(tabs[0]['contents'][0], AuthorInline)
        self.assertIsInstance(tabs[1]['contents'][0], LinkInline)

    def test_returns_list_if_tabs_are_list_of_dicts(self):
        class Admin(ArticleAdmin):
            tabs = [{
                'title': 'Additional',
                'contents': [AuthorInline, LinkInline],
            }]

        tabs = self.get_tabs(Admin)
        self.assertEqual(len(tabs), 1)
        self.assertEqual(len(tabs[0]['contents']), 2)
        self.assertIsInstance(tabs[0]['contents'][0], AuthorInline)
        self.assertIsInstance(tabs[0]['contents'][1], LinkInline)

    def test_returns_list_if_tabs_are_list_of_dicts_of_classes(self):
        class Admin(ArticleAdmin):
            tabs = [
                {'title': 'Author', 'contents': AuthorInline},
                {'title': 'Link', 'contents': LinkInline},
            ]

        tabs = self.get_tabs(Admin)
        self.assertEqual(len(tabs), 2)
        self.assertEqual(len(tabs[0]['contents']), 1)
        self.assertEqual(len(tabs[1]['contents']), 1)
        self.assertIsInstance(tabs[0]['contents'][0], AuthorInline)
        self.assertIsInstance(tabs[1]['contents'][0], LinkInline)
