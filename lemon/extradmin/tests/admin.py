from django import forms

from lemon import extradmin
from lemon.extradmin.tests.models import Article


class CustomTextarea(forms.Textarea):

    pass


class ArticleAdmin(extradmin.ModelAdmin):

    markup_fields = ['content']
    markup_widget = CustomTextarea
