from django.template import Library, Node, TemplateSyntaxError


register = Library()


class DashboardNode(Node):

    def __init__(self, admin_site, user):
        self.admin_site = admin_site
        self.user = user

    def render(self, context):
        user = self.user.resolve(context)
        admin_site = self.admin_site.resolve(context)
        return admin_site.dashboard.render(user, context)


@register.tag
def dashboard(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) != 2:
        raise TemplateSyntaxError("'dashboard' tag requires two arguments")
    return DashboardNode(parser.compile_filter(bits[0]),
                         parser.compile_filter(bits[1]))
