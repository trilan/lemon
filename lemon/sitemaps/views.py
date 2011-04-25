from django.shortcuts import render
from django.utils.translation import get_language

from lemon.sitemaps.models import Item


def sitemap_xml(request):
    qs = Item.objects.filter(sites=request.site, enabled=True, language=get_language())
    return render(request, 'sitemaps/sitemap.xml',
                  {'object_list': qs}, content_type='application/xml')
