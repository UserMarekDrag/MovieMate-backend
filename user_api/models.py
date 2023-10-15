import uuid

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class AppUserManager(BaseUserManager):
    """
    Custom manager for `AppUser` model.
    """

    def create_user(self, email, username, password=None, **kwargs):
        """
        Create and save a User with the given email, username, and password.
        """
        if not email:
            raise ValueError('An email is required.')
        if not username:
            raise ValueError('A username is required.')
        if not password:
            raise ValueError('A password is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        """
        Create and save a SuperUser with the given email, username, and password.
        """
        if not email:
            raise ValueError('An email is required.')
        if not username:
            raise ValueError('A username is required.')
        if not password:
            raise ValueError('A password is required.')
        user = self.create_user(email, username, password, is_staff=True, is_superuser=True, is_active=True)
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    """
    Main user model for the application. It uses email as the unique identifier.
    """
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AppUserManager()

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    """
    Model to store the verification tokens for email confirmation of users.
    """
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expiry_date = models.DateTimeField()

    @classmethod
    def generate_token_for_user(cls, user):
        """
        Generate a unique token for user email verification.
        Args:
            user (AppUser): User instance for whom the token is to be generated.
        Returns:
            uuid.UUID: Generated unique token.
        """
        token = uuid.uuid4()
        expiry_date = timezone.now() + timezone.timedelta(days=1)
        verification_token = cls(user=user, token=token, expiry_date=expiry_date)
        verification_token.save()
        return token
