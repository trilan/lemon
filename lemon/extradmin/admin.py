from django.contrib import admin
from django.contrib.auth.admin import User, UserAdmin, Group, GroupAdmin
from django.contrib.sites.admin import Site, SiteAdmin
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from lemon import extradmin
from lemon.extradmin.dashboard import AppsWidget, LogWidget
from lemon.extradmin.forms import MenuItemForm
from lemon.extradmin.forms import contenttype_inlineformset_factory
from lemon.extradmin.models import MenuSection, MenuItem


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


class UserExtrAdmin(extradmin.ModelAdmin, UserAdmin):

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


class GroupExtrAdmin(extradmin.ModelAdmin, GroupAdmin):

    string_overrides = {
        'add_title': _(u'Add user group'),
        'change_title': _(u'Change user group'),
        'changelist_title': _(u'Choose user group to change'),
        'changelist_popup_title': _(u'Choose user group'),
        'changelist_addlink_title': _(u'Add user group'),
        'changelist_paginator_description': lambda n: \
            ungettext('%(count)d user group', '%(count)d user groups', n)
    }


class SiteExtrAdmin(extradmin.ModelAdmin, SiteAdmin):

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
extradmin.site.register(User, UserExtrAdmin)
extradmin.site.register(Group, GroupExtrAdmin)
extradmin.site.register(Site, SiteExtrAdmin)
extradmin.site.dashboard.register(AppsWidget)
extradmin.site.dashboard.register(LogWidget)
