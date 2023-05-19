from datetime import datetime
from .models import Film, Cinema, Showtime, ScraperData
from .scraper import get_movie_info
from celery import shared_task


@shared_task
def scrape_and_store_data():
    """
    Task that scrapes movie data for selected cities and stores it in the database.
    """
    # Here, add the list of cities you want to scrape
    cities = ["kielce", "gdansk", "krakow", "lublin"]

    for city in cities:
        # Search for the cinema, if it doesn't exist - create a new one
        cinema, created = Cinema.objects.get_or_create(name=city)
        if created:
            cinema.url = f"https://multikino.pl/repertuar/{city}/teraz-gramy"
            cinema.save()

        # Save the scraping date
        scraper_data = ScraperData.objects.create(cinema=cinema)

        # Get today's date and fetch movie data
        today = datetime.today().strftime('%Y-%m-%d')
        movie_info_list = get_movie_info(city, today)

        for movie_info in movie_info_list:
            # Create a new film if it doesn't exist
            film, created = Film.objects.get_or_create(title=movie_info['title'], cinema=cinema)

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
                    cinema=cinema,
                    date=today,
                    time=show_time,
                    booking_link=show_info['booking_link']
                )
