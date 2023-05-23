from datetime import datetime
from datetime import timedelta
from .models import Film, Cinema, Showtime, ScraperData, City, CinemaInCity
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
    AMOUNT_OF_DAYS = 2
    dates = []

    for i in range(AMOUNT_OF_DAYS):
        showing_date = add_days(today, i)
        dates.append(showing_date.strftime('%Y-%m-%d'))

    # Search for the cinema, if it doesn't exist - create a new one
    cinema, created = Cinema.objects.get_or_create(name=cinema_name)
    if created:
        cinema.name = cinema_name
        cinema.url = f"https://multikino.pl/"
        cinema.save()

    # Save the scraping date
    for date in dates:
        scraper_data, created = ScraperData.objects.get_or_create(date=date)

        for city_name in cities:

            city, created = City.objects.get_or_create(name=city_name)

            # Search for the cinema and city, if it doesn't exist - create a new one
            cinema_in_city, created = CinemaInCity.objects.get_or_create(city=city, cinema=cinema, data=scraper_data)
            if created:
                cinema_in_city.name = city
                cinema_in_city.url = f"https://multikino.pl/{city_name}"
                cinema_in_city.save()

            movie_info_list = get_movie_info_from_multikino(city_name, date)

            for movie_info in movie_info_list:
                # Create a new film if it doesn't exist
                film, created = Film.objects.get_or_create(
                    title=movie_info['title'],
                    cinema_in_city=cinema_in_city
                )

                if created:
                    film.description = movie_info['description']
                    film.category = movie_info['category']
                    film.image_url = movie_info['image_url']
                    film.save()

                for show_info in movie_info['show_info']:
                    # Convert the time to the TimeField format
                    show_time = datetime.strptime(show_info['hour'], '%H:%M').time()

                    # Create a new Showtime if it doesn't exist
                    showtime, created = Showtime.objects.get_or_create(
                        film=film,
                        city=city,
                        time=show_time,
                        booking_link=show_info['booking_link']
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

    for i in range(1, AMOUNT_OF_DAYS):
        showing_date = add_days(today, i)
        dates[(showing_date.strftime('%Y-%m-%d'))] = i

    # Search for the cinema, if it doesn't exist - create a new one
    cinema, created = Cinema.objects.get_or_create(name=cinema_name)
    if created:
        cinema.name = cinema_name
        cinema.url = f"https://helios.pl/"
        cinema.save()

    # Save the scraping date
    for date in dates:
        data_number = dates[date]
        scraper_data, created = ScraperData.objects.get_or_create(date=date)

        for city_name in cities:
            cinema_number_in_city = cities[city_name]
            city, created = City.objects.get_or_create(name=city_name)

            # Search for the cinema and city, if it doesn't exist - create a new one
            cinema_in_city, created = CinemaInCity.objects.get_or_create(city=city, cinema=cinema, data=scraper_data)
            if created:
                cinema_in_city.name = city
                cinema_in_city.url = f"https://www.helios.pl/{cinema_number_in_city},{city_name}"
                cinema_in_city.save()

            movie_info_list = get_movie_info_helios(city_name, data_number, cinema_number_in_city)

            for movie_info in movie_info_list:
                # Create a new film if it doesn't exist
                film, created = Film.objects.get_or_create(
                    title=movie_info['title'],
                    cinema_in_city=cinema_in_city
                )

                if created:
                    film.save()

                for show_info in movie_info['show_info']:
                    # Convert the time to the TimeField format
                    try:
                        show_time = datetime.strptime(show_info['hour'], '%H:%M').time()
                    except ValueError:
                        print(f"Could not convert time: {show_info['hour']}")
                        continue

                    # Create a new Showtime if it doesn't exist
                    showtime, created = Showtime.objects.get_or_create(
                        film=film,
                        city=city,
                        time=show_time,
                        booking_link=show_info['booking_link']
                    )
