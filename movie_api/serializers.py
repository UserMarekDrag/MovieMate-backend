from rest_framework import serializers
from django.utils import timezone
from .models import Movie
from scraper.models import ScraperAll


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """
    class Meta:
        model = Movie
        fields = ['id', 'user', 'city', 'showing_date', 'created_date']
        read_only_fields = ['id', 'user', 'created_date']

    def validate(self, data):
        """
        Check that the showing_date is not in the past.
        """
        showing_date = data['showing_date']
        if showing_date <= timezone.now():
            raise serializers.ValidationError("Showing date cannot be in the past.")
        return data


class ScraperAllSerializer(serializers.ModelSerializer):
    """
    Serializer for the ScraperAll model.
    """
    class Meta:
        model = ScraperAll
        fields = ['cinema_name', 'city_name', 'date', 'title', 'category', 'description', 'image_url', 'booking_link', 'time']
