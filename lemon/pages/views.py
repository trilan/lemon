from django.template import RequestContext
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

from lemon.pages.models import Page


@csrf_protect
def page(request, slug):
    qs = Page.objects.published().filter(site=request.site)
    page = get_object_or_404(qs, slug=slug)
    return render(request, 'pages/%s' % page.template, {'page': page})
