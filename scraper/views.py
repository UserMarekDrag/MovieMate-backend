from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CinemaSerializer, FilmSerializer, ShowtimeSerializer, ScraperDataSerializer
from .models import Cinema, Film, Showtime, ScraperData


def get(request):
    city = request.GET.get('city')
    showing_date = request.GET.get('showing_date')

    # Find the cinema(s) in the requested city
    cinemas = Cinema.objects.filter(name__icontains=city)

    # Find the ScraperData object(s) for the requested date and cinema(s)
    scraper_data = ScraperData.objects.filter(
        cinema__in=cinemas,
        scraped_date=timezone.datetime.strptime(showing_date, '%Y-%m-%d').date()
    ).order_by('-scraped_date')

    # Find the Film object(s) for the requested cinema(s)
    films = Film.objects.filter(cinema__in=cinemas)

    # Find the Showtime object(s) for the requested date and film(s)
    showtimes = Showtime.objects.filter(
        film__in=films,
        date=timezone.datetime.strptime(showing_date, '%Y-%m-%d').date()
    ).order_by('time')

    cinema_data = CinemaSerializer(cinemas, many=True).data
    film_data = FilmSerializer(films, many=True).data
    showtime_data = ShowtimeSerializer(showtimes, many=True).data
    scraper_data = ScraperDataSerializer(scraper_data, many=True).data

    data = {
        'cinemas': cinema_data,
        'films': film_data,
        'showtimes': showtime_data,
        'scraper_data': scraper_data,
    }

    return Response(data)


class MovieDataView(APIView):
    pass