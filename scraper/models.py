from django.db import models


class Cinema(models.Model):
    """
    Model representing a cinema.
    """
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)


class Movie(models.Model):
    """
    Model representing a movie.
    """
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    image_url = models.URLField(null=True)
    movie_url = models.URLField(max_length=2000, null=True)


class Show(models.Model):
    """
    Model representing a movie show.
    """
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    booking_link = models.URLField(unique=True)
