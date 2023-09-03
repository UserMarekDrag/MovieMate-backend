from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from scraper.models import Show
from .models import SearchHistory
from .serializers import ShowSerializer, SearchHistorySerializer


class ApiOverview(APIView):
    """
    Returns an overview of available API endpoints.
    """
    def get(self, request):
        """
        Listing API endpoints.
        """
        api_urls = {
            'List': '/movie-history-list/',
            'Detail View': '/movie-detail/<str:pk>/',
            'Create': '/movie-create/',
            'Update': '/movie-update/<str:pk>',
            'Delete': '/movie-delete/<str:pk>',
            'Search': '/cinema_in_city>',
        }

        return Response(api_urls)


class MovieList(generics.ListAPIView):
    """
    Returns a list of movie searches.
    """
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class MovieDetail(generics.RetrieveAPIView):
    """
    Returns details of a specific movie.
    """
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class MovieCreate(generics.CreateAPIView):
    """
    Creates a new movie.
    """
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class MovieUpdate(generics.UpdateAPIView):
    """
    Updates an existing movie.
    """
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class MovieDelete(generics.DestroyAPIView):
    """
    Deletes a movie.
    """
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class ShowList(generics.ListAPIView):
    """
    API endpoint for listing shows based on filters.
    """
    permission_classes = [AllowAny]  # Authorization off
    serializer_class = ShowSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        """
        Get a queryset of Show objects filtered by the provided query parameters.

        The queryset can be filtered by 'cinema__city' and 'date'. If 'cinema__city' is provided in the query
        parameters, the queryset will be filtered to include only shows in cinemas in cities that start with
        the provided string. If 'date' is provided, the queryset will be filtered to include only shows on that date.

        Returns:
        QuerySet: The queryset of Show objects, filtered according to the provided query parameters.
        """
        queryset = Show.objects.all()
        city = self.request.query_params.get('cinema__city', None)
        date = self.request.query_params.get('date', None)
        if city is not None:
            queryset = queryset.filter(cinema__city__startswith=city)
        if date is not None:
            queryset = queryset.filter(date=date)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Overridden list method to implement search history logging.

        This method logs the search history of a user if they are authenticated.
        The user's city and the date of the show they're searching for are logged if provided in the request.

        Parameters:
        request (Request): The request that triggered this method. 'cinema__city' and 'date' can be optionally provided
        in the query parameters.
        args (list): Variable length argument list.
        kwargs (dict): Arbitrary keyword arguments.

        Returns:
        Response: The HTTP response containing the serialized show data.
        """
        response = super().list(request, *args, **kwargs)

        # Get user if logged in
        user = request.user if request.user.is_authenticated else None

        # Get city and showing date from request if available
        city = request.query_params.get('cinema__city')
        showing_date = request.query_params.get('date')

        # Only save search history if city or date were part of the request
        if city or showing_date:
            SearchHistory.objects.create(
                user=user,
                city=city,
                showing_date=showing_date,
                created_date=timezone.now()
            )

        return response
