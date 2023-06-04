from django.test import TestCase
from movie_api.models import SearchHistory
from user_api.models import AppUser


class ShowModelTest(TestCase):
    """
    Test class for the SearchHistory model.
    """
    def test_show_creation(self):
        """
        Test case for creating a SearchHistory object.
        """
        test_user = AppUser.objects.create(username='Test User', email='test@gmail.com')
        search_history = SearchHistory.objects.create(
            user=test_user,
            city='kielce',
            showing_date='2023-06-01',
            created_date='2023-06-04 16:54:38.070959+00',
        )
        self.assertEqual(search_history.user.username, 'Test User')
        self.assertEqual(search_history.city, 'kielce')
        self.assertEqual(search_history.showing_date, '2023-06-01')
        self.assertEqual(search_history.created_date, '2023-06-04 16:54:38.070959+00')
