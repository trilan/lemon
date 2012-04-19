import datetime
import os
import re

from django.utils import formats
from django.utils.text import capfirst

from lemon.filebrowser.settings import MEDIA_ROOT, MEDIA_URL


class FileObject(object):

    def __init__(self, path, file_browser_site):
        self.path = path
        self.file_browser_site = file_browser_site
        self.head = os.path.split(path)[0]
        self.filename = os.path.split(path)[1]
        self.filename_lower = self.filename.lower() # important for sorting
        self.filetype = self._get_filetype()
    
    def _get_filetype(self):
        file_extension = os.path.splitext(self.filename_lower)[1]
        if os.path.isdir(os.path.join(MEDIA_ROOT, self.path)):
            return 'Folder'
        for key, value in self.file_browser_site.extensions.iteritems():
            for extension in value:
                if file_extension == extension.lower():
                    return key
        return ''

    def _filesize(self):
        if os.path.isfile(os.path.join(MEDIA_ROOT, self.path)) or \
           os.path.isdir(os.path.join(MEDIA_ROOT, self.path)):
            return os.path.getsize(os.path.join(MEDIA_ROOT, self.path))
        return ""
    filesize = property(_filesize)

    def _date(self):
        if os.path.isfile(os.path.join(MEDIA_ROOT, self.path)) or \
           os.path.isdir(os.path.join(MEDIA_ROOT, self.path)):
            return os.path.getmtime(os.path.join(MEDIA_ROOT, self.path))
        return ""
    date = property(_date)

    def _datetime(self):
        return datetime.datetime.fromtimestamp(self.date)
    datetime = property(_datetime)

    def _formatted_datetime(self):
        return capfirst(formats.date_format(self.datetime, 'DATETIME_FORMAT'))
    formatted_datetime = property(_formatted_datetime)

    def _extension(self):
        return u"%s" % os.path.splitext(self.filename)[1]
    extension = property(_extension)

    def _filetype_checked(self):
        if self.filetype == "Folder" and os.path.isdir(self.path_full):
            return self.filetype
        elif self.filetype != "Folder" and os.path.isfile(self.path_full):
            return self.filetype
        else:
            return ""
    filetype_checked = property(_filetype_checked)

    def _path_full(self):
        return u"%s" % os.path.join(MEDIA_ROOT, self.path)
    path_full = property(_path_full)

    def _path_relative_directory(self):
        directory_re = re.compile(r'^(%s)' % self.file_browser_site.upload_to)
        value = directory_re.sub('', self.path).lstrip('/')
        return u"%s" % value
    path_relative_directory = property(_path_relative_directory)

    def _url_full(self):
        return u"%s" % self._url_join(MEDIA_URL, self.path)
    url_full = property(_url_full)

    def _is_empty(self):
        if os.path.isdir(self.path_full):
            if not os.listdir(self.path_full):
                return True
            else:
                return False
        else:
            return None
    is_empty = property(_is_empty)
    
    def _url_join(self, *args):
        if args[0].startswith("http://"):
            url = "http://"
        else:
            url = "/"
        for arg in args:
            arg = unicode(arg).replace("\\", "/")
            arg_split = arg.split("/")
            for elem in arg_split:
                if elem != "" and elem != "http:":
                    url = url + elem + "/"
        # remove trailing slash for filenames
        if os.path.splitext(args[-1])[1]:
            url = url.rstrip("/")
        return url

    def __repr__(self):
        return u'%s' % self.path

    def __str__(self):
        return '%s' % self.path

    def __unicode__(self):
        return u'%s' % self.path
