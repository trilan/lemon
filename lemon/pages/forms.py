from django import forms
from django.contrib.sites.models import Site
from django.db.models import Count, Max
from django.utils.translation import ugettext_lazy as _

from lemon.pages.models import Page
from lemon.pages.widgets import SelectPageTemplate


class PageAdminForm(forms.ModelForm):

    template = forms.CharField(
        label = _(u'Template'),
        max_length = 255,
        widget = SelectPageTemplate(),
        error_messages = {
            'required': _(u'Please create template for pages')
        },
    )

    def is_slug_unique(self):
        qs = Site.objects.all()
        qs = qs.filter(pk__in=self.cleaned_data['sites'])
        qs = qs.filter(page__slug=self.cleaned_data['slug'])
        if self.instance and self.instance.pk:
            qs = qs.exclude(page__pk=self.instance.pk)
        qs = qs.annotate(page_count=Count('page'))
        result = qs.aggregate(page_count_max=Max('page_count'))
        return not result['page_count_max']

    def clean(self):
        data = self.cleaned_data
        if 'slug' in data and 'sites' in data and not self.is_slug_unique():
            msg = u'Page %s already exists for some of selected sites'
            raise forms.ValidationError(_(msg) % data['slug'])
        return data

    class Meta:
        model = Page
