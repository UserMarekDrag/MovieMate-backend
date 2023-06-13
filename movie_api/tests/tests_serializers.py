from datetime import datetime, timedelta
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from scraper.models import Cinema, Movie, Show
from movie_api.models import SearchHistory
from movie_api.serializers import SearchHistorySerializer, CinemaSerializer, MovieSerializer, ShowSerializer


class MovieSerializerTest(TestCase):
    """Test suite for the MovieSerializer."""

    def setUp(self):
        """Create sample Movie object and MovieSerializer instance."""
        self.movie = Movie.objects.create(title='Test movie', category='Drama', description='Test description',
                                          image_url='https://example.com/image.jpg')
        self.serializer = MovieSerializer(instance=self.movie)

    def test_contains_expected_fields(self):
        """Ensure serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['title', 'category', 'description', 'image_url'])


class CinemaSerializerTest(TestCase):
    """Test suite for the CinemaSerializer."""

    def setUp(self):
        """Create sample Cinema object and CinemaSerializer instance."""
        self.cinema = Cinema.objects.create(name='Test cinema', city='Test city')
        self.serializer = CinemaSerializer(instance=self.cinema)

    def test_contains_expected_fields(self):
        """Ensure serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['name', 'city'])


class ShowSerializerTest(TestCase):
    """Test suite for the ShowSerializer."""

    def setUp(self):
        """Create sample Show object and ShowSerializer instance."""
        self.cinema = Cinema.objects.create(name='Test cinema', city='Test city')
        self.movie = Movie.objects.create(title='Test movie', category='Drama', description='Test description',
                                          image_url='https://example.com/image.jpg')
        self.show = Show.objects.create(cinema=self.cinema, movie=self.movie, date='2023-06-03', time='10:00:00',
                                        booking_link='https://example.com/booking_link')
        self.serializer = ShowSerializer(instance=self.show)

    def test_contains_expected_fields(self):
        """Ensure serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['cinema', 'movie', 'date', 'time', 'booking_link'])


class SearchHistorySerializerTest(TestCase):
    """Test suite for the SearchHistorySerializer."""

    def setUp(self):
        """Create sample SearchHistory object and SearchHistorySerializer instance."""
        self.search_history = SearchHistory.objects.create(user=None, city='Test city', showing_date='2023-06-03')
        self.serializer = SearchHistorySerializer(instance=self.search_history)

    def test_contains_expected_fields(self):
        """Ensure serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'user', 'city', 'showing_date', 'created_date'])

    def test_validate_showing_date(self):
        """Ensure showing_date validation works properly by checking that past dates are invalid."""
        serializer = SearchHistorySerializer(data={'user': None, 'city': 'Test city',
                                                   'showing_date': datetime.today() - timedelta(days=1)})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
