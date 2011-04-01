import os

from django.forms.widgets import Select
from django.utils.encoding import force_unicode

from lemon.pages import settings


class SelectPageTemplate(Select):

    def __init__(self, attrs=None):
        super(SelectPageTemplate, self).__init__(attrs)
    
    def _is_template(self, dir_, f):
        f = os.path.join(dir_, f)
        if not os.path.isfile(f):
            return False
        return any([f.endswith(e) for e in settings.TEMPLATE_EXTENSIONS])

    def _get_template_choices(self):
        template_dirs = [os.path.join(d, 'pages') for d in settings.TEMPLATE_DIRS]
        templates = []
        for dir_ in template_dirs:
            try:
                files = os.listdir(dir_)
            except OSError:
                pass
            else:
                templates.extend([f for f in files if self._is_template(dir_, f)])
        templates = [(force_unicode(t), force_unicode(t)) for t in sorted(list(set(templates)))]
        return templates

    def render_options(self, choices, selected_choices):
        self.choices = self._get_template_choices()
        return super(SelectPageTemplate, self).render_options(choices, selected_choices)
