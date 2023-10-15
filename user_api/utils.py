from decouple import config


def generate_verification_url(token):
    """
    Generate a verification URL for email confirmation using the given token.
    Args:
        token (uuid.UUID): Verification token.
    Returns:
        str: Full verification URL.
    """
    base_url = config('FRONTEND_BASE_URL')
    verification_path = f"/verify-email/{token}/"
    return base_url + verification_path
