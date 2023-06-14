from django.test import TestCase
from user_api.serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from user_api.models import AppUser


class UserSerializerTestCase(TestCase):
    """
    Test case for the user serializers.
    """
    def setUp(self):
        """
        Set up the test by creating a user instance and serializer.
        """
        self.user = AppUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )
        self.user_serializer = UserSerializer(instance=self.user)

    def test_user_serializer(self):
        """
        Test the UserSerializer.
        """
        data = self.user_serializer.data
        self.assertEqual(set(data.keys()), set(['email', 'username']))
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['username'], self.user.username)


class UserRegisterSerializerTestCase(TestCase):
    """
    Test case for the user registration serializers.
    """
    def setUp(self):
        """
        Set up the test by creating a user data dictionary and serializer.
        """
        self.user_data = {
            'email': 'testuser2@example.com',
            'username': 'testuser2',
            'password': 'password123'
        }
        self.serializer = UserRegisterSerializer(data=self.user_data)

    def test_user_register_serializer(self):
        """
        Test the UserRegisterSerializer.
        """
        self.assertTrue(self.serializer.is_valid())
        user = self.serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))


class UserLoginSerializerTestCase(TestCase):
    """
    Test case for the user login serializers.
    """
    def setUp(self):
        """
        Set up the test by creating a user instance, login data dictionary, and serializer.
        """
        self.user = AppUser.objects.create_user(
            email='testuser3@example.com',
            username='testuser3',
            password='password123'
        )
        self.login_data = {
            'email': 'testuser3@example.com',
            'password': 'password123'
        }
        self.login_serializer = UserLoginSerializer(data=self.login_data)

    def test_user_login_serializer(self):
        """
        Test the UserLoginSerializer.
        """
        self.assertTrue(self.login_serializer.is_valid())
        user = self.login_serializer.check_user(self.login_serializer.validated_data)
        self.assertEqual(user, self.user)
