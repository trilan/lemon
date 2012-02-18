from django.template.loader import render_to_string

from haystack import site, indexes

from .models import Page


class PageTextField(indexes.CharField):

    def prepare_template(self, object):
        return render_to_string('search/indexes/pages/page_text.txt', {
            'object': object,
        })


class PageIndex(indexes.SearchIndex):

    sites = indexes.MultiValueField()
    language = indexes.CharField(model_attr='language')
    title = indexes.CharField()
    text = PageTextField(document=True, use_template=True)
    url = indexes.CharField()

    def index_queryset(self):
        return Page.objects.published()

    def prepare_sites(self, object):
        return list(object.sites.values_list('pk', flat=True))

    def prepare_title(self, object):
        return unicode(object)

    def prepare_url(self, object):
        return object.get_absolute_url()


site.register(Page, PageIndex)
