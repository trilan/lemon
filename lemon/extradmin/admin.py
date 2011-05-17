from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.auth.admin import (
    GroupAdmin as DjangoGroupAdmin, UserAdmin as DjangoUserAdmin)
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.admin import SiteAdmin as DjangoSiteAdmin
from django.contrib.sites.models import Site
from django.db import models
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin
from lemon.extradmin.dashboard import AppsWidget, LogWidget
from lemon.extradmin.forms import MenuItemForm, GroupPermissionsForm
from lemon.extradmin.forms import PermissionMultipleChoiceField
from lemon.extradmin.forms import contenttype_inlineformset_factory
from lemon.extradmin.models import MenuSection, MenuItem
from lemon.extradmin.widgets import PermissionSelectMultiple


class MenuItemInline(extradmin.TabularInline):

    form = MenuItemForm
    model = MenuItem

    def get_formset(self, request, obj=None, **kwargs):
        defaults = {
            "formfield_callback": curry(self.formfield_for_dbfield,
                                        request=request),
            "extra": self.extra,
            "max_num": self.max_num,
        }
        defaults.update(kwargs)
        return contenttype_inlineformset_factory(self.parent_model, self.model,
                                                 self.admin_site, **defaults)


class MenuSectionAdmin(extradmin.ModelAdmin):

    string_overrides = {
        'add_title': _(u'Add menu section'),
        'change_title': _(u'Change menu section'),
        'changelist_title': _(u'Choose menu section to change'),
        'changelist_popup_title': _(u'Choose menu section'),
        'changelist_addlink_title': _(u'Add menu section'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d menu section', '%(count)d menu sections', n)
    }
    tabs = True
    inlines = [MenuItemInline]


class UserAdmin(extradmin.ModelAdmin, DjangoUserAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
            'description': _(
                u"First, enter a username and password. "
                u"Then, you'll be able to edit more user options.")}
        ),
    )
    string_overrides = {
        'add_title': _(u'Add user'),
        'change_title': _(u'Change user'),
        'changelist_title': _(u'Choose user to change'),
        'changelist_popup_title': _(u'Choose user'),
        'changelist_addlink_title': _(u'Add user'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d user', '%(count)d users', n)
    }

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'user_permissions':
            kwargs['form_class'] = PermissionMultipleChoiceField
            kwargs['widget'] = PermissionSelectMultiple
            kwargs['help_text'] = u''
        return super(UserAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)


class GroupAdmin(extradmin.ModelAdmin, DjangoGroupAdmin):

    string_overrides = {
        'add_title': _(u'Add user group'),
        'change_title': _(u'Change user group'),
        'changelist_title': _(u'Choose user group to change'),
        'changelist_popup_title': _(u'Choose user group'),
        'changelist_addlink_title': _(u'Add user group'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d user group', '%(count)d user groups', n)
    }

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'permissions':
            kwargs['form_class'] = PermissionMultipleChoiceField
            kwargs['widget'] = PermissionSelectMultiple
            kwargs['help_text'] = u''
        return super(GroupAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_urls(self):
        return patterns('',
            url(r'^permissions/$',
                self.admin_site.admin_view(self.permissions_view),
                name='auth_group_permissions'),
        ) + super(GroupAdmin, self).get_urls()

    def permissions_view(self, request):
        form = GroupPermissionsForm(data=request.POST or None)
        if form.is_valid():
            form.save()
            self.message_user(request, _(u'Permissions was successfully saved.'))
            return redirect(request.path)
        rows = []
        for permission in form.permissions:
            model_class = permission.content_type.model_class()
            model_name_plural = model_class._meta.verbose_name_plural
            rows.append({'name': model_name_plural, 'permission': permission})
        rows.sort(key=lambda x: x['name'])
        return TemplateResponse(request,
            template = 'admin/auth/group/permissions.html',
            context = {
                'title': _(u'Groups permissions'),
                'rows': rows,
                'form': form
            },
            current_app = self.admin_site.name
        )


class SiteAdmin(extradmin.ModelAdmin, DjangoSiteAdmin):

    string_overrides = {
        'add_title': _(u'Add site'),
        'change_title': _(u'Change site'),
        'changelist_title': _(u'Choose site to change'),
        'changelist_popup_title': _(u'Choose site'),
        'changelist_addlink_title': _(u'Add site'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d site', '%(count)d sites', n)
    }


extradmin.site.register(MenuSection, MenuSectionAdmin)
extradmin.site.register(User, UserAdmin)
extradmin.site.register(Group, GroupAdmin)
extradmin.site.register(Site, SiteAdmin)
extradmin.site.dashboard.register(AppsWidget)
extradmin.site.dashboard.register(LogWidget)
