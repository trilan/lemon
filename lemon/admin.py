from django.contrib.auth.admin import User, UserAdmin, Group, GroupAdmin
from django.contrib.sites.admin import Site, SiteAdmin
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from .options import TabularInline, ModelAdmin
from .sites import site
from .forms import UserChangeForm, MenuItemForm
from .forms import contenttype_inlineformset_factory
from .models import MenuSection, MenuItem


class MenuItemInline(TabularInline):

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


class MenuSectionAdmin(ModelAdmin):

    string_overrides = {
        'add_title': _(u'Add menu section'),
        'change_title': _(u'Change menu section'),
        'changelist_title': _(u'Choose menu section to change'),
        'changelist_popup_title': _(u'Choose menu section'),
        'changelist_addlink_title': _(u'Add menu section'),
        'changelist_paginator_description': lambda n: ungettext(
            '%(count)d menu section',
            '%(count)d menu sections',
            n,
        ),
    }
    tabs = True
    inlines = [MenuItemInline]


class UserExtrAdmin(ModelAdmin, UserAdmin):

    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
            'description': _(
                u"First, enter a username and password. "
                u"Then, you'll be able to edit more user options.")}
        ),
    )
    form = UserChangeForm
    string_overrides = {
        'add_title': _(u'Add user'),
        'change_title': _(u'Change user'),
        'changelist_title': _(u'Choose user to change'),
        'changelist_popup_title': _(u'Choose user'),
        'changelist_addlink_title': _(u'Add user'),
        'changelist_paginator_description': lambda n: ungettext(
            '%(count)d user',
            '%(count)d users',
            n,
        ),
    }


class GroupExtrAdmin(ModelAdmin, GroupAdmin):

    string_overrides = {
        'add_title': _(u'Add user group'),
        'change_title': _(u'Change user group'),
        'changelist_title': _(u'Choose user group to change'),
        'changelist_popup_title': _(u'Choose user group'),
        'changelist_addlink_title': _(u'Add user group'),
        'changelist_paginator_description': lambda n: ungettext(
            '%(count)d user group',
            '%(count)d user groups',
            n,
        ),
    }


class SiteExtrAdmin(ModelAdmin, SiteAdmin):

    string_overrides = {
        'add_title': _(u'Add site'),
        'change_title': _(u'Change site'),
        'changelist_title': _(u'Choose site to change'),
        'changelist_popup_title': _(u'Choose site'),
        'changelist_addlink_title': _(u'Add site'),
        'changelist_paginator_description': lambda n: ungettext(
            '%(count)d site',
            '%(count)d sites',
            n,
        ),
    }


site.register(MenuSection, MenuSectionAdmin)
site.register(User, UserExtrAdmin)
site.register(Group, GroupExtrAdmin)
site.register(Site, SiteExtrAdmin)
