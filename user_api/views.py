from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer, UserChangePasswordSerializer
from .models import AppUser


class UserRegister(APIView):
    """
    Class based view for user registration.
    """
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        """
        Handles user registration POST request.
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.validated_data['token']
            user = serializer.validated_data['user']
            return Response({'token': token, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


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


class UserChangePasswordView(APIView):
    """
    Class based view for password change.
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def put(self, request):
        """
        Handles password change PUT request.
        """
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"detail": "Successfully password changed."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    """
    Class based view for user accounts delete.
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def delete(self, request):
        """
        Handles accounts delete DELETE request.
        """
        try:
            user = AppUser.objects.get(pk=request.user.pk)
        except AppUser.DoesNotExist:
            return Response({"detail": "Error, user does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"detail": "Successfully account deleted."}, status=status.HTTP_204_NO_CONTENT)
