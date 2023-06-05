from django.urls import path
from .views import ShowList, ApiOverview, MovieList, MovieDetail, MovieCreate, MovieUpdate, MovieDelete


urlpatterns = [
    path('', ApiOverview.as_view(), name='api-overview'),
    path('movie-list/', MovieList.as_view(), name='movie-list'),
    path('movie-detail/<str:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('movie-create/', MovieCreate.as_view(), name='movie-create'),
    path('movie-update/<str:pk>/', MovieUpdate.as_view(), name='movie-update'),
    path('movie-delete/<str:pk>/', MovieDelete.as_view(), name='movie-delete'),
    path('cinemas_in_city/', ShowList.as_view(), name='cinema_in_city_list'),
]
