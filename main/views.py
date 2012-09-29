# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm

def create_account(request):
    form = UserCreationForm()
    return render_to_response(
        "create_account.html",
        { "form": form })

