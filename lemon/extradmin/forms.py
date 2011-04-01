from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory
from django.forms.models import ModelForm, BaseInlineFormSet
from django.forms.models import ModelFormMetaclass, _get_foreign_key
from django.utils.translation import ugettext_lazy as _

from lemon.extradmin.fields import ContentTypeChoiceField
from lemon.extradmin.models import MenuItem


class MenuItemForm(forms.ModelForm):

    admin_site = None

    class Meta(object):
        fields = ['content_type', 'name', 'position']

    def __init__(self, *args, **kwargs):
        model = self._meta.model
        
        qs = ContentType.objects.all()
        
        content_type = ContentTypeChoiceField(self.admin_site, qs,
                                              label=_('content type'))
        self.base_fields['content_type'] = content_type
        super(MenuItemForm, self).__init__(*args, **kwargs)


formfield_callback = lambda f: f.formfield()


def contenttype_inlineformset_factory(parent_model, model, admin_site,
                                      formfield_callback,
                                      extra=3, can_order=False,
                                      can_delete=True, max_num=0):
    fk = _get_foreign_key(parent_model, model)
    Meta = type('Meta', (MenuItemForm.Meta,), {'model': model})
    class_name = model.__name__ + 'Form'
    form_class_attrs = {
        'admin_site': admin_site,
        'Meta': Meta,
        'formfield_callback': formfield_callback
    }
    form = ModelFormMetaclass(class_name, (MenuItemForm,), form_class_attrs)
    FormSet = formset_factory(form, BaseInlineFormSet, extra=extra,
                              max_num=max_num,
                              can_order=can_order, can_delete=can_delete)
    FormSet.model = model
    FormSet.fk = fk
    return FormSet
