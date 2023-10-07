from django.core.mail import send_mail
from django.http import HttpResponse


def send_test_email(request):
    """Send an email on verify address email"""
    send_mail(
        'Test Subject',
        'Test message body.',
        'moviemate.md@gmail.com',
        ['marekdrag@gmail.com']
    )
