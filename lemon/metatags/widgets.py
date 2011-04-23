from django import forms


class AdminSmallTextareaWidget(forms.Textarea):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vSmallTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminSmallTextareaWidget, self).__init__(attrs=final_attrs)
