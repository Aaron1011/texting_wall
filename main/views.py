# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import forms as auth_forms

from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
import forms as local_forms

def create_account(request):
    form = local_forms.UserCreation()
    if request.POST:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password1"])
            login(request,user)
            return render_to_response('finish.html')
    else:
        return render_to_response(
    "create_account.html",
        { "form": form }, RequestContext(request))
def finish(request):
    return HttpResponse("Login Successfull!")

def new_wall(request):
    if request.POST:
        pass
    else:
        form = local_forms.WallForm()
        return render_to_response(
        "create_wall.html",
            {"form": form}, RequestContext(request))
