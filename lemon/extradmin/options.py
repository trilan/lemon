import inspect

from django import forms
from django.contrib.admin import options
from django.contrib.admin.views.main import IS_POPUP_VAR
from django.contrib.admin.widgets import AdminRadioSelect
from django.conf import settings
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon.extradmin import widgets


FORMFIELD_FOR_DBFIELD_DEFAULTS = {
    models.DateTimeField: {'form_class': forms.SplitDateTimeField,
                           'widget': widgets.AdminSplitDateTime},
    models.DateField: {'widget': widgets.AdminDateWidget}}


class IncorrectTabFormat(Exception):

    pass


class InlineInstanseNotFound(Exception):

    pass


class BaseModelAdmin(options.BaseModelAdmin):

    def __init__(self):
        self.filter_vertical = ()
        self.filter_horizontal = ()
        if self.fieldsets:
            self._fix_fieldsets()
        overrides = FORMFIELD_FOR_DBFIELD_DEFAULTS.copy()
        overrides.update(self.formfield_overrides)
        self.formfield_overrides = overrides
        super(BaseModelAdmin, self).__init__()

    def _fix_fieldsets(self):
        """
        Ugly hack for prevention of 'CollapsedFieldsets.js' inclusion.
        """
        for name, options in self.fieldsets:
            if 'classes' in options and 'collapse' in options['classes']:
                classes = tuple(set(options['classes']) - set(['collapse']))
                options['classes'] = classes

    def formfield_for_dbfield(self, db_field, **kwargs):
        request = kwargs.pop('request', None)
        if db_field.choices:
            return self.formfield_for_choice_field(
                db_field, request, **kwargs)
        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(
                    self.formfield_overrides[db_field.__class__], **kwargs)
            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(
                    db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(
                    db_field, request, **kwargs)
            if formfield and db_field.name not in self.raw_id_fields:
                formfield.widget = widgets.RelatedFieldWidgetWrapper(
                    formfield.widget, db_field.rel, self.admin_site)
            return formfield
        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[klass], **kwargs)
                return db_field.formfield(**kwargs)
        return db_field.formfield(**kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = widgets.ForeignKeyRawIdWidget(db_field.rel)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = AdminRadioSelect(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = db_field.blank and _('None') or None

        return db_field.formfield(**kwargs)


class ModelAdmin(options.ModelAdmin, BaseModelAdmin):

    string_overrides = {}
    tabs = False
    action_description_overrides = {}

    def __init__(self, model, admin_site):
        super(ModelAdmin, self).__init__(model, admin_site)
        if self.tabs:
            if isinstance(self.tabs, bool):
                tabs = []
                for inline in self.inline_instances:
                    tabs.append({'title': inline.verbose_name_plural,
                                 'contents': [inline]})
                self.tabs = tabs
            else:
                tabs = []
                for tab in self.tabs:
                    tabs.append(self._inspect_tab(tab))
                self.tabs = tabs

    def _inspect_tab(self, tab):
        if inspect.isclass(tab) and issubclass(tab, options.InlineModelAdmin):
            title, contents = self._get_tab_for_inline(tab)
            return {'title': title, 'contents': contents}
        if isinstance(tab, dict):
            contents = tab['contents']
            if inspect.isclass(contents) and \
               issubclass(contents, options.InlineModelAdmin):
                title, contents = self._get_tab_for_inline(contents)
                if 'title' in tab:
                    title = tab['title']
                return {'title': title, 'contents': contents}
            if isinstance(contents, (list, tuple)):
                if len(contents) == 1 and inspect.isclass(contents[0]) and \
                   issubclass(contents[0], options.InlineModelAdmin):
                    title, contents = self._get_tab_for_inline(contents[0])
                    if 'title' in tab:
                        title = tab['title']
                    return {'title': title, 'contents': contents}
                if 'title' not in tab:
                    raise IncorrectTabFormat(
                        u'No title provided for tab with multiple items.')
                new_contents = []
                for tab_item in contents:
                    new_contents.extend(self._get_tab_for_inline(tab_item)[1])
                tabs.append({'title': tab['title'], 'contents': new_contents})
        raise IncorrectTabFormat(u'Incorrect tab format.')

    def _get_tab_for_inline(self, inline):
        for inline_instance in self.inline_instances:
            if isinstance(inline_instance, inline):
                title = inline_instance.verbose_name_plural
                contents = [inline_instance]
                break
        else:
            raise InlineInstanseNotFound(
                u'It seems that inline %s is in %s.tabs but is not in '
                u'%s.inlines.' % (inline.__name__, self.__class__.__name__,
                                  self.__class__.__name__))
        return title, contents

    def _media(self):
        js = [settings.ADMIN_MEDIA_PREFIX + 'js/SelectBox.js',
              settings.STATIC_URL + 'extradmin/js/jquery.relatedobjectlookup.js']
        if self.prepopulated_fields:
            js.extend([settings.ADMIN_MEDIA_PREFIX + 'js/urlify.js',
                       settings.STATIC_URL + 'extradmin/js/jquery.prepopulate.js'])
        if self.tabs:
            js.extend([settings.STATIC_URL + 'extradmin/js/jquery-ui.lemon.tabs.js'])
        return forms.Media(js=js)
    media = property(_media)

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        tabs = False
        tabulated_formsets = []
        inline_admin_formsets = context.get('inline_admin_formsets')
        if self.tabs:
            formsets = {}
            for formset in context.get('inline_admin_formsets'):
                formsets[formset.opts] = formset
            tabs = []
            for tab in self.tabs:
                contents = [formsets[inline] for inline in tab['contents']]
                tabs.append({'title': tab['title'], 'contents': contents})
                tabulated_formsets.extend(contents)
            contents = [formset for formset in inline_admin_formsets \
                            if formset not in tabulated_formsets]
            tabs[0:0] = [{'title': _('General'), 'contents': contents}]
        context.update({'tabs': tabs})
        return super(ModelAdmin, self).render_change_form(
            request, context, add, change, form_url, obj)

    def get_actions(self, request):
        """
        Override generic descriptions with provided by child class.
        """
        if self.actions is None:
            return []
        actions = super(ModelAdmin, self).get_actions(request)
        new_actions = []
        for key, value in actions.items():
            new_actions.append((
                value[0],
                value[1],
                self.action_description_overrides.get(key, value[2])
            ))
        new_actions.sort(lambda a,b: cmp(a[2].lower(), b[2].lower()))
        actions = SortedDict([
            (name, (func, name, desc))
            for func, name, desc in new_actions
        ])
        return actions

    def add_view(self, request, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {'string_overrides': self.string_overrides}
        elif 'string_overrides' not in extra_context:
            extra_context['string_overrides'] = self.string_overrides
        if 'add_title' in self.string_overrides and 'title' not in extra_context:
            extra_context['title'] = self.string_overrides['add_title']
        return super(ModelAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, extra_context=None):
        if extra_context is None:
            extra_context = {'string_overrides': self.string_overrides}
        elif 'string_overrides' not in extra_context:
            extra_context['string_overrides'] = self.string_overrides
        if 'change_title' in self.string_overrides and 'title' not in extra_context:
            extra_context['title'] = self.string_overrides['change_title']
        return super(ModelAdmin, self).change_view(request, object_id, extra_context)

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {'string_overrides': self.string_overrides}
        elif 'string_overrides' not in extra_context:
            extra_context['string_overrides'] = self.string_overrides
        if 'changelist_title' in self.string_overrides and 'title' not in extra_context:
            extra_context['title'] = self.string_overrides['changelist_title']
        if 'changelist_paginator_description' in self.string_overrides and \
           'changelist_paginator_description' not in extra_context:
            extra_context['changelist_paginator_description'] = \
                self.string_overrides['changelist_paginator_description']
        else:
            extra_context['changelist_paginator_description'] = lambda n: \
                ungettext('%(count)d element', '%(count)d elements', n)
        return super(ModelAdmin, self).changelist_view(request, extra_context)


class InlineModelAdmin(options.InlineModelAdmin, BaseModelAdmin):

    def __init__(self, parent_model, admin_site):
        super(InlineModelAdmin, self).__init__(parent_model, admin_site)

    def _media(self):
        js = [settings.STATIC_URL + 'extradmin/js/jquery.inlines.js']
        if self.prepopulated_fields:
            js.append(settings.ADMIN_MEDIA_PREFIX + 'js/urlify.js')
            js.append(settings.STATIC_URL + 'extradmin/js/jquery.prepopulate.js')
        return forms.Media(js=js)
    media = property(_media)


class StackedInline(InlineModelAdmin):

    template = 'admin/edit_inline/stacked.html'


class TabularInline(InlineModelAdmin):

    template = 'admin/edit_inline/tabular.html'
