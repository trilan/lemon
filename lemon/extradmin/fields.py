from django.forms.models import ModelChoiceIterator, ModelChoiceField


class ContentTypeChoiceIterator(ModelChoiceIterator):

    def __init__(self, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        super(ContentTypeChoiceIterator, self).__init__(*args, **kwargs)
    
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u'', self.field.empty_label)
        for obj in self.queryset.all():
            key = obj.pk
            try:
                model_class = obj.model_class()
                if model_class in self.admin_site._registry.keys():
                    value = model_class._meta.verbose_name_plural
                    value = value and value[0].upper() + value[1:]
                    yield (key, value)
            except AttributeError:
                pass


class ContentTypeChoiceField(ModelChoiceField):
    
    def __init__(self, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        super(ContentTypeChoiceField, self).__init__(*args, **kwargs)
    
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return ContentTypeChoiceIterator(self.admin_site, self)
    choices = property(_get_choices, ModelChoiceField._set_choices)
