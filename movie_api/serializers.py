from rest_framework import serializers
from django.utils import timezone
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
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
