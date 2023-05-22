from django.db import models


class Cinema(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)


class City(models.Model):
    """Represents a cinema."""
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='city')
    data = models.ForeignKey('ScraperData', on_delete=models.CASCADE, related_name='data')


class Film(models.Model):
    """Represents a film."""
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    description = models.TextField(default="")
    image_url = models.URLField()
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='films')


class Showtime(models.Model):
    """Represents a film's showtime at a cinema."""
    film = models.ForeignKey('Film', on_delete=models.CASCADE, related_name='showtimes')
    city = models.ForeignKey('City', on_delete=models.CASCADE, related_name='showtimes')
    time = models.TimeField(default="")
    booking_link = models.URLField(default="")


class ScraperData(models.Model):
    """Represents scraped data for a cinema."""
    date = models.DateField()
