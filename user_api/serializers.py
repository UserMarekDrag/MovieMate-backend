from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
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
        Validate user registration data.
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
        return user_obj


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

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

    def check_user(self, clean_data):
        """
        Check user with given credentials.
        """
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise exceptions.ValidationError('user not found')
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User instances.
    """
    class Meta:
        model = UserModel
        fields = ('email', 'username')
