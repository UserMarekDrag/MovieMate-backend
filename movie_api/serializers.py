from rest_framework import serializers
from django.utils import timezone
from .models import Movie
from scraper.models import Showtime, Film, City


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


class FilmSerializer(serializers.ModelSerializer):
    """
    Serializer for the Film model.
    """
    class Meta:
        model = Film
        fields = ['title', 'category', 'description', 'image_url']


class CitySerializer(serializers.ModelSerializer):
    """
    Serializer for the City model.
    """
    class Meta:
        model = City
        fields = ['name']


class ShowtimeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Showtime model.
    """
    film = FilmSerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Showtime
        fields = ['film', 'city', 'time', 'booking_link']
