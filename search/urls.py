from django.urls import path
from .views import city_suggestions, city_photo
from . import views
urlpatterns = [
    path("city", city_suggestions, name="city_search"),  # Returns city suggestions based on user input.
    path("city/photo", city_photo, name="city_photo") , # Fetches a photo of the specified city.
    path('locate-me/', views.locate_me, name='locate_me')
]
