from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from .validations import custom_validation, validate_email, validate_password


class UserRegister(APIView):
    """
    Class based view for user registration.
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        """
        Handles user registration POST request.
        """
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Class based view for user login.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        """
        Handles user login POST request.
        """
        data = request.data
        if not validate_email(data) or not validate_password(data):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            user = serializer.validated_data['user']
            return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    """
    Class based view for user logout.
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        """
        Handles user logout POST request.
        """
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    """
    Class based view for retrieving user information.
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        """
        Handles GET request to retrieve user information.
        """
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
