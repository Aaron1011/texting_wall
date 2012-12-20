from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from models import TRAFFIC_SOURCE, Wall, MessageSender
import re


class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(TRAFFIC_SOURCE)


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={
        'id': 'inputEmail', 'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs=
        {'id': 'inputPassword', 'placeholder': 'Password'}
    ))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)


class WallForm(forms.ModelForm):
    def clean_hashtag(self):
        if self.cleaned_data['hashtag'][0] != u'#':
            raise forms.ValidationError("Hashtag doesn't start with #")
        return self.cleaned_data['hashtag']

    class Meta:
        model = Wall
        widgets = {
            'hashtag': forms.TextInput(attrs={
                'id': 'inputHashtag'
            })
        }
        exclude = ('phone_number',)


class UploadImageForm(forms.Form):
    name = forms.CharField()
    photo = forms.ImageField()
    claimall = forms.BooleanField(required=False, label="Clame all other messages sent using this phone number")

    def clean_name(self):
        if not re.match('[a-z A-Z]+', self.cleaned_data['name']):
            raise forms.ValidationError("Invalid name")
