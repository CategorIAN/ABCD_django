from django import forms
from .models import Person


class newPersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "status"]
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial["status"] = "Active"
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
        self.fields["status"].widget = forms.HiddenInput()