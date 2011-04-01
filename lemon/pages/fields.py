import re

from django import forms
from django.utils.translation import ugettext_lazy as _

url_path_re = re.compile(r'^/[\.\-/\w]*$')

class URLPathField(forms.RegexField):

    default_error_messages = {
        'invalid': _(u"Enter a valid 'slug' beginning with slash and consisting of letters, numbers,"
                     u" underscores, slashes or hyphens.")
    }

    def __init__(self, *args, **kwargs):
        super(URLPathField, self).__init__(url_path_re, *args, **kwargs)
