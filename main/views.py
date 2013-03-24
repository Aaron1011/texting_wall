# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from forms import WallForm
import forms as local_forms
import models
from django.contrib.auth.decorators import login_required
from django_twilio.decorators import twilio_view
from django.conf import settings
from django_twilio.client import twilio_client
from Pubnub import Pubnub
from main.models import Message, MessageSender, Wall
from django.utils.timezone import utc
import tweepy
import json
import datetime
from PIL import Image
import StringIO
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt


def index(request):
    if request.user.is_authenticated():
        return render_to_response("account.html", {"walls": list(request.user.wall_set.all())}, RequestContext(request))
    return render_to_response("index.html", RequestContext(request))


@login_required(login_url=reverse_lazy('django.contrib.auth.views.login'))
def display_wall(request, id):
    wall = get_object_or_404(models.Wall, pk=id)
    return render_to_response("wall.html", {'wall': wall, 'messages': [str(m.message) for m in wall.message_set.all()],
                                            "PUBNUB_PUBLISH_KEY" : settings.PUBNUB_PUBLISH_KEY,
                                            "PUBNUB_SUBSCRIBE_KEY" : settings.PUBNUB_SUBSCRIBE_KEY,
                                            "PUBNUB_SECRET": settings.PUBNUB_SECRET
                              })


def twitter_oauth(request, id=None):
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    if 'request_token' in request.session:
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

        wall = Wall.objects.get(pk=request.session['wall_id'])
        message = Message.objects.get(pk=request.session['message_id'])
        message.sender = sender
        message.wall = wall
        message.save()

        if request.session['claimall']:
            for message in wall.message_set.filter(twitter_account=sender.twitter_username):
                message.sender = sender
                message.wall = wall
                message.save()

        if 'message_page' in request.session:
            return HttpResponseRedirect(request.session['message_page'])
        return HttpResponseRedirect(reverse('main.views.index'))
    auth_url = auth.get_authorization_url()
    request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    request.session['wall_id'] = id
    request.session['claimall'] = json.loads(request.GET.get('claimall'))
    request.session['message_id'] = request.GET.get('message')
    request.session.modified = True
    return HttpResponseRedirect(auth_url)


@twilio_view
def sms_message(request):
    twilio_message = request.POST['Body']
    phone_number = request.POST['From']
    incoming_phone_number = request.POST['To']

    hashtag, body = _split_message(twilio_message, incoming_phone_number)
    print hashtag, body
    if hashtag is not None and body is not None:
        message = models.Message()
        message.message = body
        message.phone_number = phone_number
        message.wall = models.Wall.objects.get(hashtag=hashtag)
        message.save()
        print message

        pubnub = Pubnub(settings.PUBNUB_PUBLISH_KEY, settings.PUBNUB_SUBSCRIBE_KEY, settings.PUBNUB_SECRET, False)
        print pubnub.publish({
            'channel': hashtag,
            'message': {
                'message': body
            }
        })
        return HttpResponse("Success!")
    return HttpResponse("Error")

def _get_phone_number():
    if settings.DEBUG:
        return "+16176005993"
    return "+16176005993"  # Will be removed when deployed to other companies

    return [num for num in twilio_client.phone_numbers.list() if not Wall.objects.filter(phone_number__exact=num)]


def _split_message(message, phone_number):
    walls = models.Wall.objects.all()
    if len(walls) == 1:
        hashtag = str(walls[0].hashtag)
        return hashtag, message
    try:
        wall = models.Wall.objects.get(phone_number=phone_number)
    except models.Wall.DoesNotExist:
        return None, None
    if datetime.datetime.now(utc) - datetime.timedelta(minutes=settings.WALL_EXPIRATION) > wall.last_ping:
        return wall.hashtag, message
    return None, None


def _purchase_phone_number(request):
    for area in settings.AREA_CODES:
        numbers = twilio_client.phone_numbers.search(area_code=area)
        if numbers:
            numbers[0].purchase()
            break
    numbers[0].update(sms_method='POST', sms_url=reverse('main.views.sms_message'))
    return numbers[0]


def _generateMessages(wall):
    for message in wall.message_set.all():
        yield message.message, message.time_sent, message.twitter_account, message.phone_number


def display_messages(request, name):
    wall = models.Wall.objects.filter(hashtag="#" + name.strip('/'))
    form = local_forms.UploadImageForm()
    if wall:
        print request.get_full_path()
        request.session['message_page'] = request.get_full_path()
        return render_to_response("messages.html", {"messages": wall[0].message_set.all(), 'user': request.user, 'form': form}, RequestContext(request))
    return render_to_response("404.html", RequestContext(request))


def create_account(request):
    form = local_forms.UserCreation()
    if request.POST:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            auth_login(request, user)
            return HttpResponseRedirect(reverse('main.views.index'))
        return render_to_response(
            "create_account.html", {"form": form}, RequestContext(request))
    else:
        return render_to_response(
            "create_account.html",
            {"form": form}, RequestContext(request))


def finish(request):
    return HttpResponse("Login Successfull!")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main.views.index'))


@login_required(login_url=reverse_lazy('django.contrib.auth.views.login',
    kwargs={'template_name': 'login.html'}))
def new_wall(request):
    if request.POST:
        f = WallForm(data=request.POST)
        if f.is_valid():
            wallform = f.save(commit=False)
            wallform.user = request.user
            wallform.phone_number = f.data['phone_number']
            wallform.save()
            return HttpResponseRedirect(reverse('main.views.display_wall',
                args=[wallform.id]))
        else:
            print f.errors
            return render_to_response(
                "create_wall.html",
                {"form": f, "phone_number": f.data['phone_number']}, RequestContext(request))

    phone_number = _get_phone_number()
    #if not phone_number:
        #phone_number = _purchase_phone_number(request)
    print "Phone number: " + phone_number
    form = WallForm(data={'phone_number': phone_number})
    return render_to_response(
        "create_wall.html",
        {"form": form, "phone_number": phone_number}, RequestContext(request))


def _handle_uploaded_photo(photo):
    D = settings.USER_THUMB_DIM
    photo2 = Image.open(photo)
    photo2.thumbnail((D, D), Image.ANTIALIAS)
    back = Image.new("RGB", (D, D))
    if float(photo2.size[0]) / photo2.size[1] > 1:
        corner = (0, (back.size[1] - photo2.size[1]) / 2)
    else:
        corner = ((back.size[0] - photo2.size[0]) / 2, 0)
    back.paste(photo2, corner)
    thumb_io = StringIO.StringIO()
    back.save(thumb_io, format="PNG")

    return ContentFile(thumb_io.getvalue())


def create_sms_sender(request):
    message = Message.objects.get(pk=request.POST['id'])
    imageform = local_forms.UploadImageForm(request.POST, request.FILES)
    if imageform.is_valid():
        if message.phone_number == "+1" + request.POST['areacode'] + request.POST['first'] + request.POST['second']:
            photo = request.FILES.get('photo')
            sender = MessageSender()
            sender.phone_number = message.phone_number
            sender.name = imageform.cleaned_data['name']
            if photo:
                photoname = photo.name.split('.')[0]
                resizedphoto = _handle_uploaded_photo(photo)
                sender.image.save(photoname + '.png', resizedphoto)
            sender.save()

            message.sender = sender
            message.save()

            if imageform.cleaned_data['claimall']:
                for othermessage in Message.objects.get(phone_number=message.phone_number):
                    othermessage.sender = sender
                    othermessage.save()
    print imageform.errors
    return HttpResponseRedirect(reverse('main.views.display_messages',
        args=[Message.objects.get(pk=request.POST['id']).wall.hashtag.strip("#")]))
def json_response(f):
    def func(*args, **kwargs):
        status_code = 200
        response = f(*args, **kwargs)

        body = json.dumps(response)
        if 'callback' in args[0].GET:
            body = '%s(%s)' % (args[0].GET['callback'], body)

        return HttpResponse(body, status=status_code)
    return func

@json_response
@csrf_exempt
def verify_sms(request):
    try:
        message = Message.objects.get(pk=request.GET['message_id'])
    except Message.DoesNotExist:
        return {'status': False}

    print message.phone_number
    print request.GET['phone_number']
    if message.phone_number == request.GET['phone_number']:
        return {'status': True}

    return {'status': False}


@csrf_exempt
def close_wall(request):
    wall = Wall.objects.get(pk=request.GET['id'])
    print "Closing wall"
    wall.last_ping -= datetime.timedelta(minutes=settings.WALL_EXPIRATION)
    print wall.last_ping
    wall.save()


@csrf_exempt
@json_response
def ping_wall(request):
    wall = Wall.objects.get(pk=request.GET['id'])
    wall.lastping = datetime.datetime.now(utc)
    print wall.lastping
    wall.save()



