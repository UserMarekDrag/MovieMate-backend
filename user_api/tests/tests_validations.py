from django.test import TestCase
from django.core.exceptions import ValidationError
from user_api.models import AppUser
from user_api.validations import custom_validation, validate_email, validate_username, validate_password


class CustomValidationTestCase(TestCase):
    def setUp(self):
        """
        Set up the test by creating a user instance.
        """
        self.user = AppUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )

    def test_custom_validation(self):
        """
        Test the custom_validation function.
        """
        valid_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword123'
        }

        invalid_data = {
            'email': 'testuser@example.com',  # This email already exists
            'username': '',  # username is empty
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


class ValidationMethodsTestCase(TestCase):
    def setUp(self):
        """
        Set up the test by creating valid and invalid data dictionaries.
        """
        self.valid_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword123'
        }

        self.invalid_data = {
            'email': '',  # email is empty
            'username': '',  # username is empty
            'password': ''  # password is empty
        }

    def test_validate_email(self):
        """
        Test the validate_email function.
        """
        # Test with valid data
        try:
            validate_email(self.valid_data)
        except ValidationError:
            self.fail("validate_email() raised ValidationError unexpectedly!")

        # Test with invalid data
        with self.assertRaises(ValidationError):
            validate_email(self.invalid_data)

    def test_validate_username(self):
        """
        Test the validate_username function.
        """
        # Test with valid data
        try:
            validate_username(self.valid_data)
        except ValidationError:
            self.fail("validate_username() raised ValidationError unexpectedly!")

        # Test with invalid data
        with self.assertRaises(ValidationError):
            validate_username(self.invalid_data)

    def test_validate_password(self):
        """
        Test the validate_password function.
        """
        # Test with valid data
        try:
            validate_password(self.valid_data)
        except ValidationError:
            self.fail("validate_password() raised ValidationError unexpectedly!")

        # Test with invalid data
        with self.assertRaises(ValidationError):
            validate_password(self.invalid_data)
