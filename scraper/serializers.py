from rest_framework import serializers
from .models import Cinema, Film, Showtime, ScraperData, FilmTimes


class CinemaSerializer(serializers.ModelSerializer):
    """Serializer for the Cinema model."""
    class Meta:
        model = Cinema
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    """Serializer for the Film model."""
    cinema = CinemaSerializer()

    class Meta:
        model = Film
        fields = '__all__'


class ShowtimeSerializer(serializers.ModelSerializer):
    """Serializer for the Showtime model."""
    film = FilmSerializer()

    class Meta:
        model = Showtime
        fields = '__all__'


class FilmTimesSerializer(serializers.ModelSerializer):
    """Serializer for the FilmTimes model."""
    showing = ShowtimeSerializer()

    class Meta:
        model = FilmTimes
        fields = '__all__'


class ScraperDataSerializer(serializers.ModelSerializer):
    """Serializer for the ScraperData model."""
    cinema = CinemaSerializer()

    class Meta:
        model = ScraperData
        fields = '__all__'
