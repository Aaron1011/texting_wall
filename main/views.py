# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms as auth_forms
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from forms import WallForm
import forms as local_forms
import models
from django.contrib.auth.decorators import login_required
from django_twilio.decorators import twilio_view
from django.conf import settings
from django_twilio.client import twilio_client
import random, string, re
from Pubnub import Pubnub
from django.views.decorators.csrf import csrf_exempt
from main.models import Message, MessageSender
import datetime
import tweepy

def index(request):
    if request.user.is_authenticated():
        return render_to_response("account.html", {"walls": list(request.user.wall_set.all())}, RequestContext(request))
    return render_to_response("index.html", RequestContext(request))

@login_required(login_url='/login', redirect_field_name='/create_wall')
def display_wall(request, id):
    wall = models.Wall.objects.filter(pk=id)[0]
    if not wall:
        return render_to_response("404.html")
    return render_to_response("wall.html", {'wall': wall})

def twitter_oauth(request):
    print settings.OAUTH_CALLBACK
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, settings.OAUTH_CALLBACK)
    if request.session.has_key('request_token'):
        token = request.session['request_token']
        del request.session['request_token']
        auth.set_request_token(token[0], token[1])
        verifier = request.GET['oauth_verifier']
        auth.get_access_token(verifier)

        api = tweepy.API(auth)
        user = api.me()

        sender = MessageSender()
        sender.name = user.name
        sender.twitter_username = user.screen_name
        sender.image_url = user.profile_image_url
        sender.save()

        for message in Message.objects.filter(twitter_account=sender.twitter_username):
            message.sender = sender
            message.save()

        if request.session.has_key('message_page'):
            return HttpResponseRedirect(request.session['message_page'])
        return HttpResponseRedirect('/')
    print settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, settings.OAUTH_CALLBACK
    auth_url = auth.get_authorization_url()
    request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    return HttpResponseRedirect(auth_url)

@twilio_view
def sms_message(request):
    PUBLISH_KEY = "pub-8a8223f4-631c-4484-a118-2b01232307cc"
    SUBSCRIBE_KEY = "sub-e754ed6b-133d-11e2-91f2-b58e6c804094"
    SECRET = "sec-ZjcxZGVjNDAtZWQyMC00MGZmLTg1Y2MtNmJkNGE3YTJiYjlj"

    twilio_message = request.POST['Body']
    phone_number = request.POST['From']
    incoming_phone_number = request.POST['To']

    hashtag, body = _split_message(twilio_message, incoming_phone_number)
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
    return HttpResponse("Error")

def _get_phone_number():
    if settings.DEBUG:
        return "6176005993"
    return "6176005993" # Will be removed when deployed to other companies
    numbers = []
    for num in twilio_client.phone_numbers.iter():
        numbers.append(num)
    for wall in models.Wall.objects.all():
        try:
            numbers.remove(wall.phone_number)
        except ValueError:
            pass
    return numbers[0]

def _split_message(message, phone_number):
    walls = models.Wall.objects.all()
    if len(walls) == 1:
        hashtag = str(walls[0].hashtag)
        return hashtag, message
    try:
        wall = models.Wall.objects.get(phone_number=phone_number)
    except models.Wall.DoesNotExist:
        return None, None
    return wall.hashtag, message

def _purchase_phone_number():
    for area in settings.AREA_CODES:
        numbers = twilio_client.phone_numbers.search(area_code=area)
        if numbers:
            numbers[0].purchase()
            break
    numbers[0].update(sms_method='POST', sms_url=build_absolute_uri('/recieve_sms'))
    return numbers[0]

def _generateMessages(wall):
    for message in wall.message_set.all():
        yield message.message, message.time_sent, message.twitter_account, message.phone_number

def display_messages(request, name):
    wall = models.Wall.objects.filter(hashtag="#" + name.strip('/'))
    if wall:
        request.session['message_page'] = request.get_full_path()
        return render_to_response("messages.html", {"messages": wall[0].message_set.all(), 'user': request.user}, RequestContext(request))
    return render_to_response("404.html", RequestContext(request))

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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

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
            print f.errors
            return render_to_response(
            "create_wall.html",
                {"form": f, "phone_number": f.data['phone_number']}, RequestContext(request))

    phone_number = _get_phone_number()
    #if not phone_number:
        #phone_number = _purchase_phone_number()
    print "Phone number: " + phone_number
    form = WallForm(data={'phone_number': phone_number})
    return render_to_response(
    "create_wall.html",
        {"form": form, "phone_number": phone_number}, RequestContext(request))
