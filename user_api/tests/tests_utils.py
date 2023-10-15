import uuid
from unittest.mock import patch
from django.test import TestCase
from decouple import config
from user_api.utils import generate_verification_url


class UtilsTestCase(TestCase):
    """
    Test case for generate varification url.
    """

    def test_generate_verification_url(self):
        """
        Test generate varification url.
        """
        # Given
        token = uuid.uuid4()
        test_base_url = config('FRONTEND_BASE_URL')

        # Mock the config method to return our test_base_url for 'FRONTEND_BASE_URL'
        with patch('user_api.utils.config', return_value=test_base_url):
            # When
            verification_url = generate_verification_url(token)

            # Then
            expected_url = f"{test_base_url}/verify-email/{token}/"
            self.assertEqual(verification_url, expected_url)
