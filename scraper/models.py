from django.db import models


class ScraperAll(models.Model):
    """
    Model representing scraped data for movies.
    """
    cinema_name = models.CharField(max_length=255)
    city_name = models.CharField(max_length=255)
    date = models.DateField()
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    booking_link = models.URLField(unique=True, default="")
    time = models.TimeField(default="")
