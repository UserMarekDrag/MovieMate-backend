from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_overview(request):
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
    queryset = Movie.objects.all()
    serializer = MovieSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, pk):
    queryset = Movie.objects.get(id=pk)
    serializer = MovieSerializer(queryset, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def movie_create(request):
    serializer = MovieSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def movie_update(request, pk):
    queryset = Movie.objects.get(id=pk)
    serializer = MovieSerializer(instance=queryset, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def movie_delete(request, pk):
    queryset = Movie.objects.get(id=pk)
    queryset.delete()

    return Response('Item successfully deleted!')