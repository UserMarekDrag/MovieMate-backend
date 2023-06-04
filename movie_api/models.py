from django.db import models
from django.utils import timezone
from user_api.models import AppUser


class SearchHistory(models.Model):
    """
    Model representing the search history of movies/shows.
    """
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100)
    showing_date = models.DateField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Returns a string representation of the search history object.
        """
        return self.city
