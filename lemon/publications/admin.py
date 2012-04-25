from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from lemon import extradmin


class PublicationAdmin(extradmin.ModelAdmin):

    """
    Default configuration for admin publications.
    """

    actions = ['make_enabled', 'make_disabled']
    fieldsets = (
        (_('Publication parameters'), {
            'classes': ('collapse', 'wide'),
            'fields': ('enabled',
                       'publication_start_date',
                       'publication_end_date')
        }),
    )
    date_hierarchy = 'publication_start_date'
    extend_list_display = True
    list_filter = ('enabled', 'publication_start_date')
    list_per_page = 25

    def author_name(self, obj):
        """
        Show author full name and link to author's admin change page.
        """
        url = reverse('admin:auth_user_change', args=(obj.author.pk,))
        name = obj.author.get_full_name() or obj.author.username
        return u'<a href="%s">%s</a>' % (url, name)
    author_name.short_description = _('author name')
    author_name.allow_tags = True
    author_name.admin_order_field = 'author'

    def make_enabled(self, request, queryset):
        """
        Action which set enabled field to True.
        """
        queryset.update(enabled=True)
    make_enabled.short_description = _('Enable selected %(verbose_name_plural)s')

    def make_disabled(self, request, queryset):
        """
        Action which set enabled field to False.
        """
        queryset.update(enabled=False)
    make_disabled.short_description = _('Disable selected %(verbose_name_plural)s')

    def queryset(self, request):
        """
        Join author information to default queryset.
        """
        qs = super(PublicationAdmin, self).queryset(request)
        qs = qs.select_related('author')
        return qs

    def save_model(self, request, obj, form, change):
        """
        Set publication author from request.
        """
        if not change:
            obj.author = request.user
        super(PublicationAdmin, self).save_model(request, obj, form, change)

    def get_list_display(self, request, extend=None):
        if extend is None:
            extend = self.extend_list_display
        list_display = super(PublicationAdmin, self).get_list_display(request)
        if extend:
            list_display = tuple(list_display)
            list_display += ('author_name', 'publication_start_date', 'enabled')
        return list_display
