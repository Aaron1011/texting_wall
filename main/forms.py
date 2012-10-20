from django.contrib.auth.forms import UserCreationForm
from django import forms
from models import TRAFFIC_SOURCE, Wall
class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(TRAFFIC_SOURCE)

class WallForm(forms.ModelForm):
    sms_keyword = forms.CharField(widget=forms.HiddenInput)
    class Meta:
        model = Wall
