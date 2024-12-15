from django import forms
from .models import Person, FormRequests
import datetime


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

class FormRequestForm(forms.ModelForm):
    class Meta:
        model = FormRequests
        fields = "__all__"

    timestamp = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial["form"] = "ABCD General Survey"
        initial["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d")
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)


