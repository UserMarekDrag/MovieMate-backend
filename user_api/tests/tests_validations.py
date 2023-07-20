from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password as django_validate_password
from user_api.validations import custom_validation


class CustomValidationTestCase(TestCase):
    """
    Test case for the custom validation.
    """

    def test_custom_validation(self):
        """
        Test the custom_validation function.
        """
        valid_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'Newpassword123'
        }

        invalid_data = {
            'email': 'testuser@example.com',
            'username': 'newuser',
            'password': '123'  # password is less than 8 characters
        }

        # Test with valid data
        try:
            custom_validation(valid_data)
        except ValidationError:
            self.fail("custom_validation() raised ValidationError unexpectedly!")

        # Test with invalid data
        with self.assertRaises(ValidationError):
            custom_validation(invalid_data)

    def test_django_password_validation(self):
        """
        Test Django's built-in password validation function.
        """
        valid_password = 'Newpassword123'
        invalid_password = '123'  # password is less than 8 characters

        # Test with valid password
        try:
            django_validate_password(valid_password)
        except ValidationError:
            self.fail("django_validate_password() raised ValidationError unexpectedly!")

        # Test with invalid password
        with self.assertRaises(ValidationError):
            django_validate_password(invalid_password)
