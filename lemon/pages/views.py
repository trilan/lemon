from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_protect

from lemon.pages.models import Page


@csrf_protect
def page(request, url_path):
    qs = Page.objects.published().filter(sites=request.site, language=get_language)
    page = get_object_or_404(qs, url_path=url_path)
    return render(request, 'pages/%s' % page.template, {'page': page})
