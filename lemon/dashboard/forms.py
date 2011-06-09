from django import forms
from lemon.dashboard.models import WidgetInstance


class CreateWidgetInstanceForm(forms.ModelForm):

    class Meta:
        model = WidgetInstance
        fields = ('widget', 'column', 'position')

    def __init__(self, dashboard, user, *args, **kwargs):
        super(CreateWidgetInstanceForm, self).__init__(*args, **kwargs)
        self.dashboard = dashboard
        self.user = user

    def clean_widget(self):
        widget_label = self.cleaned_data['widget']
        if widget_label not in self.dashboard._registry:
            raise forms.ValidationError(
                u'Widget with label %r is not registered in dashboard %r' %
                (widget_label, self.dashboard.label))
        widget = self.dashboard._registry[widget_label]
        if widget not in self.dashboard.get_available_widgets(self.user):
            raise forms.ValidationError(
                u'Widget with label %r is not available for user %r '
                u'in dashboard %r' % (widget_label, self.user.username,
                                      self.dashboard.label))
        return widget_label

    def save(self, commit=True):
        instance = super(CreateWidgetInstanceForm, self).save(commit=False)
        instance.dashboard = self.dashboard.label
        instance.user = self.user
        if commit:
            instance.save()
        return instance
