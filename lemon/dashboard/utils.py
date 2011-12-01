from django.conf import settings
from django.forms.widgets import Media as DjangoMedia
from django.template import loader
from django.template.base import TemplateDoesNotExist


MEDIA_TYPES = ('css', 'js')


def find_template_source_loaders():
    loaders = []
    for loader_name in settings.TEMPLATE_LOADERS:
        l = loader.find_template_loader(loader_name)
        if l is not None:
            loaders.append(l)
    return tuple(loaders)


def find_template_source(name):
    global loader
    if loader.template_source_loaders is None:
        loader.template_source_loaders = self.find_template_source_loaders()
    for l in loader.template_source_loaders:
        try:
            source, display_name = l.load_template_source(name)
            return source
        except TemplateDoesNotExist:
            pass
    raise TemplateDoesNotExist(name)


class Media(DjangoMedia):

    def __init__(self, media=None, **kwargs):
        media_attrs = media.__dict__ if media else kwargs
        self._css = []
        self._js = []
        for name in MEDIA_TYPES:
            getattr(self, 'add_' + name)(media_attrs.get(name))

    def __add__(self, other):
        combined = Media()
        for name in MEDIA_TYPES:
            getattr(combined, 'add_' + name)(getattr(self, '_' + name, None))
            getattr(combined, 'add_' + name)(getattr(other, '_' + name, None))
        return combined

    def __getitem__(self, name):
        if name in MEDIA_TYPES:
            return Media(**{str(name): getattr(self, '_' + name)})
        raise KeyError('Unknown media type "%s"' % name)

    def add_css(self, data):
        if not data:
            return
        for path in data:
            if path not in self._css:
                self._css.append(path)

    def render_css(self):
        tag = lambda path: u'<link rel="stylesheet" href="%s">' % path
        return [tag(self.absolute_path(path)) for path in self._css]

    def render_js(self):
        tag = lambda path: u'<script src="%s"></script>' % path
        return [tag(self.absolute_path(path)) for path in self._js]


def media_property(cls):
    def _media(self):
        if hasattr(super(cls, self), 'media'):
            base = super(cls, self).media
        else:
            base = Media()
        definition = getattr(cls, 'Media', None)
        if definition:
            extend = getattr(definition, 'extend', True)
            if extend:
                if extend == True:
                    m = base
                else:
                    m = Media()
                    for medium in extend:
                        m = m + base[medium]
                return m + Media(definition)
            return Media(definition)
        return base
    return property(_media)


class MediaDefiningClass(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(MediaDefiningClass, cls).__new__(
            cls, name, bases, attrs)
        if 'media' not in attrs:
            new_class.media = media_property(new_class)
        return new_class
