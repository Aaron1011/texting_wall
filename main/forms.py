from django.contrib.auth.forms import UserCreationForm
from django import forms
from models import TRAFFIC_SOURCE, Wall
class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(TRAFFIC_SOURCE)

class WallForm(forms.ModelForm):
    class Meta:
        model = Wall
        widgets = {
            'sms_keyword' : forms.HiddenInput
        }
