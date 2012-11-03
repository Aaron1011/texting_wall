from django.contrib.auth.forms import UserCreationForm
from django import forms
from models import TRAFFIC_SOURCE, Wall
class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(TRAFFIC_SOURCE)

class WallForm(forms.ModelForm):
    def clean_hashtag(self):
        if self.cleaned_data['hashtag'][0] != u'#':
            print "Whoops!"
            raise forms.ValidationError("Hashtag doesn't start with #")
    class Meta:
        model = Wall
        widgets = {
            'sms_keyword' : forms.HiddenInput
        }
