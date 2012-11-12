# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms as auth_forms
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from forms import WallForm
import forms as local_forms
import models
from django.contrib.auth.decorators import login_required
from django_twilio.decorators import twilio_view
import random, string, re
from Pubnub import Pubnub

def index(request):
    return render_to_response("index.html", RequestContext(request))
@login_required(login_url='/login', redirect_field_name='/create_wall') 
def display_wall(request, id):
    wall = models.Wall.objects.get(pk=id)
    return render_to_response("wall.html", {'wall': wall})

@twilio_view
def sms_message(request):
    PUBLISH_KEY = "pub-8a8223f4-631c-4484-a118-2b01232307cc"
    SUBSCRIBE_KEY = "sub-e754ed6b-133d-11e2-91f2-b58e6c804094"
    SECRET = "sec-ZjcxZGVjNDAtZWQyMC00MGZmLTg1Y2MtNmJkNGE3YTJiYjlj"

    twilio_message = request.POST['Body']
    phone_number = request.POST['From']

    hashtag, body = _split_message(twilio_message)
    print hashtag, body
    if hashtag != None and body != None:
        message = models.Message()
        message.message = body
        message.phone_number = phone_number
        message.wall = models.Wall.objects.get(hashtag=hashtag)
        message.save()

        pubnub = Pubnub(PUBLISH_KEY, SUBSCRIBE_KEY, SECRET, False)
        info = pubnub.publish({
            'channel' : hashtag,
            'message' : {
                'message' : body
            }
        })
        print info
        return HttpResponse("Success!")

def _split_message(message):
    wall = models.Wall.objects.all()
    if len(wall) == 1:
        hashtag = str(wall[0].hashtag)
        return hashtag, message

def create_account(request):
    form = local_forms.UserCreation()
    if request.POST:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password1"])
            auth_login(request,user)
            return render_to_response('finish.html')
        return render_to_response(
            "create_account.html",
                { "form": form }, RequestContext(request))
    else:
        return render_to_response(
    "create_account.html",
        { "form": form }, RequestContext(request))
def finish(request):
    return HttpResponse("Login Successfull!")

def _get_phone_number():
    # This will get an available phone number from Twilio
    return "6176005993"

@login_required(login_url="/login", redirect_field_name='/create_wall/' )
def new_wall(request):
    if request.POST:
        f = WallForm(data=request.POST)
        if f.is_valid():
            wallform = f.save(commit=False)
            wallform.user = request.user
            wallform.phone_number = f.data['phone_number']
            wallform.save()
            return HttpResponseRedirect('/wall/' + str(wallform.id))
        else:
            print dir(f)
            return render_to_response(
            "create_wall.html",
                {"form": f, "phone_number": f.data['phone_number']}, RequestContext(request))

    phone_number = _get_phone_number() 
    form = WallForm(data={'phone_number': phone_number})
    return render_to_response(
    "create_wall.html",
        {"form": form, "phone_number": phone_number}, RequestContext(request))
