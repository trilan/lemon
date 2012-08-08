from django.shortcuts import render
from django.utils import translation

from lemon.sitemaps.models import Item


def sitemap_xml(request):
    translation.activate('en')
    qs = Item.objects.filter(sites=request.site, enabled=True)
    return render(request, 'sitemaps/sitemap.xml',
                  {'object_list': qs}, content_type='application/xml')
