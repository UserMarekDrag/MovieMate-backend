from django.db import models


class Cinema(models.Model):
    """Represents a cinema."""
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)


class City(models.Model):
    """Represents a city."""
    name = models.CharField(max_length=255)


class CinemaInCity(models.Model):
    """Represents a cinema in city."""
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='city')
    url = models.URLField(max_length=255)
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='cinema')
    data = models.ForeignKey('ScraperData', on_delete=models.CASCADE, related_name='data')


class Film(models.Model):
    """Represents a film."""
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    cinema_in_city = models.ForeignKey('CinemaInCity', on_delete=models.CASCADE, related_name='films')


class Showtime(models.Model):
    """Represents a film's showtime at a cinema."""
    film = models.ForeignKey('Film', on_delete=models.CASCADE, related_name='showtimes')
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='showtimes')
    time = models.TimeField(default="")
    booking_link = models.URLField(default="")


class ScraperData(models.Model):
    """Represents scraped data for a cinema."""
    date = models.DateField(unique=True)
