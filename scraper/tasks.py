from datetime import datetime
from datetime import timedelta
from .models import Cinema, Movie, Show
from .scraper import get_movie_info_from_multikino, get_movie_info_helios
from celery import shared_task


def add_days(today, num_of_days):
    return today + timedelta(days=num_of_days)


@shared_task
def scrape_and_store_data_multikino():
    """
    Task that scrapes movie data for selected cities and stores it in the database.
    """
    # List of cities to scrape
    cities = ["kielce", "gdansk", "krakow", "lublin"]
    cinema_name = 'multikino'

    # Get today's date and fetch movie data
    today = datetime.today()
    AMOUNT_OF_DAYS = 3
    dates = []

    for i in range(AMOUNT_OF_DAYS):
        showing_date = add_days(today, i)
        dates.append(showing_date.strftime('%Y-%m-%d'))

    # Save the scraping date
    for date in dates:
        for city_name in cities:
            movie_info_list = get_movie_info_from_multikino(city_name, date)

            for movie_info in movie_info_list:
                for show_info in movie_info['show_info']:
                    show_time = datetime.strptime(show_info['hour'], '%H:%M').time()

                    booking_link = show_info['booking_link']

                    # Get or create the cinema
                    cinema, _ = Cinema.objects.get_or_create(
                        name=cinema_name,
                        city=city_name
                    )

                    # Get or create the movie
                    movie, _ = Movie.objects.get_or_create(
                        title=movie_info['title'],
                        defaults={
                            'category': movie_info['category'],
                            'description': movie_info['description'],
                            'image_url': movie_info['image_url'],
                        }
                    )

                    # Create a new show if it doesn't exist
                    Show.objects.get_or_create(
                        booking_link=booking_link,
                        defaults={
                            'cinema': cinema,
                            'movie': movie,
                            'date': date,
                            'time': show_time,
                        },
                    )


@shared_task
def scrape_and_store_data_helios():
    """
    Task that scrapes movie data for selected cities and stores it in the database.
    """
    # List of cities and number of cinemas to scrape
    cities = {"kielce": 13, "sosnowiec": 22, "poznan": 50, "bydgoszcz": 38}
    cinema_name = 'helios'

    # Get today's date and fetch movie data
    today = datetime.today()
    AMOUNT_OF_DAYS = 3
    dates = {}

    for i in range(0, AMOUNT_OF_DAYS):
        showing_date = add_days(today, i)
        dates[(showing_date.strftime('%Y-%m-%d'))] = i

    # Save the scraping date
    for date in dates:
        data_number = dates[date]

        for city_name in cities:
            cinema_number_in_city = cities[city_name]

            movie_info_list = get_movie_info_helios(city_name, data_number, cinema_number_in_city)

            for movie_info in movie_info_list:
                for show_info in movie_info['show_info']:

                    # Convert the time to the TimeField format
                    show_time = datetime.strptime(show_info['hour'], '%H:%M').time()

                    booking_link = show_info['booking_link']

                    # Get or create the cinema
                    cinema, _ = Cinema.objects.get_or_create(
                        name=cinema_name,
                        city=city_name
                    )

                    # Get or create the movie
                    movie, _ = Movie.objects.get_or_create(
                        title=movie_info['title'],
                    )

                    # Create a new show if it doesn't exist
                    Show.objects.get_or_create(
                        booking_link=booking_link,
                        defaults={
                            'cinema': cinema,
                            'movie': movie,
                            'date': date,
                            'time': show_time,
                        },
                    )
