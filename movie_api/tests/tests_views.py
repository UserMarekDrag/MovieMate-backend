from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from movie_api.models import SearchHistory
from movie_api.views import MovieList, MovieDetail, MovieCreate, MovieDelete, ShowList, ApiOverview
from rest_framework.test import APIRequestFactory, force_authenticate
from mixer.backend.django import mixer
from movie_api.serializers import SearchHistorySerializer
import json
from user_api.models import AppUser


class MovieListViewTest(TestCase):
    """Test suite for the MovieList view."""

    def setUp(self):
        """Create test user, setup API request factory, and MovieList view."""
        self.factory = APIRequestFactory()
        self.view = MovieList.as_view()
        self.uri = '/movie-list/'
        self.user = AppUser.objects.create_user(username='jacob', email='jacob@example.com', password='top_secret')

    def test_list(self):
        """Test for getting the list of movies. Ensures that the response code is 200."""
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))


class MovieDetailViewTest(TestCase):
    """Test suite for the MovieDetail view."""

    def setUp(self):
        """Create test user, setup API request factory, and MovieDetail view."""
        self.factory = APIRequestFactory()
        self.view = MovieDetail.as_view()
        self.uri = '/movie-detail/'
        self.user = AppUser.objects.create_user(email='jacob@example.com', username='jacob', password='top_secret')
        self.search_history = mixer.blend('movie_api.SearchHistory')

    def test_detail(self):
        """Test for getting the detail of a movie. Ensures that the response code is 200."""
        request = self.factory.get(self.uri+str(self.search_history.id)+'/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.search_history.id)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))


class MovieDeleteViewTest(TestCase):
    """Test suite for the MovieDelete view."""

    def setUp(self):
        """Create test user, setup API request factory, and MovieDelete view."""
        self.factory = APIRequestFactory()
        self.view = MovieDelete.as_view()
        self.uri = '/movie-delete/'
        self.user = AppUser.objects.create_user(email='jacob@example.com', username='jacob', password='top_secret')
        self.search_history = mixer.blend('movie_api.SearchHistory')

    def test_delete_movie(self):
        """Test for deleting a movie. Ensures that the response code is 204."""
        request = self.factory.delete(self.uri+str(self.search_history.id)+'/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.search_history.id)
        self.assertEqual(response.status_code, 204, 'Expected Response Code 204, received {0} instead.'.format(response.status_code))


class ShowListViewTest(TestCase):
    """Test suite for the ShowList view."""

    def setUp(self):
        """Create test user, setup API request factory, and ShowList view."""
        self.factory = APIRequestFactory()
        self.view = ShowList.as_view()
        self.uri = '/show-list/'
        self.user = AppUser.objects.create_user(email='jacob@example.com', username='jacob', password='top_secret')

    def test_show_list(self):
        """Test for getting the list of shows. Ensures that the response code is 200."""
        request = self.factory.get(self.uri)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
