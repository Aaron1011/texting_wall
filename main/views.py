# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect
my_choice = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)

class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(my_choice)

def create_account(request):
    c = {}
    form = UserCreation()
    if request.POST:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('finish.html')
        return render_to_response('finish.html') # This will be changed to some
#sort of error page
    else:
        choices = (
        ('BG', 'Blog'),
        ('FR', 'Friend'),
        ('OT', 'Other',
))
        
        
        return render_to_response(
    "create_account.html",
        { "form": form }, RequestContext(request))
 
