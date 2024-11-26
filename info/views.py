from datetime import datetime
import json
import pytz
import googlemaps
from collections import defaultdict
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from info.helpers.places import FourSquarePlacesHelper
from info.helpers.weather import WeatherBitHelper
from search.helpers.photo import UnplashCityPhotoHelper
from .models import CitySearchRecord, Comment, FavCityEntry
from django.core.cache import cache
from .forms import CommentForm

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import ItineraryItem
import os


@require_http_methods(["GET"])
@login_required
def map_view(request):
    """
    Render the map in the HTML
    """
    return render(request, "city_info.html")


@require_http_methods(["GET"])
@login_required
def google_maps_api(request):
    """
    Makes a request to the Google Maps API (needed to hide the API key)
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    script_url = f"https://maps.googleapis.com/maps/api/js?key={api_key}"
    return JsonResponse({"script": script_url})


@require_http_methods(["GET"])
@login_required
def drop_pin(request):
    """
    Drops a pin on a specified location and returns its details.
    """
    location = request.GET.get("location")  # Expecting a location name or address
    if not location:
        return JsonResponse({"error": "No location provided"}, status=400)

    try:
        gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
        geocode_result = gmaps.geocode(location)
        if not geocode_result:
            return JsonResponse({"error": "Location not found"}, status=404)

        lat_lng = geocode_result[0]["geometry"]["location"]
        return JsonResponse(
            {
                "location": location,
                "latitude": lat_lng["lat"],
                "longitude": lat_lng["lng"],
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required()
def addTofav(request):
    """Toggles the favorite status of a city for the logged-in user, adding it if not present
       or removing it if it already exists, and returns the action status as a JSON response."""

    city = request.GET.get("city")
    country = request.GET.get("country")
    if not city or not country:
        return JsonResponse({"data": None})
    data = "removed"
    count = FavCityEntry.objects.filter(
        city=city, country=country, user=request.user
    ).count()
    if count > 0:
        FavCityEntry.objects.filter(
            city=city, country=country, user=request.user
        ).delete()
    else:
        FavCityEntry.objects.create(
            city=city, country=country, user=request.user
        )
        data = "added"
    return JsonResponse({"data": data})


@require_http_methods(["GET"])
def place_photo(request):
    """Fetches and caches the photo link for a specific place identified by fsq_id,
       then redirects the user to that photo link."""

    photo_link = cache.get(f"photo-link-{request.GET.get('fsq_id')}")
    if not photo_link:
        photo_link = FourSquarePlacesHelper().get_place_photo(
            fsq_id=request.GET.get("fsq_id")
        )
        cache.set(f"photo-link-{request.GET.get('fsq_id')}", photo_link)
    return redirect(photo_link)


@require_http_methods(["GET", "POST"])
def info_page(request):
    """Handles GET and POST requests for city information, including weather, dining, and comments.
       Saves user comments and fetches various city-related data from caches or external APIs."""

    city = request.GET.get("city")
    country = request.GET.get("country")

    if request.method == "POST":
        commentForm = CommentForm(request.POST)

        if commentForm.is_valid():
            # save the form data to model
            form = commentForm.save(commit=False)
            form.author = request.user
            form.city = city
            form.country = country
            form.save()
    commentForm = CommentForm()
    # if (
    #     CitySearchRecord.objects.filter(city_name=city, country_name=country).count()
    #     == 0
    # ):
    CitySearchRecord.objects.create(city_name=city, country_name=country)
    weather_info = cache.get(f"{city}-weather")
    if not weather_info:
        try:
            weather_info = WeatherBitHelper().get_city_weather(
                city=city, country=country
            )["data"][0]

            weather_info["sunrise"] = (
                datetime.strptime(weather_info["sunrise"], "%H:%M")
                .astimezone(pytz.timezone(weather_info["timezone"]))
                .strftime("%I:%M")
            )
            weather_info["sunset"] = (
                datetime.strptime(weather_info["sunset"], "%H:%M")
                .astimezone(pytz.timezone(weather_info["timezone"]))
                .strftime("%I:%M")
            )
            weather_info["ts"] = datetime.fromtimestamp(
                weather_info["ts"]
            ).strftime("%m-%d-%Y, %H:%M")
            cache.set(f"{city}-weather", weather_info)
        except Exception:
            weather_info = {}
    dining_info = cache.get(f"{city}-dinning")

    if not dining_info:
        dining_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="13065",
            sort="RELEVANCE",
            limit=5,
        )
        cache.set(f"{city}-dinning", dining_info)

    airport_info = cache.get(f"{city}-airport")
    if not airport_info:
        airport_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="19040",
            sort="RELEVANCE",
            limit=5,
        )
        cache.set(f"{city}-airport", airport_info)

    outdoor_info = cache.get(f"{city}-outdoor")
    if not outdoor_info:
        outdoor_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="16000",
            sort="RELEVANCE",
            limit=5,
        )
        cache.set(f"{city}-outdoor", outdoor_info)

    arts_info = cache.get(f"{city}-arts")
    if not arts_info:
        arts_info = FourSquarePlacesHelper().get_places(
            city=f"{city}, {country}",
            categories="10000",
            sort="RELEVANCE",
            limit=5,
        )
        cache.set(f"{city}-arts", arts_info)

    photo_link = cache.get(f"{city}-photolink")
    if not photo_link:
        photo_link = UnplashCityPhotoHelper().get_city_photo(city=city)
        cache.set(f"{city}-photolink", photo_link)
    comments = Comment.objects.filter(city=city, country=country).order_by(
        "-created_on"
    )
    isInFav = (
        True
        if FavCityEntry.objects.filter(
            city=city, country=country, user=request.user
        ).count()
        > 0
        else False
    )

    itinerary_items = ItineraryItem.objects.filter(
        user=request.user, city=city
    ).values_list("spot_name", flat=True)

    return render(
        request,
        "search/city_info.html",
        context={
            "weather_info": weather_info,
            "dining_info": dining_info,
            "airport_info": airport_info,
            "outdoor_info": outdoor_info,
            "arts_info": arts_info,
            "photo_link": photo_link,
            "comments": comments,
            "commentForm": commentForm,
            "city": city,
            "country": country,
            "isInFav": isInFav,
            "itinerary_items": itinerary_items,
        },
    )


@login_required()
def profile_page(request):
    """Renders the profile page for the logged-in user, displaying their favorite cities and the most popular cities based on search records."""
    favCities = FavCityEntry.objects.filter(user=request.user)
    popularCities = (
        CitySearchRecord.objects.values("city_name")
        .annotate(city_count=Count("city_name"))
        .order_by("-city_count")[:10]
    )
    return render(
        request,
        "profile/profile.html",
        {"favCities": favCities, "popularCities": popularCities},
    )


@require_http_methods(["GET"])
@login_required
def add_to_itinerary(request, city, spot_name, address, category):
    """Adds a place to the user's itinerary if it's not already in the itinerary."""
    if not ItineraryItem.objects.filter(
        user=request.user, city=city, spot_name=spot_name
    ).exists():
        ItineraryItem.objects.create(
            user=request.user,
            city=city,
            spot_name=spot_name,
            address=address,
            category=category,
        )
        return JsonResponse(
            {"status": "success", "message": "Added to itinerary."}
        )
    


@login_required
def remove_from_itinerary(request, city, spot_name):
    """Removes a place from the user's itinerary if it exists."""
    print(city,spot_name,request)
    print(ItineraryItem.objects)
    item = ItineraryItem.objects.filter(
        user=request.user, city=city, spot_name=spot_name
    ).first()
    if item:
        item.delete()
        return JsonResponse(
            {"status": "success", "message": "Removed from itinerary."}
        )
    


@require_http_methods(["GET", "POST"])
@login_required
def itinerary_page(request):
    """Retrieves and displays the itinerary items for the specified city and user. Allows updating of scheduled dates."""
    city = request.GET.get("city")
    country = request.GET.get("country")

    if request.method == "POST":
        # Handle date updates for itinerary items
        item_id = request.POST.get('item_id')
        scheduled_on = request.POST.get('scheduled_on')
        if item_id:
            try:
                itinerary_item = ItineraryItem.objects.get(id=item_id, user=request.user)
                if scheduled_on:
                    itinerary_item.scheduled_on = scheduled_on
                else:
                    itinerary_item.scheduled_on = None  # Allow clearing the date
                itinerary_item.save()
            except ItineraryItem.DoesNotExist:
                pass  # Handle error as needed

    itinerary_items = ItineraryItem.objects.filter(
        user=request.user, city=city
    ).order_by("scheduled_on", "added_on")

    return render(
        request,
        "search/itinerary.html",
        context={
            "itinerary": itinerary_items,
            "city": city,
            "country": country,
        },
    )

@login_required
def all_itineraries_page(request):
    """
    Show all itineraries grouped by city for the logged-in user.
    """
    # Fetch all itineraries for the logged-in user
    itineraries = ItineraryItem.objects.filter(user=request.user).order_by("city", "scheduled_on")
    
    itineraries_by_city = {}
    for item in itineraries:
        if item.city not in itineraries_by_city:
            itineraries_by_city[item.city] = []
        itineraries_by_city[item.city].append(item)
    
    # Debug: Check if the data is correct
    print(itineraries_by_city)  # This will show in the server logs
    # Or return as JSON for a quick debug
    return render(
        request,
        "search/all_itineraries.html",
        context={"grouped_itineraries": itineraries_by_city},
    )