import inspect

from django import forms
from django.contrib.admin import options
from django.contrib.admin.templatetags.admin_static import static
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

    markup_fields = ()
    markup_widget = None

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
            return self.formfield_for_choice_field(db_field, request, **kwargs)

        if isinstance(db_field, (models.ForeignKey, models.ManyToManyField)):
            if db_field.__class__ in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[db_field.__class__], **kwargs)

            if isinstance(db_field, models.ForeignKey):
                formfield = self.formfield_for_foreignkey(db_field, request, **kwargs)
            elif isinstance(db_field, models.ManyToManyField):
                formfield = self.formfield_for_manytomany(db_field, request, **kwargs)

            if formfield and db_field.name not in self.raw_id_fields:
                related_modeladmin = self.admin_site._registry.get(db_field.rel.to)
                can_add_related = bool(related_modeladmin and
                                       related_modeladmin.has_add_permission(request))
                formfield.widget = widgets.RelatedFieldWidgetWrapper(
                    formfield.widget, db_field.rel, self.admin_site,
                    can_add_related=can_add_related)
            return formfield

        markup_widget = self.get_markup_widget(request)
        markup_fields = self.get_markup_fields(request)
        if markup_widget and db_field.name in markup_fields:
            return db_field.formfield(widget=markup_widget)

        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                kwargs = dict(self.formfield_overrides[klass], **kwargs)
                return db_field.formfield(**kwargs)

        return db_field.formfield(**kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        db = kwargs.get('using')
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = widgets.ForeignKeyRawIdWidget(
                db_field.rel, self.admin_site, using=db)
        elif db_field.name in self.radio_fields:
            kwargs['widget'] = AdminRadioSelect(attrs={
                'class': get_ul_class(self.radio_fields[db_field.name]),
            })
            kwargs['empty_label'] = db_field.blank and _('None') or None

        return db_field.formfield(**kwargs)

    def get_markup_widget(self, request):
        return self.markup_widget

    def get_markup_fields(self, request):
        return self.markup_fields


class ModelAdmin(options.ModelAdmin, BaseModelAdmin):

    string_overrides = {}
    tabs = False
    action_description_overrides = {}

    def _inspect_tab(self, request, tab):
        if isinstance(tab, dict):
            contents = tab['contents']
            if not isinstance(contents, (list, tuple)):
                contents = [contents]
            new_contents = []
            for inline in contents:
                inline_instance = self._get_inline_instance(request, inline)
                new_contents.append(inline_instance)
            return {'title': tab['title'], 'contents': new_contents}
        title, contents = self._get_tab_for_inline(request, tab)
        return {'title': title, 'contents': contents}

    def _get_inline_instance(self, request, inline):
        for inline_instance in self.get_inline_instances(request):
            if isinstance(inline_instance, inline):
                return inline_instance
        raise InlineInstanseNotFound(u'It seems that inline %s is in %s.tabs '
            u'but is not in %s.inlines.' % (inline.__name__,
            self.__class__.__name__, self.__class__.__name__))

    def _get_tab_for_inline(self, request, inline):
        inline_instance = self._get_inline_instance(request, inline)
        return inline_instance.verbose_name_plural, [inline_instance]

    @property
    def media(self):
        js = [static('admin/js/SelectBox.js'),
              static('extradmin/js/jquery.relatedobjectlookup.js')]
        if self.prepopulated_fields:
            js.extend(static('admin/js/urlify.js'),
                      static('extradmin/js/jquery.prepopulate.js'))
        if self.tabs:
            js.append(static('extradmin/js/jquery-ui.lemon.tabs.js'))
        return forms.Media(js=js)

    def get_tabs(self, request):
        if not self.tabs:
            return False
        tabs = []
        if isinstance(self.tabs, bool):
            for inline in self.get_inline_instances(request):
                tabs.append({'title': inline.verbose_name_plural,
                             'contents': [inline]})
        else:
            for tab in self.tabs:
                tabs.append(self._inspect_tab(request, tab))
        return tabs

    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        tabs = self.get_tabs(request)
        tabulated_formsets = []
        inline_admin_formsets = context.get('inline_admin_formsets')
        if tabs:
            formsets = {}
            for formset in context.get('inline_admin_formsets'):
                formsets[formset.opts.__class__] = formset
            new_tabs = []
            for tab in tabs:
                contents = [formsets[inline.__class__] for inline in tab['contents']]
                new_tabs.append({'title': tab['title'], 'contents': contents})
                tabulated_formsets.extend(contents)
            contents = [formset for formset in inline_admin_formsets
                        if formset not in tabulated_formsets]
            new_tabs.insert(0, {'title': _('General'), 'contents': contents})
            tabs = new_tabs
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
        return super(ModelAdmin, self).add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if extra_context is None:
            extra_context = {'string_overrides': self.string_overrides}
        elif 'string_overrides' not in extra_context:
            extra_context['string_overrides'] = self.string_overrides
        if 'change_title' in self.string_overrides and 'title' not in extra_context:
            extra_context['title'] = self.string_overrides['change_title']
        return super(ModelAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

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
        return super(ModelAdmin, self).changelist_view(request, extra_context=extra_context)

    def get_markup_widget(self, request):
        return self.markup_widget or self.admin_site.get_markup_widget(request)


class InlineModelAdmin(options.InlineModelAdmin, BaseModelAdmin):

    def __init__(self, parent_model, admin_site):
        super(InlineModelAdmin, self).__init__(parent_model, admin_site)

    @property
    def media(self):
        js = [static('extradmin/js/jquery.inlines.js')]
        if self.prepopulated_fields:
            js.append(static('admin/js/urlify.js'))
            js.append(static('extradmin/js/jquery.prepopulate.js'))
        return forms.Media(js=js)

    def get_markup_widget(self, request):
        return self.markup_widget or self.admin_site.get_markup_widget(request)


class StackedInline(InlineModelAdmin):

    template = 'admin/edit_inline/stacked.html'


class TabularInline(InlineModelAdmin):

    template = 'admin/edit_inline/tabular.html'
