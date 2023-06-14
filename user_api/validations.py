from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def custom_validation(data):
    """
    Perform custom validation on user data.

    This function checks if the provided email, username, and password are valid and not already in use.
    It raises a ValidationError if any of these checks fail.

    Args:
        data (dict): User data containing 'email', 'username', and 'password'.
    Returns:
        dict: The original data if all checks pass.
    """
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('choose another email')

    if not password or len(password) < 8:
        raise ValidationError('choose another password, min 8 characters')

    if not username:
        raise ValidationError('choose another username')
    return data


def validate_email(data):
    """
    Validate email data.

    This function checks if the provided email is valid.
    It raises a ValidationError if this check fails.

    Args:
        data (dict): User data containing 'email'.
    Returns:
        bool: True if the check passes.
    """
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True


def validate_username(data):
    """
    Validate username data.

    This function checks if the provided username is valid.
    It raises a ValidationError if this check fails.

    Args:
        data (dict): User data containing 'username'.
    Returns:
        bool: True if the check passes.
    """
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True


def validate_password(data):
    """
    Validate password data.

    This function checks if the provided password is valid.
    It raises a ValidationError if this check fails.

    Args:
        data (dict): User data containing 'password'.
    Returns:
        bool: True if the check passes.
    """
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True
