from django.test import TestCase
from user_api.models import AppUser


class UserManagerTestCase(TestCase):
    """
    Test case for the user manager methods.
    """
    def setUp(self):
        """
        Set up the test by creating user instances.
        """
        self.user1 = AppUser.objects.create_user(
            email='testuser1@example.com',
            username='testuser1',
            password='password123'
        )
        self.superuser = AppUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword'
        )

    def test_create_user(self):
        """
        Test the creation of a regular user.
        """
        self.assertEqual(self.user1.email, 'testuser1@example.com')
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertFalse(self.user1.is_superuser)

    def test_create_superuser(self):
        """
        Test the creation of a superuser.
        """
        self.assertEqual(self.superuser.email, 'admin@example.com')
        self.assertEqual(self.superuser.username, 'admin')
        self.assertTrue(self.superuser.is_superuser)

    def test_required_fields(self):
        """
        Test the required fields for user creation.
        """
        self.assertEqual(AppUser.REQUIRED_FIELDS, ['username'])
