from django import forms
from .models import Person, FormRequests, Invitation, Event
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

    person = forms.ModelChoiceField(queryset=Person.objects.all().order_by("name"), label="")

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial["form"] = "ABCD General Survey"
        initial["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d")
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

class SimpleEventForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all().order_by("-eventid"), label="")

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ["event", "timestamp", "person", "plus_ones", "result"]

    person = forms.ModelChoiceField(queryset=Person.objects.all().order_by("name"), label="")

    timestamp = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateTimeInput(attrs={'type': 'date'})
    )

    result = forms.ChoiceField(
        choices = [("", "--------")] + [(x, x) for x in ['Going', 'Flaked', 'To Redeem']]
    )

    plus_ones = forms.IntegerField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["event"].widget = forms.HiddenInput()
        self.fields["timestamp"].widget = forms.HiddenInput()


