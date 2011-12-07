import os
import operator
import re
from time import gmtime, strftime, localtime, time

from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.views.i18n import javascript_catalog

from lemon.filebrowser import settings
from lemon.filebrowser.base import FileObject
from lemon.filebrowser.utils import query_helper


class FileBrowserSite(object):

    upload_to = 'filebrowser'
    extensions = {'Folder': [''],
                  'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
                  'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
                  'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls',
                               '.csv'],
                  'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
                  'Code': ['.html', '.py', '.js', '.css']}
    select_formats = {'File': ['Folder', 'Document'],
                      'Image': ['Image'],
                      'Media': ['Video', 'Sound'],
                      'Document': ['Document']}
    order_by = '-date'
    list_per_page = 100
    convert_filenames = True
    max_upload_size = 10 * 1024 * 1024

    def __init__(self, admin_site, name='filebrowser',
                 app_name='filebrowser'):
        self.admin_site = admin_site
        self.name = name
        self.app_name = app_name
        self.extension_list = []
        for exts in self.extensions.values():
            self.extension_list.extend(exts)
        self.sort_order = 'desc' if self.order_by.startswith('-') else 'asc'
        self.sort_by = self.order_by.strip('+-')

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns(
            '',
            url(r'^$',
                self.admin_site.admin_view(self.browse_view),
                name='browse'),
            url(r'^mkdir/$',
                self.admin_site.admin_view(self.mkdir_view),
                name='mkdir'),
            url(r'^upload/$',
                self.admin_site.admin_view(self.upload_view),
                name='upload'),
            url(r'^rename/$',
                self.admin_site.admin_view(self.rename_view),
                name='rename'),
            url(r'^delete/$',
                self.admin_site.admin_view(self.delete_view),
                name='delete'),
            url(r'^jsi18n/$',
                self.admin_site.admin_view(self.i18n_javascript),
                name='jsi18n'),
        )

        return urlpatterns

    def urls(self):
        return self.get_urls(), self.app_name, self.name
    urls = property(urls)

    def get_path(self, path):
        fullpath = os.path.join(settings.MEDIA_ROOT, self.upload_to, path)
        if path.startswith('.') or os.path.isabs(path) or \
           not os.path.isdir(fullpath):
            return None
        return path

    def get_file(self, path, filename):
        abs_path = os.path.join(
            settings.MEDIA_ROOT, self.upload_to, path, filename)
        if not os.path.isfile(abs_path) and not os.path.isdir(abs_path):
            return None
        return filename

    def get_breadcrumbs(self, query, path):
        breadcrumbs = []
        dir_query = ''
        if path:
            for item in path.split(os.sep):
                dir_query = os.path.join(dir_query, item)
                breadcrumbs.append([item, dir_query])
        return breadcrumbs

    def get_filterdate(self, filter_date, date_time):
        date_year = strftime('%Y', gmtime(date_time))
        date_month = strftime('%m', gmtime(date_time))
        date_day = strftime('%d', gmtime(date_time))
        if filter_date == 'today' and \
           int(date_year) == int(localtime()[0]) and \
           int(date_month) == int(localtime()[1]) and \
           int(date_day) == int(localtime()[2]):
            return 'true'
        if filter_date == 'thismonth' and date_time >= time() - 2592000:
            return 'true'
        if filter_date == 'thisyear' and \
           int(date_year) == int(localtime()[0]):
            return 'true'
        if filter_date == 'past7days' and date_time >= time() - 604800:
            return 'true'
        if filter_date == '':
            return 'true'
        return ''

    def sort_by_attr(self, seq, attr):
        intermed = map(None, map(getattr, seq, (attr,)*len(seq)),
                       xrange(len(seq)), seq)
        intermed.sort()
        return map(operator.getitem, intermed, (-1,) * len(intermed))

    def browse_view(self, request):
        query = request.GET.copy()

        directory = self.get_path('')
        if directory is None:
            try:
                os.makedirs(
                    os.path.join(settings.MEDIA_ROOT, self.upload_to), 0755)
            except OSError:
                raise ImproperlyConfigured(
                    "Error finding upload-folder. It seems that we can't "
                    " create it.")
            else:
                directory = self.get_path('')

        path = self.get_path(query.get('dir', ''))
        if path is None:
            msg = _('The requested folder does not exist.')
            request.user.message_set.create(message=msg)
            redirect_url = reverse('admin:filebrowser:browse')
            redirect_url += query_helper(query, 'dir')
            return HttpResponseRedirect(redirect_url)
        abs_path = os.path.join(settings.MEDIA_ROOT, self.upload_to, path)

        results_var = {'results_total': 0, 'delete_total': False}
        counter = {}
        for key in self.extensions.iterkeys():
            counter[key] = 0
        dir_list = os.listdir(abs_path)
        file_objects = []
        for filename in dir_list:
            if filename.startswith('.'):
                continue
            relative_path = os.path.join(self.upload_to, path, filename)
            file_object = FileObject(relative_path, self)
            q = request.GET.get('q')
            filter_type = request.GET.get('filter_type', file_object.filetype)
            filter_date = request.GET.get('filter_date', '')
            filter_date = self.get_filterdate(filter_date, file_object.date)
            append = file_object.filetype == filter_type and filter_date
            if q and not re.compile(q.lower(), re.M).search(filename.lower()):
                append = False
            if append:
                try:
                    if file_object.filetype != 'Folder' or \
                       file_object.is_empty:
                        results_var['delete_total'] = True
                except OSError:
                    continue
                else:
                    file_objects.append(file_object)
                    results_var['results_total'] += 1
            if file_object.filetype:
                counter[file_object.filetype] += 1
        query['o'] = request.GET.get('o', self.sort_by)
        query['ot'] = request.GET.get('ot', self.sort_order)
        file_objects = self.sort_by_attr(file_objects, query['o'])
        if query['ot'] == 'desc':
            file_objects.reverse()

        paginator = Paginator(file_objects, self.list_per_page)
        page_number = request.GET.get('p', 1)
        try:
            page_number = int(page_number)
        except ValueError:
            raise Http404
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            raise Http404

        return render_to_response('filebrowser/browse.html',
            {'dir': path,
             'page': page,
             'results_var': results_var,
             'query': query,
             'title': _(u'File Browser'),
             'breadcrumbs': self.get_breadcrumbs(query, path),
             'breadcrumbs_title': '',
             'is_popup': request.GET.get('pop', False),
             'editor': request.GET.get('editor', None)},
            context_instance=RequestContext(request))

    def mkdir_view(self, request):
        from lemon.filebrowser.forms import MakeDirForm

        query = request.GET.copy()
        path = self.get_path(query.get('dir', ''))
        if path is None:
            msg = _('The requested folder does not exist.')
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect(reverse('admin:filebrowser:browse'))
        abs_path = os.path.join(settings.MEDIA_ROOT, self.upload_to, path)

        if request.method == 'POST':
            form = MakeDirForm(abs_path, request.POST)
            if form.is_valid():
                server_path = os.path.join(abs_path,
                                           form.cleaned_data['dir_name'])
                try:
                    os.mkdir(server_path)
                    os.chmod(server_path, 0775)
                except OSError, (errno, strerror):
                    if errno == 13:
                        form.errors['dir_name'] = ErrorList(
                            [_('Permission denied.')]
                        )
                    else:
                        form.errors['dir_name'] = ErrorList(
                            [_('Error creating folder.')]
                        )
                else:
                    msg = _('The folder "%s" was successfully created.')
                    msg %= form.cleaned_data['dir_name']
                    request.user.message_set.create(message=msg)
                    # on redirect, sort by date desc to see the new directory
                    # on top of the list
                    # remove filter in order to actually _see_ the new folder
                    # remove pagination
                    redirect_url = reverse("admin:filebrowser:browse")
                    redirect_url += query_helper(
                        query, 'o', 'q', 'p', 'ot', 'filter_type',
                        'filter_date', o='date', ot='desc')
                    return HttpResponseRedirect(redirect_url)
        else:
            form = MakeDirForm(abs_path)

        return render_to_response(
            'filebrowser/makedir.html',
            {'form': form,
             'query': query,
             'title': _(u'New Folder'),
             'breadcrumbs': self.get_breadcrumbs(query, path),
             'breadcrumbs_title': _(u'New Folder'),
             'is_popup': request.GET.get('pop', False)},
            context_instance=RequestContext(request))

    def upload_view(self, request):
        from lemon.filebrowser.forms import FileUploadForm

        query = request.GET.copy()
        path = self.get_path(query.get('dir', ''))
        if path is None:
            msg = _('The requested folder does not exist.')
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect(reverse('admin:filebrowser:browse'))
        abs_path = os.path.join(settings.MEDIA_ROOT, self.upload_to, path)

        if request.method == 'POST':
            form = FileUploadForm(abs_path, request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.cleaned_data['file']
                f = open(os.path.join(abs_path, uploaded_file.name), 'wb+')
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
                f.close()
                redirect_url = reverse("admin:filebrowser:browse")
                redirect_url += query_helper(
                    query, 'o', 'q', 'p', 'ot', 'filter_type', 'filter_date',
                    ot='desc', o='date')
                return HttpResponseRedirect(redirect_url)
        else:
            form = FileUploadForm(abs_path)

        return render_to_response(
            'filebrowser/upload.html',
            {'form': form,
             'query': query,
             'title': _(u'Upload File'),
             'is_popup': request.GET.get('pop', False)},
            context_instance=RequestContext(request))

    def rename_view(self, request):
        from lemon.filebrowser.forms import RenameForm

        query = request.GET.copy()
        path = self.get_path(query.get('dir', ''))
        filename = self.get_file(
            query.get('dir', ''), query.get('filename', ''))
        if path is None or filename is None:
            if path is None:
                msg = _('The requested folder does not exist.')
            else:
                msg = _('The requested file does not exist.')
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect(reverse('admin:filebrowser:browse'))
        abs_path = os.path.join(settings.MEDIA_ROOT, self.upload_to, path)
        file_extension = os.path.splitext(filename)[1].lower()

        if request.method == 'POST':
            form = RenameForm(file_extension, abs_path, request.POST)
            if form.is_valid():
                server_path = os.path.join(
                    settings.MEDIA_ROOT, self.upload_to, path, filename)
                new_filename = form.cleaned_data['name'] + file_extension
                new_server_path = os.path.join(
                    settings.MEDIA_ROOT, self.upload_to, path, new_filename)
                try:
                    os.rename(server_path, new_server_path)
                    if os.path.isdir(new_server_path):
                        msg = _('The folder was successfully renamed.')
                    else:
                        msg = _('The file was successfully renamed.')
                except OSError, (errno, strerror):
                    msg = _(u'OS error while delete.')
                else:
                    request.user.message_set.create(message=msg)
                    redirect_url = reverse("admin:filebrowser:browse")
                    redirect_url += query_helper(query, 'filename')
                    return HttpResponseRedirect(redirect_url)
        else:
            form = RenameForm(file_extension, abs_path)

        return render_to_response('filebrowser/rename.html', {
            'form': form,
            'query': query,
            'file_extension': file_extension,
            'title': _(u'Rename "%s"') % filename,
            'breadcrumbs': self.get_breadcrumbs(query, path),
            'breadcrumbs_title': _(u'Rename'),
            'is_popup': request.GET.get('pop', False)
        }, context_instance=RequestContext(request))

    def delete_view(self, request):
        query = request.GET.copy()
        path = self.get_path(query.get('dir', ''))
        filename = self.get_file(
            query.get('dir', ''), query.get('filename', ''))
        if path is None or filename is None:
            if path is None:
                msg = _('The requested folder does not exist.')
            else:
                msg = _('The requested file does not exist.')
            request.user.message_set.create(message=msg)
            return HttpResponseRedirect(reverse('admin:filebrowser:browse'))
        abs_path = os.path.join(settings.MEDIA_ROOT, self.upload_to, path)

        msg = ''
        if request.GET:
            if request.GET.get('filetype') != 'Folder':
                try:
                    os.unlink(os.path.join(abs_path, filename))
                except OSError:
                    msg = _(u'OS error while delete.')
                else:
                    msg = _('The file "%s" was successfully deleted.')
                    msg %= filename.lower()
                    request.user.message_set.create(message=msg)
                    redirect_url = reverse('admin:filebrowser:browse')
                    redirect_url += query_helper(
                        query, 'filename', 'filetype')
                    return HttpResponseRedirect(redirect_url)
            else:
                try:
                    os.rmdir(os.path.join(abs_path, filename))
                except OSError:
                    msg = _(u'OS error while delete.')
                else:
                    msg = _('The folder "%s" was successfully deleted.')
                    msg %= filename.lower()
                    request.user.message_set.create(message=msg)
                    redirect_url = reverse('admin:filebrowser:browse')
                    redirect_url += query_helper(
                        query, 'filename',  'filetype')
                    return HttpResponseRedirect(redirect_url)
        if msg:
            request.user.message_set.create(message=msg)

        return render_to_response('filebrowser/browse.html', {
            'dir': dir_name,
            'file': request.GET.get('filename', ''),
            'query': query,
            'breadcrumbs': self.get_breadcrumbs(query, dir_name),
            'breadcrumbs_title': '',
            'is_popup': request.GET.get('pop', False)
        }, context_instance=RequestContext(request))

    def i18n_javascript(self, request):
        return javascript_catalog(
            request, packages='lemon.filebrowser')
