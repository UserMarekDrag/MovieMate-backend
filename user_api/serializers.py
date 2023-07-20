from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .validations import custom_validation

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    class Meta:
        model = UserModel
        fields = '__all__'

    def validate(self, data):
        """
        Apply custom validation to user registration data.
        """
        custom_validation(data)
        return data

    def create(self, validated_data):
        """
        Create a new user instance.
        """
        user_obj = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return {'username': user_obj.username, 'email': user_obj.email}


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validates the user credentials
        """
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise exceptions.ValidationError('Invalid credentials')

        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token.key, 'user': user}

    def create(self, validated_data):
        """
        Not used, included for completeness of Serializer implementation.
        """
        raise NotImplementedError("Method 'create' not implemented.")

    def update(self, instance, validated_data):
        """
        Not used, included for completeness of Serializer implementation.
        """
        raise NotImplementedError("Method 'update' not implemented.")


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User instances.
    """
    class Meta:
        model = UserModel
        fields = ('email', 'username')


class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        """
        Check that the old password is correct and the new passwords match.
        """
        if not self.context['request'].user.check_password(data['old_password']):
            raise ValidationError({'old_password': 'Wrong password.'})

        if data['new_password'] != data['new_password2']:
            raise ValidationError({'new_password': 'Passwords must match.'})

        custom_validation({'password': data['new_password']})

        return data

    def create(self, validated_data):
        """
        Not used, included for completeness of Serializer implementation.
        """
        raise NotImplementedError("Method 'create' not implemented.")

    def update(self, instance, validated_data):
        """
        Not used, included for completeness of Serializer implementation.
        """
        raise NotImplementedError("Method 'update' not implemented.")
