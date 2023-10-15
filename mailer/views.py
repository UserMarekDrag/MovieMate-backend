from django.core.mail import send_mail


def send_verification_email(user, verification_url):
    """
    Send an email to the user containing the verification link.
    Args:
        user (AppUser): User instance to whom the email should be sent.
        verification_url (str): Verification link for the user.
    Returns:
        int: Number of successfully sent emails.
    """
    email_subject = "Registration Confirmation"
    email_body = f"""
    Hello {user.username},

    Thank you for registering with us. Please click the link below to activate your account:
    {verification_url}

    If you did not initiate this request, kindly ignore this email.

    Best regards,
    MovieMate
    """
    send_mail(email_subject, email_body, 'moviemate.md@gmail.com', [user.email])
