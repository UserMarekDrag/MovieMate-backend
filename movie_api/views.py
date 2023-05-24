from .models import Movie
from .serializers import MovieSerializer, ShowtimeSerializer
from scraper.models import Showtime, City
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.shortcuts import get_object_or_404


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


class ShowtimeList(generics.ListAPIView):
    """
    Lists showtimes for a specific city and date.
    """
    serializer_class = ShowtimeSerializer
    permission_classes = [AllowAny]  # Authorization off

    def get_queryset(self):
        city_name = self.kwargs['city']
        date = self.kwargs['date']
        city = get_object_or_404(City, name=city_name)
        return Showtime.objects.filter(city=city, film__cinema_in_city__data__date=date)
