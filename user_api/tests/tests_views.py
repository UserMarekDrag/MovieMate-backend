from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegisterViewTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient.
        """
        self.client = APIClient()

    def test_user_register_view(self):
        """
        Test the user registration view.
        """
        response = self.client.post('/api/register/', {'email': 'test@example.com', 'username': 'test', 'password': 'test1234'})
        self.assertEqual(response.status_code, 201)


class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient and a user instance.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='test1234')

    def test_user_login_view(self):
        """
        Test the user login view.
        """
        response = self.client.post('/api/login/', {'email': 'test@example.com', 'password': 'test1234'})
        self.assertEqual(response.status_code, 200)


class UserLogoutViewTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient, a user instance, and authenticating the client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='test1234')
        self.client.force_authenticate(user=self.user)

    def test_user_logout_view(self):
        """
        Test the user logout view.
        """
        response = self.client.post('/api/logout/')
        self.assertEqual(response.status_code, 200)


class UserViewTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient, a user instance, and authenticating the client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email='test@example.com', password='test1234')
        self.client.force_authenticate(user=self.user)

    def test_user_view(self):
        """
        Test the user view.
        """
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, 200)
