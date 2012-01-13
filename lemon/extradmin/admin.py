from django.conf.urls.defaults import patterns, url
from django.contrib.auth.admin import (
    GroupAdmin as DjangoGroupAdmin, UserAdmin as DjangoUserAdmin)
from django.contrib.auth.models import Group, User
from django.contrib.sites.admin import SiteAdmin as DjangoSiteAdmin
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from lemon import extradmin
from lemon.extradmin.forms import GroupPermissionsForm
from lemon.extradmin.forms import PermissionMultipleChoiceField
from lemon.extradmin.widgets import PermissionSelectMultiple


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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'user_permissions':
            kwargs['form_class'] = PermissionMultipleChoiceField
            kwargs['widget'] = PermissionSelectMultiple
            kwargs['help_text'] = u''
        return super(UserAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)


class GroupAdmin(extradmin.ModelAdmin, DjangoGroupAdmin):

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
    pass


extradmin.site.register(User, UserAdmin)
extradmin.site.register(Group, GroupAdmin)
extradmin.site.register(Site, SiteAdmin)

section = extradmin.site.menu.add_section('sites', title=_(u'Sites'))
section.add_item('sites', model=Site, title=_(u'Sites'))
section.add_item('users', model=User, title=_(u'Users'))
section.add_item('user groups', model=Group, title=_(u'User groups'))

extradmin.site.menu.add_section('content', title=_(u'Content'))
