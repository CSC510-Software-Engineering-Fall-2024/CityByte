from django.db import models
from django.contrib.auth import get_user_model


class CitySearchRecord(models.Model):
    city_name = models.CharField(max_length=126)
    country_name = models.CharField(max_length=126)

    def __str__(self):
        return f"{self.city_name}-{self.country_name}"


class Comment(models.Model):
    city = models.CharField(max_length=125)
    country = models.CharField(max_length=125)
    comment = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}-{self.country}-{self.author.username}"


class FavCityEntry(models.Model):
    city = models.CharField(max_length=125)
    country = models.CharField(max_length=125)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city}-{self.country}-{self.user.username}"


class ItineraryItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    spot_name = models.CharField(max_length=255)
    address = models.TextField()
    category = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)
    scheduled_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.spot_name} in {self.city} - {self.user.username}"
