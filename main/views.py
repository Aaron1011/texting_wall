# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
my_choice = (
    ('BG', 'Blog'),
    ('FR', 'Friend'),
    ('OT', 'Other',)
)

class UserCreation(UserCreationForm):
    about_textwall = forms.ChoiceField(my_choice)

def create_account(request):
    form = UserCreation()
    if request.POST:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.clean_username()
            form.clean_password2()
            form.save()
            user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password1"])
            login(request,user)
            return render_to_response('finish.html')
    else:
        choices = (
        ('BG', 'Blog'),
        ('FR', 'Friend'),
        ('OT', 'Other',
))
        
        
        return render_to_response(
    "create_account.html",
        { "form": form }, RequestContext(request))
        
 			
def finish(request):
	return HttpResponse("Login Successfull!")
