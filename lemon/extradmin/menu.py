from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.datastructures import SortedDict


_registry = {}


class Menu(SortedDict):

    def __new__(cls, name, admin_site):
        if name in _registry:
            raise ImproperlyConfigured(
                'Menu with name %r already exists.' % name)
        instance = super(Menu, cls).__new__(cls, name, admin_site)
        _registry[name] = instance
        return instance

    @classmethod
    def with_name(self, name):
        return _registry[name]

    def __init__(self, name, admin_site):
        self.name = name
        self.admin_site = admin_site

    def add_section(self, name, title=None):
        section = Section(title or name.capitalize(), self.admin_site)
        self[name] = section
        return section

    def section(self, name):
        return self[name]

    def sections(self):
        return self.values()

    def non_empty_sections(self):
        return [section for section in self.sections() if section]


class Section(SortedDict):

    def __init__(self, title, admin_site):
        self.title = title
        self.admin_site = admin_site

    def add_item(self, name, model, title=None):
        item = Item(model, title or name.capitalize(), self.admin_site)
        self[name] = item
        return item

    def item(self, name):
        return self[name]

    def items(self):
        return self.values()


class Item(object):

    def __init__(self, model, title, admin_site):
        self.model = model
        self.title = title
        self.admin_site = admin_site

    def get_url(self, user=None, request=None):
        if request:
            model_admin = self.admin_site._register[self.model]
            if model_admin.has_change_permission(request):
                return self.get_changelist_url()
            if model_admin.has_add_permission(request):
                return self.get_add_url()
        elif user:
            if self.has_change_permission(user):
                return self.get_changelist_url()
            if self.has_add_permission(user):
                return self.get_add_url()

    def get_changelist_url(self):
        return reverse('admin:%s_%s_changelist' % self.get_opts())

    def get_add_url(self):
        return reverse('admin:%s_%s_add' % self.get_opts())

    def has_change_permission(self, user):
        return self.has_permission(user, self.model._meta.get_change_permission())

    def has_add_permission(self, user):
        return self.has_permission(user, self.model._meta.get_add_permission())

    def has_permission(self, user, permission_name):
        app_label = self.model._meta.app_label
        return user.has_perm('%s.%s' % (app_label, permission_name))

    def get_opts(self):
        return (self.model._meta.app_label, self.model._meta.module_name)

    def get_content_type(self):
        return ContentType.objects.get_for_model(self.model)
