from datetime import datetime
from .models import Film, Cinema, Showtime, ScraperData, City
from .scraper import get_movie_info_from_multikino
from celery import shared_task


@shared_task
def scrape_and_store_data():
    """
    Task that scrapes movie data for selected cities and stores it in the database.
    """
    # Here, add the list of cities you want to scrape
    cities = ["kielce", "gdansk", "krakow", "lublin"]
    cinema_name = 'multikino'

    # Get today's date and fetch movie data
    today = datetime.today().strftime('%Y-%m-%d')

    # Save the scraping date
    scraper_data = ScraperData.objects.create(date=today)

    # Search for the cinema, if it doesn't exist - create a new one
    cinema, created = Cinema.objects.get_or_create(name=cinema_name)
    if created:
        cinema.name = cinema_name
        cinema.url = f"https://multikino.pl/"
        cinema.save()

    for city in cities:
        # Search for the cinema and city, if it doesn't exist - create a new one
        cinema_in_city, created = City.objects.get_or_create(name=city, cinema=cinema, data=scraper_data)
        if created:
            cinema_in_city.name = city
            cinema_in_city.url = f"https://multikino.pl/{city}"
            cinema_in_city.save()

        movie_info_list = get_movie_info_from_multikino(city, today)

        for movie_info in movie_info_list:
            # Create a new film if it doesn't exist
            film, created = Film.objects.get_or_create(title=movie_info['title'], city=cinema_in_city)

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
                    city=cinema_in_city,
                    time=show_time,
                    booking_link=show_info['booking_link']
                )
