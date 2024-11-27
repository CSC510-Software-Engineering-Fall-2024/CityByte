class InfoViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username="test_user", password="test_password")
        self.client.login(username="test_user", password="test_password")
        self.city = "Hyderabad"
        self.country = "India"
        self.fsq_id = "test-fsq-id"

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