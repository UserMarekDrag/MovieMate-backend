from django.db import models


class Film(models.Model):
    """Represents a film."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_info = models.DateField()
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='films')


class Cinema(models.Model):
    """Represents a cinema."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    url = models.URLField(max_length=255)


class Showtime(models.Model):
    """Represents a film's showtime at a cinema."""
    film = models.ForeignKey('Film', on_delete=models.CASCADE, related_name='showtimes')
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()


class FilmTimes(models.Model):
    """Represents specific film showtimes at a cinema."""
    film = models.ForeignKey('Film', on_delete=models.CASCADE, related_name='filmtime')
    hours = models.TimeField()
    booking_link = models.URLField()


class ScraperData(models.Model):
    """Represents scraped data for a cinema."""
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='scraper_data')
    scraped_date = models.DateField(auto_now_add=True)
