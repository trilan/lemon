from django import forms

from ..options import ModelAdmin, StackedInline
from .models import Author, Link


class CustomTextarea(forms.Textarea):

    pass


class AuthorInline(StackedInline):

    model = Author


class LinkInline(StackedInline):

    model = Link


class ArticleAdmin(ModelAdmin):

    markup_fields = ['content']
    markup_widget = CustomTextarea
    inlines = [AuthorInline, LinkInline]
