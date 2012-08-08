from django.template import Library


CHANGEFREQ_VALUES = {
    'N': 'never',
    'A': 'always',
    'H': 'hourly',
    'D': 'daily',
    'W': 'weekly',
    'M': 'monthly',
    'Y': 'yearly',
}


register = Library()


@register.filter
def changefreq(value):
    return CHANGEFREQ_VALUES.get(value, 'monthly')
