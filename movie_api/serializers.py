from rest_framework import serializers
from django.utils import timezone
from scraper.models import Cinema, Movie, Show
from .models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """
    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'city', 'showing_date', 'created_date']
        read_only_fields = ['id', 'user', 'created_date']

    def validate(self, data):
        """
        Check that the showing_date is not in the past.
        """
        showing_date = data['showing_date']
        if showing_date <= timezone.now().date():
            raise serializers.ValidationError("Showing date cannot be in the past.")
        return data


class CinemaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cinema model.
    """
    class Meta:
        model = Cinema
        fields = ['name', 'city', 'address']


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """
    class Meta:
        model = Movie
        fields = ['title', 'category', 'description', 'image_url', 'movie_url']


class ShowSerializer(serializers.ModelSerializer):
    """
    Serializer for the Show model.
    """
    cinema = CinemaSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Show
        fields = ['cinema', 'movie', 'date', 'time', 'booking_link']
