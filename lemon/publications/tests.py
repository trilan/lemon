from django.db import models
from django.test import TestCase, RequestFactory

from lemon.extradmin import AdminSite
from lemon.publications.admin import PublicationAdmin
from lemon.publications.models import Publication


class Article(Publication):

    title = models.CharField(max_length=100)
    content = models.TextField()


class PublicationAdminTests(TestCase):

    def setUp(self):
        self.admin = PublicationAdmin(Article, AdminSite())
        self.request = RequestFactory().get('/')

    def get_list_display(self, *args, **kwargs):
        return self.admin.get_list_display(self.request, *args, **kwargs)

    def test_default_list_display(self):
        self.assertEqual(self.get_list_display(), (
            '__str__', 'author_name', 'publication_start_date', 'enabled',
        ))

    def test_custom_list_display(self):
        self.admin.list_display = ('title', 'content')
        self.assertEqual(self.get_list_display(), (
            'title', 'content', 'author_name', 'publication_start_date', 'enabled',
        ))

    def test_extend_list_display_is_disabled(self):
        self.admin.list_display = ('title', 'content')
        self.admin.extend_list_display = False
        self.assertEqual(self.get_list_display(), ('title', 'content'))

    def test_extend_list_display_is_disabled_by_argument(self):
        self.admin.list_display = ('title', 'content')
        self.assertEqual(self.get_list_display(extend=False), ('title', 'content'))
