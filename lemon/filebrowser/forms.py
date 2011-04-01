import os
import re

from django import forms
from django.utils.translation import ugettext as _


alnum_name_re = re.compile(r'^[\sa-zA-Z0-9._/-]+$')


class FileForm(forms.Form):
    
    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(FileForm, self).__init__(*args, **kwargs)
    
    def _normalize_name(self, name):
        return name.replace(' ', '_').lower()
    
    def _check_if_name_correct(self, name):
        if not alnum_name_re.search(name):
            raise forms.ValidationError(
                _(u'Only letters, numbers, underscores, spaces and '
                  u'hyphens are allowed.'))
    
    def _check_if_not_exists(self, name):
        if os.path.isdir(os.path.join(self.path, name)):
            raise forms.ValidationError(_(u'The folder with this name '
                                          u'already exists.'))
        if os.path.isfile(os.path.join(self.path, name)):
            raise forms.ValidationError(_(u'The file with this name '
                                          u'already exists.'))


class MakeDirForm(FileForm):

    dir_name = forms.CharField(
        label=_(u'Name'), min_length=3, max_length=50,
        help_text=_(u'Only letters, numbers, underscores, spaces and hyphens '
                    u'are allowed.'))

    def clean_dir_name(self):
        dir_name = self.cleaned_data['dir_name']
        self._check_if_name_correct(dir_name)
        dir_name = self._normalize_name(dir_name)
        self._check_if_not_exists(dir_name)
        return dir_name


class RenameForm(FileForm):

    name = forms.CharField(
        label=_(u'New Name'), min_length=3, max_length=50,
        help_text=_(u'Only letters, numbers, underscores, spaces and hyphens '
                    u'are allowed.'))

    def __init__(self, file_extension, *args, **kwargs):
        self.file_extension = file_extension
        super(RenameForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        self._check_if_name_correct(name)
        name_ext = self._normalize_name(name + self.file_extension)
        self._check_if_not_exists(name_ext)
        return name


class FileUploadForm(FileForm):
    
    file = forms.FileField(
        label=_(u'File'),
        help_text=_(u'Only letters, numbers, underscores, spaces and hyphens '
                    u'are allowed.'))
    
    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        self._check_if_name_correct(uploaded_file.name)
        uploaded_file.name = self._normalize_name(uploaded_file.name)
        self._check_if_not_exists(uploaded_file.name)
        return uploaded_file
