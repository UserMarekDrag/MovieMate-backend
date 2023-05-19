from django.db import models


class Cinema(models.Model):
    """Represents a cinema."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)  # Make it optional as it can be empty
    url = models.URLField(max_length=255)


class Film(models.Model):
    """Represents a film."""
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    description = models.TextField(default="")
    image_url = models.URLField()
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='films')


class Showtime(models.Model):
    """Represents a film's showtime at a cinema."""
    film = models.ForeignKey('Film', on_delete=models.CASCADE, related_name='showtimes')
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField(default="")
    booking_link = models.URLField(default="")


class ScraperData(models.Model):
    """Represents scraped data for a cinema."""
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='scraper_data')
    scraped_date = models.DateField(auto_now_add=True)
