from django import forms
from django.utils.translation import ugettext_lazy as _

from lemon.pages.models import Page
from lemon.pages.widgets import SelectPageTemplate


class PageAdminForm(forms.ModelForm):

    template = forms.CharField(
        label = _(u'Template'),
        max_length = 255,
        widget = SelectPageTemplate(),
        error_messages = {
            'required': _(u'Please create template for pages')
        },
    )

    class Meta:
        model = Page
