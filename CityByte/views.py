import os
import time
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests


class SignUpView(generic.CreateView):
    """Sign up form the creates a user; ensures certain critera is met (defined in /CityByte/settings.py)."""
    #UI changes in login
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@csrf_exempt
def sign_in(request):
    """Signs users in."""
    return render(request, "login.html")


@csrf_exempt
def auth_receiver(request):
    """Allow Google sign-ins."""
    if request.method == "POST":
        if "credential" not in request.POST:
            return JsonResponse({"error": "Missing credential"}, status=403)
        token = request.POST["credential"]

    time.sleep(
        1
    )  # delay is needed in order to ensure creation of token before retrieving user's data

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ["GOOGLE_OAUTH2_ID"]
        )
    except ValueError:
        return HttpResponse(status=403)

    email = user_data.get("email")
    first_name = user_data.get("given_name")
    last_name = user_data.get("family_name")

    # Get or create the user
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    login(request, user)
    request.session["user_data"] = user_data

    return redirect("main_page")


def sign_out(request):
    """Signs out a user by deleting their session for the particular user; function works for Google and normal signouts."""
    if "user_data" in request.session:
        del request.session["user_data"]
    logout(request)
    return redirect("sign_in")
