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
from django.views.decorators.csrf import csrf_exempt
import random, string, re
from Pubnub import Pubnub
@login_required(login_url='/login', redirect_field_name='/create_wall') 
def display_wall(request, id):
    wall = models.Wall.objects.get(pk=id)
    print str(wall.sms_keyword)
    return render_to_response("wall.html", {'wall': wall})

@csrf_exempt
def sms_message(request):
    PUBLISH_KEY = "pub-8a8223f4-631c-4484-a118-2b01232307cc"
    SUBSCRIBE_KEY = "sub-e754ed6b-133d-11e2-91f2-b58e6c804094"
    SECRET = "sec-ZjcxZGVjNDAtZWQyMC00MGZmLTg1Y2MtNmJkNGE3YTJiYjlj"
    message = request.POST['Body']
    sms_codes, message = _split_message(message)
    if sms_codes != None and message != None:
        pubnub = Pubnub(PUBLISH_KEY, SUBSCRIBE_KEY, SECRET, False)
        info = pubnub.publish({
            'channel' : sms_code,
            'message' : {
                'message' : message
            }
        })
        print matched_message.groups()

def _split_message(message):
    wall = models.Wall.objects.all()
    if len(wall) == 1:
        keyword = str(wall[0].sms_keyword)
        message = message.replace(keyword, '').replace('  ', ' ')
        return keyword, message
    codes = re.search("(^|\s)(\w{3})(\s|$)", message)
    if codes == None:
        return None, None
    valid = True
    for keyword in codes.groups():
        try:
            models.Wall.objects.get(sms_keyword=keyword)
        except models.Wall.DoesNotExist:
            valid = False
        else:
            valid = True
            break
    if valid == False:
        return None, None
    message = message.replace(keyword, '').replace('  ', ' ')
    return keyword, message.strip()

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

@login_required(login_url="/login", redirect_field_name='/create_wall/' )
def new_wall(request):
    if request.POST:
        f = WallForm(data=request.POST)
        if f.is_valid():
            wallform = f.save(commit=False)
            wallform.user = request.user
            wallform.save()
            return HttpResponseRedirect('/wall/' + str(wallform.id))
        else:
            return render_to_response(
            "create_wall.html",
                {"form": f, "sms_keyword": f.data['sms_keyword']}, RequestContext(request))

    keyword = "".join(random.choice(string.lowercase) for i in range(1,4))
    form = WallForm(data={'sms_keyword': keyword})
    return render_to_response(
    "create_wall.html",
        {"form": form, "sms_keyword": keyword}, RequestContext(request))
