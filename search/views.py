from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from search.helpers.autocomplete import GenericDBSearchAutoCompleteHelper
from search.helpers.photo import UnplashCityPhotoHelper
from search.utils.search import AmadeusCitySearch
from search.utils.url import URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


@login_required
@require_http_methods(["GET"])
def main_page(request):
    """
    Loads the home page
    """
    user_count = get_user_model().objects.all().count()

    return render(request, "search/search.html", context={"request": request, "userCount": user_count})


@require_http_methods(["GET"])
def city_suggestions(request):
    """
    Retrieves a list of suggested cities if multiple meet the criteria
    """
    suggestions_data = GenericDBSearchAutoCompleteHelper(
        klass=AmadeusCitySearch, url=URL(**settings.AMADEUS_CONFIG)
    ).get_suggestions(city=request.GET.get("q"), max=10)

    return JsonResponse({"results": suggestions_data.get("data", [])})


@require_http_methods(["GET"])
def city_photo(request):
    """
    Retrieves the photo for a city
    """
    photo_link = UnplashCityPhotoHelper().get_city_photo(city=request.GET.get("q"))
    return JsonResponse({"path": photo_link})


def locate_me(request):
    """
    Retrieves location of user as a pin on map
    """
    google_maps_api_key = settings.YOUR_GOOGLE_MAPS_API_KEY  # Replace with your API Key
    return render(request, 'search/locate_me.html', {'google_maps_api_key': google_maps_api_key})