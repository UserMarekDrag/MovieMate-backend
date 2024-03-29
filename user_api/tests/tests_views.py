from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterViewTestCase(APITestCase):
    """
    Test case for the user registration view.
    """

    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient.
        """
        self.client = APIClient()

    def test_user_register_view(self):
        """
        Test the user registration view.
        """
        response = self.client.post('/api-user/register/',
                                    {'email': 'test@example.com',
                                     'username': 'test',
                                     'password': 'Test1234!'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['username'], 'test')


class UserLoginViewTestCase(APITestCase):
    """
    Test case for the user login view.
    """

    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient and a user instance.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test1234',
            is_active=True
        )

    def test_user_login_view(self):
        """
        Test the user login view.
        """
        response = self.client.post('/api-user/login/', {'email': 'test@example.com', 'password': 'test1234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)


class UserLogoutViewTestCase(APITestCase):
    """
    Test case for the user logout view.
    """

    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient, a user instance, and authenticating the client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test1234',
            is_active=True
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """
        Authentication with Token Auth
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_logout_view(self):
        """
        Test the user logout view.
        """
        response = self.client.post('/api-user/logout/')
        self.assertEqual(response.status_code, 200)


class UserViewTestCase(APITestCase):
    """
    Test case for the user view.
    """

    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient, a user instance, and authenticating the client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test1234',
            is_active=True
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """
        Authentication with Token Auth
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_view(self):
        """
        Test the user view.
        """
        response = self.client.get('/api-user/user/')
        self.assertEqual(response.status_code, 200)


class UserChangePasswordViewTestCase(APITestCase):
    """
    Test case for the user password changed.
    """

    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient, a user instance, and authenticating the client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Test1234!',
            is_active=True
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """
        Authentication with Token Auth
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_change_password_view(self):
        """
        Test the user changed his password view.
        """
        response = self.client.put('/api-user/change/', {
                                    'old_password': 'Test1234!',
                                    'new_password': 'Test12345!',
                                    'new_password2': 'Test12345!'
                                    })
        self.assertEqual(response.status_code, 200)


class UserDeleteViewTestCase(APITestCase):
    """
    Test case for the user accounts delete.
    """

    def setUp(self):
        """
        Set up the test by creating an instance of the APIClient, a user instance, and authenticating the client.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='Test1234!',
            is_active=True
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """
        Authentication with Token Auth
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_delete_account_view(self):
        """
        Test the user delete his accounts view.
        """
        response = self.client.delete('/api-user/delete/')
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='test')
