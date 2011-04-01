from django.shortcuts import render

from lemon.robots.models import File
from lemon.utils.shortcuts import get_object_or_none


def robots_txt(request):
    qs = File.objects.filter(site=request.site)
    return render(request, 'robots/robots.txt',
                  {'object': get_object_or_none(qs)},
                  content_type='text/plain')
