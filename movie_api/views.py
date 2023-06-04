from .models import SearchHistory
from scraper.models import Show
from .serializers import MovieSerializer, ShowSerializer, SearchHistorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone


@api_view(['GET'])
def api_overview(request):
    """
    Returns an overview of available API endpoints.
    """
    api_urls = {
        'List': '/movie-list/',
        'Detail View': '/movie-detail/<str:pk>/',
        'Create': '/movie-create/',
        'Update': '/movie-update/<str:pk>',
        'Delete': '/movie-delete/<str:pk>',
    }

    return Response(api_urls)


@api_view(['GET'])
def movie_list(request):
    """
    Returns a list of movies.
    """
    queryset = SearchHistory.objects.all()
    serializer = SearchHistorySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, pk):
    """
    Returns details of a specific movie.
    """
    queryset = SearchHistory.objects.get(id=pk)
    serializer = SearchHistorySerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def movie_create(request):
    """
    Creates a new movie.
    """
    serializer = SearchHistorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def movie_update(request, pk):
    """
    Updates an existing movie.
    """
    queryset = SearchHistory.objects.get(id=pk)
    serializer = SearchHistorySerializer(instance=queryset, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def movie_delete(request, pk):
    """
    Deletes a movie.
    """
    queryset = SearchHistory.objects.get(id=pk)
    queryset.delete()

    return Response('Item successfully deleted!')


class ShowList(generics.ListAPIView):
    """
    API endpoint for listing shows based on filters.
    """
    permission_classes = [AllowAny]  # Authorization off
    queryset = Show.objects.all()
    serializer_class = ShowSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cinema__city', 'date']

    def list(self, request, *args, **kwargs):
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
