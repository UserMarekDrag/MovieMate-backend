from django.db import models
from django.utils import timezone
from user_api.models import AppUser


class Movie(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100)
    showing_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # it will return the title
        return self.city
