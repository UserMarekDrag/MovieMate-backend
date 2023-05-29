from .models import Movie
from scraper.models import ScraperAll
from .serializers import MovieSerializer, ScraperAllSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


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
    queryset = Movie.objects.all()
    serializer = MovieSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, pk):
    """
    Returns details of a specific movie.
    """
    queryset = Movie.objects.get(id=pk)
    serializer = MovieSerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def movie_create(request):
    """
    Creates a new movie.
    """
    serializer = MovieSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def movie_update(request, pk):
    """
    Updates an existing movie.
    """
    queryset = Movie.objects.get(id=pk)
    serializer = MovieSerializer(instance=queryset, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def movie_delete(request, pk):
    """
    Deletes a movie.
    """
    queryset = Movie.objects.get(id=pk)
    queryset.delete()

    return Response('Item successfully deleted!')


class CinemaInCityList(generics.ListAPIView):
    """
    API endpoint for listing cinemas in a city based on filters.
    """
    permission_classes = [AllowAny]  # Authorization off
    queryset = ScraperAll.objects.all()
    serializer_class = ScraperAllSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city_name', 'date']
