from django.test import TestCase
from scraper.models import Cinema, Movie, Show


class CinemaModelTest(TestCase):
    """
    Test class for the Cinema model.
    """
    def test_cinema_creation(self):
        """
        Test case for creating a Cinema object.
        """
        cinema = Cinema.objects.create(name='Cinema Test', city='City Test')
        self.assertEqual(cinema.name, 'Cinema Test')
        self.assertEqual(cinema.city, 'City Test')


class MovieModelTest(TestCase):
    """
    Test class for the Movie model.
    """
    def test_movie_creation(self):
        """
        Test case for creating a Movie object.
        """
        movie = Movie.objects.create(
            title='Movie Test', category='Action', description='Description Test', image_url='www.test.com')
        self.assertEqual(movie.title, 'Movie Test')
        self.assertEqual(movie.category, 'Action')
        self.assertEqual(movie.description, 'Description Test')
        self.assertEqual(movie.image_url, 'www.test.com')


class ShowModelTest(TestCase):
    """
    Test class for the Show model.
    """
    def test_show_creation(self):
        """
        Test case for creating a Show object.
        """
        cinema = Cinema.objects.create(name='Cinema Test', city='City Test')
        movie = Movie.objects.create(
            title='Movie Test', category='Action', description='Description Test', image_url='www.test.com')
        show = Show.objects.create(
            cinema=cinema, movie=movie, date='2023-06-01', time='13:00:00', booking_link='www.test.com')
        self.assertEqual(show.cinema, cinema)
        self.assertEqual(show.movie, movie)
        self.assertEqual(show.date, '2023-06-01')
        self.assertEqual(show.time, '13:00:00')
        self.assertEqual(show.booking_link, 'www.test.com')
