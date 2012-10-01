# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core.context_processors import csrf
my_choice = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)

class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(my_choice)

def create_account(request):
    c = {}
    c.update(csrf(request))
    if request.POST:
        return render_to_response("finish.html", c) 
    else:
        choices = (
        ('BG', 'Blog'),
        ('FR', 'Friend'),
        ('OT', 'Other',
))
        form = UserCreation()
        return render_to_response(
    "create_account.html",
        { "form": form })
 
