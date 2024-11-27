import pytz

from urllib import request
from django.test import TestCase, Client
from info.helpers.places import *
from django.shortcuts import render
from info.helpers.weather import WeatherBitHelper
from info.helpers.places import FourSquarePlacesHelper
from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from search.helpers.photo import UnplashCityPhotoHelper
from urllib.request import urlopen
from unittest.mock import MagicMock, patch
from info.models import FavCityEntry
from search.helpers.photo import UnplashCityPhotoHelper
from urllib.request import urlopen
from info.models import ItineraryItem
from django.utils import timezone

from search.utils.search import AmadeusCitySearch, GeoDB  # Added import for timezone

image_formats = ("image/png", "image/jpeg", "image/gif")

### There are four tests commented out - all of them work but are commented out for various reasons

### These tests do work, but they are commented out because I didn't want to put
### an API key connected to a credit car in GitHub
# class DropPinViewTests(TestCase):
#     """
#     Tests for map functionality (specifically dropping a pin)
#     """
#     def setUp(self):
#         """
#         Setup for tests in this class
#         """
#         self.user = get_user_model().objects.create_user(username="test_user", password="test_password",)        
#         self.client = Client()
#         self.client.login(username='test_user', password='test_password')

#     @patch('googlemaps.Client.geocode')
#     def test_drop_pin_valid_location(self, mock_geocode):
#         """
#         Mock the geocode response for Raleigh, NC
#         """
#         mock_geocode.return_value = [{
#             'geometry': {
#                 'location': {
#                     'lat': 35.7796,
#                     'lng': -78.6382
#                 }
#             }
#         }]

#         response = self.client.get(reverse('drop_pin'), {'location': 'Raleigh, NC'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {
#             'location': 'Raleigh, NC',
#             'latitude': 35.7796,
#             'longitude': -78.6382,
#         })

#     @patch('googlemaps.Client.geocode')
#     def test_drop_pin_invalid_location(self, mock_geocode):
#         """
#         Tests for an invalid location and the relevant error handling
#         """
#         mock_geocode.return_value = []

#         response = self.client.get(reverse('drop_pin'), {'location': 'Nowhere'})
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json(), {'error': 'Location not found'})

#     def test_drop_pin_no_location(self):
#         """
#         Tests for dropping a pin with no location
#         """
#         response = self.client.get(reverse('drop_pin'))
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {'error': 'No location provided'})

#     @patch('googlemaps.Client.geocode')
#     def test_drop_pin_exception_handling(self, mock_geocode):
#         """
#         Tests for an API error and handling the error
#         """
#         mock_geocode.side_effect = Exception("API error")

#         response = self.client.get(reverse('drop_pin'), {'location': 'Somewhere'})
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(response.json(), {'error': 'API error'})

class CityByte_testcase(TestCase):
    """
    Class that tests general CityByte functionality
    """
    def setUp(self):
        """
        Setup for tests in this class
        """
        get_user_model().objects.create_user("admin", "admin.@simpson.net", "admin")

    def test_main_page(self):
        """
        Tests that the main page is reachable
        """
        assert render(request, "search/search.html").status_code == 200

    def test_cityphoto(self):
        """
        Tests that an image is returned after getting a city
        """
        with patch('search.helpers.photo.UnplashCityPhotoHelper.get_city_photo') as mock_get_city_photo:
            mock_get_city_photo.return_value = "https://example.com/photo.jpg"
            photo_link = UnplashCityPhotoHelper().get_city_photo(city="Pune")
            assert photo_link is not None

    def test_photo(self):
        """
        Tests that a specific photo is retrieved
        """
        with patch('info.helpers.places.FourSquarePlacesHelper.get_place_photo') as mock_get_place_photo:
            mock_get_place_photo.return_value = "https://example.com/photo.jpg"
            photo_link = FourSquarePlacesHelper().get_place_photo(city="Pune")
            assert photo_link is not None


    # This test works, however due to the limit on weather API key usage it is commented out
    # def test_weather_info(self):
    #     """
    #     Tests that weather information can be retrieved
    #     """
    #     city = "New York City"
    #     country = "US"

    #     try:
    #         print(WeatherBitHelper().get_city_weather(city=city, country=country))
    #         weather_info = WeatherBitHelper().get_city_weather(city=city, country=country)["data"][0]
    #         weather_info["sunrise"] = (
    #             datetime.strptime(weather_info["sunrise"], "%H:%M")
    #             .astimezone(pytz.timezone(weather_info["timezone"]))
    #             .strftime("%I:%M")
    #         )
    #         weather_info["sunset"] = (
    #             datetime.strptime(weather_info["sunset"], "%H:%M")
    #             .astimezone(pytz.timezone(weather_info["timezone"]))
    #             .strftime("%I:%M")
    #         )
    #         weather_info["ts"] = datetime.fromtimestamp(weather_info["ts"]).strftime("%m-%d-%Y, %H:%M")

    #         assert weather_info is not None  # Ensure we got weather info

    #     except Exception:
    #         self.fail("Weather API call failed or returned no data.")

    @patch('info.helpers.places.FourSquarePlacesHelper.get_places')
    def test_dining_info(self, mock_get_places):
        mock_get_places.return_value = [
            {"name": "Restaurant A", "address": "Address A"},
            {"name": "Restaurant B", "address": "Address B"},
        ]
        dining_info = FourSquarePlacesHelper().get_places(city="New York", categories="13065", limit=5)
        assert len(dining_info) == 2
        assert dining_info[0]["name"] == "Restaurant A"

    @patch('info.helpers.places.FourSquarePlacesHelper.get_places')
    def test_outdoor_info(self, mock_get_places):
        """
        Tests that outdoor activities information can be retrieved
        """
        mock_get_places.return_value = [
            {"name": "Outdoor A", "address": "Address A"},
            {"name": "Outdoor B", "address": "Address B"},
        ]
        outdoor_info = FourSquarePlacesHelper().get_places(city="New York", categories="13065", limit=5)
        assert len(outdoor_info) == 2
        assert outdoor_info[0]["name"] == "Outdoor A"

    @patch('info.helpers.places.FourSquarePlacesHelper.get_places')
    def test_airport_info(self, mock_get_places):
        mock_get_places.return_value = [
            {"name": "Airport A", "address": "Address A"},
            {"name": "Airport B", "address": "Address B"},
        ]
        airport_info = FourSquarePlacesHelper().get_places(city="New York", categories="19040", limit=5)
        assert len(airport_info) == 2
        assert airport_info[0]["name"] == "Airport A"

    @patch('info.helpers.places.FourSquarePlacesHelper.get_places')
    def test_arts_info(self, mock_get_places):
        mock_get_places.return_value = [
            {"name": "Arts A", "address": "Address A"},
            {"name": "Arts B", "address": "Address B"},
        ]
        art_info = FourSquarePlacesHelper().get_places(city="New York", categories="19040", limit=5)
        assert len(art_info) == 2
        assert art_info[0]["name"] == "Arts A"

    @patch('search.helpers.photo.UnplashCityPhotoHelper.get_city_photo')
    def test_city_photo(self,mock_get_city_photo):
        """
        Tests that a city photo can be retrieved for New York City.
        """
        city = "New York City"
        mock_get_city_photo.return_value = "https://example.com/photo.jpg"
        photo_link = UnplashCityPhotoHelper().get_city_photo(city=city)
        assert photo_link is not None

    def test_models(self):
        """
        Tests the user model
        """
        user = get_user_model().objects.create_user("admin@citybyte.com", "password")
        assert user


class ItineraryTests(TestCase):
    """Tests for the ItineraryItem model and its associated views, ensuring correct functionality for user itineraries."""

    def setUp(self):
        """Set up the test environment by creating a user and logging them in."""
        self.user = get_user_model().objects.create_user(
            username="testuser", password="Test@123"
        )
        self.client.login(username="testuser", password="Test@123")
        self.city = "Hyderabad"
        self.spot_name = "Charminar"
        self.address = "Old City, Hyderabad 500002, Telangana"
        self.category = "Monument"

    def test_add_to_itinerary(self):
        """Test that an itinerary item is added successfully to the user's itinerary."""
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ItineraryItem.objects.count(), 1)
        item = ItineraryItem.objects.first()
        self.assertEqual(item.user, self.user)
        self.assertEqual(item.city, self.city)
        self.assertEqual(item.spot_name, self.spot_name)
        self.assertEqual(item.address, self.address)
        self.assertEqual(item.category, self.category)

    def test_remove_from_itinerary(self):
        """Test that an itinerary item can be successfully removed from the user's itinerary."""
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        response = self.client.post(reverse('info:remove_from_itinerary', args=[self.city, self.spot_name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ItineraryItem.objects.count(), 0)
        self.assertContains(response, 'Removed from itinerary.')

    def test_add_multiple_items_to_itinerary(self):
        """Test that multiple itinerary items can be added successfully."""
        spots = [
            {"name": "KBR Park", "address": "Kbr National Park (LV Prasad Marg), Hyderabad 591226, Telangana", "category": "Park"},
            {"name": "Tank Bund", "address": "Lumbani Park, Hyderabad 472708, Telangana", "category": "Landmarks and Outdoors"},
            {"name": "Chowmahala Palace", "address": "Moti Gali, Hyderabad, Telangana", "category": "History Museum"},
        ]

        for spot in spots:
            response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, spot["name"], spot["address"], spot["category"]]))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Added to itinerary.')

        self.assertEqual(ItineraryItem.objects.count(), len(spots))

    def test_json_response_structure_on_successful_add(self):
        """Test the structure of the JSON response on successful item addition."""
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        json_response = response.json()
        self.assertIn('status', json_response)
        self.assertIn('message', json_response)
        self.assertEqual(json_response['status'], 'success')

    def test_unauthenticated_user_add_attempt(self):
        """Test that an unauthenticated user cannot add items to the itinerary."""
        self.client.logout()  # Log out to simulate an unauthenticated user
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 302)

    def test_case_insensitive_city_and_category(self):
        """Test that city and category are case insensitive."""
        response_upper = self.client.post(reverse('info:add_to_itinerary', args=[self.city.upper(), self.spot_name, self.address, self.category.upper()]))
        response_lower = self.client.post(reverse('info:add_to_itinerary', args=[self.city.lower(), self.spot_name, self.address, self.category.lower()]))
        self.assertEqual(response_upper.status_code, 200)
        self.assertEqual(response_lower.status_code, 200)

    def test_special_characters_in_spot_name(self):
        """Test adding an itinerary item with special characters in the spot name."""
        special_spot_name = "KBR Park & Zoo @ Hyderabad!"
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, special_spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 200)

    def test_re_add_removed_item(self):
        """Test re-adding an item that was previously removed from the itinerary."""
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.client.post(reverse('info:remove_from_itinerary', args=[self.city, self.spot_name]))
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 200)

    def test_remove_multiple_items(self):
        """Test that multiple itinerary items can be removed successfully."""
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, "KBR Park", self.address, self.category]))
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, "Tank Bund", self.address, self.category]))

        response = self.client.post(reverse('info:remove_from_itinerary', args=[self.city, "KBR Park"]))
        self.assertContains(response, 'Removed from itinerary.')
        self.assertEqual(ItineraryItem.objects.count(), 1)

        response = self.client.post(reverse('info:remove_from_itinerary', args=[self.city, "Tank Bund"]))
        self.assertContains(response, 'Removed from itinerary.')
        self.assertEqual(ItineraryItem.objects.count(), 0)

    def test_itinerary_item_fields(self):
        """Test that the fields of an itinerary item are set correctly upon addition."""
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        item = ItineraryItem.objects.first()
        self.assertEqual(item.user, self.user)
        self.assertEqual(item.city, self.city)
        self.assertEqual(item.spot_name, self.spot_name)
        self.assertEqual(item.address, self.address)
        self.assertEqual(item.category, self.category)

    def test_add_to_itinerary_without_login(self):
        """Test that unauthenticated users are redirected when trying to add an itinerary item."""
        self.client.logout()
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 302)

    def test_remove_from_itinerary_without_login(self):
        """Test that unauthenticated users are redirected when trying to remove an itinerary item."""
        self.client.logout()
        response = self.client.post(reverse('info:remove_from_itinerary', args=[self.city, self.spot_name]))
        self.assertEqual(response.status_code, 302)

    def test_view_itinerary_page(self):
        """Test that the itinerary page loads successfully."""
        response = self.client.get(reverse('info:itinerary_page'))
        self.assertEqual(response.status_code, 200)

    def test_itinerary_item_uniqueness_per_user(self):
        """Test that different users can add the same itinerary item independently."""
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.client.logout()
        new_user = get_user_model().objects.create_user(username="user2", password="Test@123")
        self.client.login(username="user2", password="Test@123")
        response = self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Added to itinerary.')
        self.assertEqual(ItineraryItem.objects.count(), 2)

    def test_itinerary_item_string_representation(self):
        item = ItineraryItem.objects.create(
            user=self.user,
            city=self.city,
            spot_name=self.spot_name,
            address=self.address,
            category=self.category,
        )
        self.assertEqual(str(item), f"{self.spot_name} in {self.city} - {self.user.username}")

    def test_added_on_field(self):
        """Test the string representation of the ItineraryItem model."""
        item = ItineraryItem.objects.create(
            user=self.user,
            city=self.city,
            spot_name=self.spot_name,
            address=self.address,
            category=self.category,
        )
        self.assertIsNotNone(item.added_on)
        self.assertTrue(item.added_on <= timezone.now())

    def test_itinerary_item_count(self):
        '''Check that a user can have multiple unique items'''
        for i in range(3):
            self.client.post(reverse('info:add_to_itinerary', args=[self.city, f"Spot {i}", self.address, self.category]))
        self.assertEqual(ItineraryItem.objects.count(), 3)

    def test_itinerary_item_category(self):
        """Test that the category of an itinerary item is set correctly upon addition."""
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, 'New Category']))
        item = ItineraryItem.objects.first()
        self.assertEqual(item.category, 'New Category')

    def test_itinerary_with_different_users(self):
        """Test that different users can have separate itinerary items without interference."""
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, self.spot_name, self.address, self.category]))
        self.client.logout()
        new_user = get_user_model().objects.create_user(username="user3", password="Test@123")
        self.client.login(username="user3", password="Test@123")
        self.client.post(reverse('info:add_to_itinerary', args=[self.city, "New Spot", self.address, self.category]))
        self.assertEqual(ItineraryItem.objects.filter(user=self.user).count(), 1)
        self.assertEqual(ItineraryItem.objects.filter(user=new_user).count(), 1)


class AuthTests(TestCase):
    """
    Tests that relate to log-in and log-out functionality
    """
    def setUp(self):
        """
        Setup for tests in this class
        """
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password", email="test@example.com"
        )

    def test_signup_view_renders_correct_template(self):
        """
        Tests that a sign-up template is used
        """
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "registration/signup.html")
        self.assertEqual(response.status_code, 200)

    def test_successful_signup_creates_user(self):
        """
        Tests that a user can sign up
        """
        response = self.client.post(
            reverse("signup"), {"username": "newuser", "password1": "newpassword123", "password2": "newpassword123"}
        )
        self.assertEqual(get_user_model().objects.count(), 2)  # 1 existing user + 1 new user
        self.assertRedirects(response, reverse("login"))

    def test_sign_in_renders_login_template(self):
        """
        Tests to a sign-in template is used
        """
        response = self.client.get(reverse("sign_in"))
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertEqual(response.status_code, 200)

    @patch("google.auth.transport.requests.Request")
    @patch("google.oauth2.id_token.verify_oauth2_token")
    def test_auth_receiver_successful_login(self, mock_verify, mock_request):
        """Tests to ensure that a Google user can successfully log in
        """
        mock_verify.return_value = {"email": "test@example.com", "given_name": "Test", "family_name": "User"}
        token = "valid_token"
        response = self.client.post(reverse("auth_receiver"), {"credential": token})
        self.assertRedirects(response, reverse("main_page"))
        self.assertTrue(self.client.session.get("user_data"))

    def test_sign_out_redirects_to_sign_in(self):
        """
        Tests to ensure that, after a sign-out, the user is redirected to the sign-in page and their session is deleted
        """
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(reverse("sign_out"))
        self.assertRedirects(response, reverse("sign_in"))
        self.assertFalse(self.client.session.get("user_data"))

    def test_sign_out_handles_logout_exception(self):
        """
        Tests to ensure redirect
        """
        self.client.login(username="test_user", password="test_password")
        with patch("django.contrib.auth.logout", side_effect=Exception("Logout error")):
            response = self.client.get(reverse("sign_out"))
            self.assertRedirects(response, reverse("sign_in"))

    def test_user_login_and_redirect(self):
        """
        Tests to ensure a user redirects to the home page after login
        """
        response = self.client.login(username="test_user", password="test_password")
        self.assertTrue(response)
        response = self.client.get(reverse("main_page"))
        self.assertEqual(response.status_code, 200)


class AuthErrorTests(TestCase):
    """
    Tests that cause failures relating to log-in/log-out and ensure there is error handling
    """
    def setUp(self):
        """
        Setup for tests in this class
        """
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="test_user", password="test_password")

    def test_signup_form_validation(self):
        """
        Tests that a user cannot sign up without a username"""
        response = self.client.post(reverse("signup"), {"username": "", "password1": "pass", "password2": "pass"})
        self.assertFormError(response, "form", "username", "This field is required.")

    def test_sign_in_with_invalid_credentials(self):
        """
        Tests to ensure a user cannot sign in with the wrong username and password
        """
        response = self.client.post(reverse("sign_in"), {"username": "wronguser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 200)

    def test_signup_with_existing_username_fails(self):
        """
        Tests to ensure that duplicate usernames are not allowed
        """
        response = self.client.post(
            reverse("signup"), {"username": "test_user", "password1": "newpassword123", "password2": "newpassword123"}
        )
        self.assertFormError(response, "form", "username", "A user with that username already exists.")

    def test_auth_receiver_with_missing_token(self):
        """
        Tests to ensure a Google login is not approved with no token/credential parameter
        """
        response = self.client.post(reverse("auth_receiver"), {})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {"error": "Missing credential"})

    def test_auth_receiver_with_empty_token(self):
        """
        Tests to ensure a Google login is not approved with no token/credential value
        """
        response = self.client.post(reverse("auth_receiver"), {"credential": ""})
        self.assertEqual(response.status_code, 403)

    @patch("google.oauth2.id_token.verify_oauth2_token", side_effect=ValueError("Invalid token"))  # Mock up of scenario with an invalid token
    def test_auth_receiver_failure_due_to_value_error(self, mock_verify):
        """
        Tests to ensure a Google login is not approved with an invalid token
        """
        response = self.client.post(reverse("auth_receiver"), {"credential": "some_invalid_token"})
        self.assertEqual(response.status_code, 403)

    def test_sign_out_without_login_redirects(self):
        """
        Tests to ensure that, if log out is attempted while not logged in, there is a redirect to the login page
        """
        response = self.client.get(reverse("sign_out"))
        self.assertRedirects(response, reverse("sign_in"))  # Should redirect even if not logged in

    def test_user_login_with_incorrect_password(self):
        """
        Tests to ensure that a user cannot log in with an incorrect password
        """
        response = self.client.login(username="test_user", password="wrongpass")
        self.assertFalse(response)

    def test_signup_with_passwords_not_matching(self):
        """
        Tests to ensure that a user cannot sign up with two different passwords
        """
        response = self.client.post(
            reverse("signup"), {"username": "newuser", "password1": "password123", "password2": "differentpassword"}
        )
        self.assertFormError(
            response, "form", "password2", "The two password fields didn’t match."
        )  # weird apostrophe is used in the forms - took forever to debug

    def test_sign_in_with_non_existent_user(self):
        """
        Tests to ensure that a fake/nonexistent account cannot sign in
        """
        response = self.client.post(reverse("sign_in"), {"username": "nonexistent", "password": "somepassword"})
        self.assertEqual(response.status_code, 200)  # Should render login page again

    def test_sign_out_with_no_active_session(self):
        """
        Test to ensure logout redirects to sign in
        """
        self.client.logout()  # Ensure user is logged out
        response = self.client.get(reverse("sign_out"))
        self.assertRedirects(response, reverse("sign_in"))  # Should still redirect to sign in

    def test_auth_receiver_when_user_creation_fails(self):
        """
        Tests that authorization fails when the creation fails
        """
        @patch("django.contrib.auth.models.User.objects.get_or_create", side_effect=Exception("Database error"))  # mock up of database failure
        def mock_user_creation(mock_get_or_create):
            """
            Tests the user creation token
            """
            token = "valid_token"
            response = self.client.post(reverse("auth_receiver"), {"credential": token})
            self.assertEqual(response.status_code, 403)

        mock_user_creation()

    def test_password_too_common(self):
        """
        Tests to ensure common passwords are not allowed
        """
        response = self.client.post(
            reverse("signup"), {"username": "newuser", "password1": "password123", "password2": "password123"}
        )
        self.assertFormError(response, "form", "password2", "This password is too common.")


class InfoViewsTestCase(TestCase):
    """
    Tests relating to info/views.py
    """
    def setUp(self):
        """
        Setup for tests in this class
        """
        
    @patch("os.getenv", return_value="test_google_api_key")
    def test_google_maps_api(self, mock_env):
        response = self.client.get(reverse("google_maps_api"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("script", response.json())
        self.assertIn("test_google_api_key", response.json()["script"])

    @patch("googlemaps.Client.geocode", return_value=[{"geometry": {"location": {"lat": 17.385, "lng": 78.4867}}}])
    def test_drop_pin_success(self, mock_geocode):
        response = self.client.get(reverse("drop_pin"), {"location": self.city})
        self.assertEqual(response.status_code, 200)
        self.assertIn("latitude", response.json())
        self.assertIn("longitude", response.json())

    @patch("googlemaps.Client.geocode", return_value=[])
    def test_drop_pin_location_not_found(self, mock_geocode):
        response = self.client.get(reverse("drop_pin"), {"location": "Unknown"})
        self.assertEqual(response.status_code, 404)

    def test_drop_pin_no_location(self):
        response = self.client.get(reverse("drop_pin"))
        self.assertEqual(response.status_code, 400)

    def test_add_to_fav(self):
        response = self.client.get(reverse("addToFav"), {"city": self.city, "country": self.country})
        self.assertEqual(response.json()["data"], "added")
        self.assertTrue(FavCityEntry.objects.filter(city=self.city, country=self.country, user=self.user).exists())

        response = self.client.get(reverse("addToFav"), {"city": self.city, "country": self.country})
        self.assertEqual(response.json()["data"], "removed")
        self.assertFalse(FavCityEntry.objects.filter(city=self.city, country=self.country, user=self.user).exists())

    def test_add_to_fav_missing_params(self):
        response = self.client.get(reverse("addToFav"))
        self.assertEqual(response.json()["data"], None)

    def test_profile_page(self):
        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile/profile.html")

    def test_itinerary_page(self):
        response = self.client.get(reverse("itinerary_page"), {"city": self.city, "country": self.country})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/itinerary.html")

    def test_all_itineraries_page(self):
        response = self.client.get(reverse("all_itineraries"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/all_itineraries.html")

    def test_add_to_itinerary(self):
        response = self.client.post(
            reverse("add_to_itinerary", args=[self.city, "Charminar", "Old City", "Monument"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ItineraryItem.objects.filter(user=self.user, city=self.city, spot_name="Charminar").exists())

    def test_remove_from_itinerary(self):
        ItineraryItem.objects.create(user=self.user, city=self.city, spot_name="Charminar")
        response = self.client.post(reverse("remove_from_itinerary", args=[self.city, "Charminar"]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ItineraryItem.objects.filter(user=self.user, city=self.city, spot_name="Charminar").exists())

class CityByteTestSuite(TestCase):
    """Comprehensive test suite for CityByte application"""

    def setUp(self):
        """Set up common test data and configurations"""
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password", email="test@example.com"
        )
        self.client.login(username="test_user", password="test_password")
        self.city = "Hyderabad"
        self.country = "India"
        self.address = "Old City"
        self.category = "Monument"
        self.spot_name = "Charminar"
        self.fsq_id = "test-fsq-id"
        self.url = URL(protocol="https", host="api.foursquare.com", port=443)  # Added port


    # Test Model Behavior
    def test_itinerary_item_model(self):
        """Test creation and string representation of ItineraryItem"""
        item = ItineraryItem.objects.create(
            user=self.user,
            city=self.city,
            spot_name=self.spot_name,
            address=self.address,
            category=self.category,
        )
        self.assertEqual(str(item), f"{self.spot_name} in {self.city} - {self.user.username}")
        self.assertIsNotNone(item.added_on)

    # Test Favorite City Features
    def test_add_and_remove_favorite_city(self):
        """Test adding and removing a favorite city"""
        response = self.client.get(reverse("addToFav"), {"city": self.city, "country": self.country})
        self.assertEqual(response.json()["data"], "added")
        self.assertTrue(FavCityEntry.objects.filter(city=self.city, country=self.country, user=self.user).exists())

        response = self.client.get(reverse("addToFav"), {"city": self.city, "country": self.country})
        self.assertEqual(response.json()["data"], "removed")
        self.assertFalse(FavCityEntry.objects.filter(city=self.city, country=self.country, user=self.user).exists())

    # Test Itinerary Features
    def test_add_to_itinerary(self):
        """Test adding an item to the itinerary"""
        response = self.client.post(
            reverse("add_to_itinerary", args=[self.city, self.spot_name, self.address, self.category])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ItineraryItem.objects.filter(user=self.user, city=self.city, spot_name=self.spot_name).exists())

    def test_remove_from_itinerary(self):
        """Test removing an item from the itinerary"""
        ItineraryItem.objects.create(
            user=self.user, city=self.city, spot_name=self.spot_name, address=self.address, category=self.category
        )
        response = self.client.post(reverse("remove_from_itinerary", args=[self.city, self.spot_name]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ItineraryItem.objects.filter(user=self.user, city=self.city, spot_name=self.spot_name).exists())

    # Test Utility Features
    @patch("requests.request")
    def test_get_place_photo(self, mock_request):
        """Test fetching place photo"""
        mock_request.return_value.json.return_value = [{"prefix": "https://example.com/", "suffix": ".jpg"}]
        photo_url = FourSquare(self.url).get_place_photo(fsq_id=self.fsq_id)
        self.assertEqual(photo_url, "https://example.com/250x250.jpg")

    @patch("requests.request")
    def test_get_place_photo_no_photos(self, mock_request):
        """Test fallback for places with no photos"""
        mock_request.return_value.json.return_value = []
        photo_url = FourSquare(self.url).get_place_photo(fsq_id="invalid")
        self.assertEqual(photo_url, "https://picsum.photos/200")

    @patch("requests.request")
    def test_get_places(self, mock_request):
        """Test fetching places using FourSquare API"""
        mock_request.return_value.json.return_value = {"results": [{"name": "Place A"}, {"name": "Place B"}]}
        places = FourSquare(self.url).get_places(city=self.city)
        self.assertIn("results", places)
        self.assertEqual(len(places["results"]), 2)

    # Test Profile Page
    def test_profile_page(self):
        """Test loading profile page with favorite cities"""
        FavCityEntry.objects.create(city="Paris", country="France", user=self.user)
        response = self.client.get(reverse("profile_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Paris")

    # Test Error Handling
    def test_missing_query_params(self):
        """Test handling of missing query parameters in requests"""
        response = self.client.get(reverse("addToFav"))
        self.assertEqual(response.json()["data"], None)

    # Test Utility Integration
    @patch("os.getenv", return_value="fake_key")
    def test_google_maps_api(self, mock_env):
        """Test integration with Google Maps API"""
        response = self.client.get(reverse("google_maps_api"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("script", response.json())

    def test_cache_integration(self):
        """Test interaction with caching backend"""
        with patch("django.core.cache.cache.get", return_value=None), patch("django.core.cache.cache.set") as mock_set:
            response = self.client.get(reverse("place_photo"), {"fsq_id": self.fsq_id})
            mock_set.assert_called_once()

    # Test Miscellaneous Scenarios
    def test_case_insensitivity(self):
        """Test case insensitivity for city and category"""
        response = self.client.post(
            reverse("add_to_itinerary", args=[self.city.upper(), self.spot_name, self.address, self.category.lower()])
        )
        self.assertEqual(response.status_code, 200)

    def test_special_characters_in_spot_name(self):
        """Test handling of special characters in spot name"""
        special_name = "KBR Park & Zoo @ Hyderabad!"
        response = self.client.post(reverse("add_to_itinerary", args=[self.city, special_name, self.address, self.category]))
        self.assertEqual(response.status_code, 200)

    def test_re_add_removed_item(self):
        """Test re-adding a previously removed item"""
        response = self.client.post(reverse("add_to_itinerary", args=[self.city, self.spot_name, self.address, self.category]))
        self.client.post(reverse("remove_from_itinerary", args=[self.city, self.spot_name]))
        response = self.client.post(reverse("add_to_itinerary", args=[self.city, self.spot_name, self.address, self.category]))
        self.assertEqual(response.status_code, 200)

#     # should add more tests relating to the profile page
class TestGeoDB(TestCase):
    def setUp(self):
        # Provide required arguments for the URL class
        self.url = URL(protocol="https", host="test-geodb.com", port=None)
        self.geo_db = GeoDB(url=self.url)

    def tearDown(self):
        self.geo_db = None

    def test_get_city_suggestions_success(self):
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"data": [{"city": "Test City", "country": "Test Country"}]}
            mock_request.return_value = mock_response

            city_suggestions = self.geo_db.get_city_suggestions(city="Test")
            self.assertIn("data", city_suggestions)
            self.assertEqual(city_suggestions["data"][0]["city"], "Test City")

    def test_get_city_suggestions_failure(self):
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "Invalid Request"}
            mock_request.return_value = mock_response

            city_suggestions = self.geo_db.get_city_suggestions(city="Invalid")
            self.assertIn("error", city_suggestions)
            self.assertEqual(city_suggestions["error"], "Invalid Request")


class TestAmadeusCitySearch(TestCase):
    def setUp(self):
        # Provide required arguments for the URL class
        self.url = URL(protocol="https", host="test-amadeus.com", port=None)
        self.city_search = AmadeusCitySearch(url=self.url)

    def tearDown(self):
        self.city_search = None

    def test_get_city_suggestions_success(self):
        with patch("requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.json.return_value = {"data": [{"name": "New York"}]}
            mock_request.return_value = mock_response

            self.city_search._access_token = "test_access_token"
            city_suggestions = self.city_search.get_city_suggestions(city="New York")
            self.assertIn("data", city_suggestions)
            self.assertEqual(city_suggestions["data"][0]["name"], "New York")