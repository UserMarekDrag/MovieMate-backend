from django.contrib.auth import get_user_model, password_validation

UserModel = get_user_model()


def custom_validation(data):
    """
    Perform custom validation on user data.

    This function checks if the provided password is valid.
    It raises a ValidationError if any of these checks fail.

    Args:
        data (dict): User data containing 'email', 'username', and 'password'.
    Returns:
        dict: The original data if all checks pass.
    """
    password = data.get('password', '').strip()

    password_validation.validate_password(password)

    return data
