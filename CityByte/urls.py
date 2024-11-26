from django.contrib import admin
from django.urls import path, include
from search.views import main_page
from info.views import info_page, profile_page, addTofav
from .views import SignUpView
from . import views

urlpatterns = [
    path("", main_page, name="main_page"),  # URL for the home page
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # URL for managing accounts; provides account registration (non-Google)
    path(
        "accounts/signup/", SignUpView.as_view(), name="signup"
    ),  # URL for handling new account registrations
    path(
        "accounts/login/", views.sign_in, name="sign_in"
    ),  # URL for logging in accounts (non-Google)
    path(
        "sign-out/", views.sign_out, name="sign_out"
    ),  # URL for signing out accounts
    path(
        "auth-receiver", views.auth_receiver, name="auth_receiver"
    ),  # URL for authorizing Google accounts
    path(
        "profile/", profile_page, name="profile_page"
    ),  # URL for the signed-in user's profile
    path(
        "city", info_page, name="info_page"
    ),  # URL for viewing the a given city
    path("admin/", admin.site.urls),  # URL for admin access to the website
    path(
        "api/search/", include(("search.urls", "search"), namespace="search")
    ),  # URL for searching for a city
    path(
        "api/info/", include(("info.urls", "info"), namespace="info")
    ),  # URL for getting info on a city
    path(
        "api/addToFav/", addTofav, name="addToFav"
    ),  # URL for adding a city to a user's favorites
    path("info/", include("info.urls")),  # URL to allow access to info URLs

    path('admin/', admin.site.urls),
    path('search/', include('search.urls')),
]
