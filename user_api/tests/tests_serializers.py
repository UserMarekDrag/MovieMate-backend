from django.test import TestCase, RequestFactory
from user_api.serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, \
    UserChangePasswordSerializer
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
            'password': 'Testuser123!'
        }
        self.serializer = UserRegisterSerializer(data=self.user_data)

    def test_user_register_serializer(self):
        """
        Test the UserRegisterSerializer.
        """
        self.assertTrue(self.serializer.is_valid(), self.serializer.errors)
        user = self.serializer.save()
        self.assertEqual(user['email'], self.user_data['email'])
        self.assertEqual(user['username'], self.user_data['username'])


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
        user = self.login_serializer.validated_data['user']
        self.assertEqual(user, self.user)


class UserChangePasswordSerializerTestCase(TestCase):
    """
    Test case for the password change serializers.
    """

    def setUp(self):
        """
        Set up the test by creating a user instance and a request context.
        """
        self.user = AppUser.objects.create_user(
            email='testuser4@example.com',
            username='testuser4',
            password='password123'
        )
        self.factory = RequestFactory()
        self.context = {
            'request': self.factory.get('/api-user/change/')
        }
        self.context['request'].user = self.user

    def test_passwords_match(self):
        """
        Test that the new passwords match.
        """
        data = {
            'old_password': 'password123',
            'new_password': 'new_password123',
            'new_password2': 'new_password123',
        }
        serializer = UserChangePasswordSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_passwords_do_not_match(self):
        """
        Test that the new passwords do not match.
        """
        data = {
            'old_password': 'password123',
            'new_password': 'new_password123',
            'new_password2': 'wrong_password123',
        }
        serializer = UserChangePasswordSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('new_password', serializer.errors)

    def test_old_password_is_incorrect(self):
        """
        Test that the old password is incorrect.
        """
        data = {
            'old_password': 'wrong_password123',
            'new_password': 'new_password123',
            'new_password2': 'new_password123',
        }
        serializer = UserChangePasswordSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn('old_password', serializer.errors)
