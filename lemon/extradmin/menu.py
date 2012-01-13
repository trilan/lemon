from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict


_registry = {}


class Menu(SortedDict):

    def __new__(cls, name):
        if name in _registry:
            raise ImproperlyConfigured(
                'Menu with name %r already exists.' % name)
        instance = super(Menu, cls).__new__(cls, name)
        _registry[name] = instance
        return instance

    @classmethod
    def with_name(self, name):
        return _registry[name]

    def __init__(self, name):
        self.name = name

    def add_section(self, name, title=None):
        section = Section(title or name.capitalize())
        self[name] = section
        return section

    def section(self, name):
        return self[name]

    def sections(self):
        return self.values()

    def non_empty_sections(self):
        return [section for section in self.sections() if section]


class Section(SortedDict):

    def __init__(self, title):
        self.title = title

    def add_item(self, name, model, title=None):
        item = Item(model, title or name.capitalize())
        self[name] = item
        return item

    def item(self, name):
        return self[name]

    def items(self):
        return self.values()


class Item(object):

    def __init__(self, model, title):
        self.model = model
        self.title = title

    def get_content_type(self):
        return ContentType.objects.get_for_model(self.model)
