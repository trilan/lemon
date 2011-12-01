from django.utils.translation import ugettext_lazy as _
from lemon.dashboard.base import Widget


class TextWidget(Widget):

    title = _(u'Text')
    description = _(u"This is a generic description for text widget.")
    backbone_view_name = u'TextWidget'
    text = _(
        u'<p>This is a generic text for this widget. '
        u'Replace it with yours.</p>')

    def to_raw(self):
        data = super(TextWidget, self).to_raw()
        data['text'] = unicode(self.text)
        return data
