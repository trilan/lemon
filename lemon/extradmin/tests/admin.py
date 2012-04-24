from django import forms

from lemon import extradmin
from lemon.extradmin.tests.models import Article, Author, Link


class CustomTextarea(forms.Textarea):

    pass


class AuthorInline(extradmin.StackedInline):

    model = Author


class LinkInline(extradmin.StackedInline):

    model = Link


class ArticleAdmin(extradmin.ModelAdmin):

    markup_fields = ['content']
    markup_widget = CustomTextarea
    inlines = [AuthorInline, LinkInline]
