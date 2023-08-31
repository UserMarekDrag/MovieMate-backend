from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from celery import shared_task

from .models import Cinema, Movie, Show
from .scraper import MultikinoScraper, HeliosScraper


def add_days(today, num_of_days):
    """
    Add a specified number of days to a given date.

    Args:
        today (datetime): The starting date.
        num_of_days (int): The number of days to add.

    Returns:
        datetime: The resulting date after adding the specified number of days.
    """
    return today + timedelta(days=num_of_days)


class BaseScrapeStore(ABC):
    """
    Abstract base class for scraping and storing movie data.
    """
    AMOUNT_OF_DAYS = 4

    def __init__(self, cities, cinema_name):
        """
        Initialize the BaseScrapeStore.

        Args:
            cities (list): List of cities to scrape movie data for.
            cinema_name (str): Name of the cinema for which the data is being scraped.
        """
        self.cities = cities
        self.cinema_name = cinema_name
        self.scraper = self.create_scraper()

    @abstractmethod
    def create_scraper(self):
        """
        Create and return the scraper object.
        """

    @abstractmethod
    def get_dates(self):
        """
        Get a list of dates for which to scrape movie data.
        """

    def create_cinema(self, city_name, cinema_number=None):
        """
        Create and return a Cinema object.

        Args:
            city_name (str): Name of the city.
            cinema_number (int): Number of the cinema.

        Returns:
            Cinema: The created or retrieved Cinema object.
        """
        cinema, _ = Cinema.objects.get_or_create(
            name=self.cinema_name,
            city=city_name,
            number=cinema_number
        )
        return cinema

    @abstractmethod
    def scrape_and_store_data(self):
        """
        Scrape movie data for the specified cities and dates, and store it in the database.
        """

    @abstractmethod
    def create_movie(self, movie_info):
        """
        Create and return a Movie object.

        Args:
            movie_info (dict): Information about the movie.
        """

    def create_show(self, booking_link, cinema, movie, date, show_time):
        """
        Create and store a Show object.

        Args:
            booking_link (str): Link to book the show.
            cinema (Cinema): The Cinema object.
            movie (Movie): The Movie object.
            date (str): The date of the show in the format '%Y-%m-%d'.
            show_time (time): The time of the show.

        Returns:
            Show: The created Show object.
        """
        Show.objects.get_or_create(
            booking_link=booking_link,
            defaults={
                'cinema': cinema,
                'movie': movie,
                'date': date,
                'time': show_time,
            },
        )


class MultikinoScrapeStore(BaseScrapeStore):
    """
    Scrape and store movie data from the Multikino website.
    """
    def __init__(self, cities):
        """
        Initialize the MultikinoScrapeStore.
        """
        super().__init__(cities, 'multikino')

    def create_scraper(self):
        """
        Create and return the MultikinoScraper object.
        """
        return MultikinoScraper()

    def get_dates(self):
        """
        Get a list of dates for which to scrape movie data.
        """
        today = datetime.today()
        return [add_days(today, i).strftime('%Y-%m-%d') for i in range(self.AMOUNT_OF_DAYS)]

    def create_movie(self, movie_info):
        """
        Create and return a Movie object.

        Args:
            movie_info (dict): Information about the movie.

        Returns:
            Movie: The created or retrieved Movie object.
        """
        movie, _ = Movie.objects.get_or_create(
            title=movie_info['title'],
            defaults={
                'category': movie_info['category'],
                'description': movie_info['description'],
                'image_url': movie_info['image_url'],
                'movie_url': movie_info['movie_url'],
            }
        )
        return movie

    def scrape_and_store_data(self):
        """
        Scrape movie data from the Multikino website for the specified cities and dates,
        and store it in the database.
        """
        for date in self.get_dates():
            # Convert the date to 'DD-MM-YYYY' format for MultikinoScraper
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')

            for city_name in self.cities:
                movie_info_list = self.scraper.get_movie_info(city_name, formatted_date)

                for movie_info in movie_info_list:
                    for show_info in movie_info['show_info']:
                        show_time = datetime.strptime(show_info['hour'], '%H:%M').time()
                        booking_link = show_info['booking_link']
                        cinema = self.create_cinema(city_name)
                        movie = self.create_movie(movie_info)
                        self.create_show(booking_link, cinema, movie, date, show_time)


class HeliosScrapeStore(BaseScrapeStore):
    """
    Scrape and store movie data from the Helios website.
    """
    def __init__(self, cities):
        """
        Initialize the HeliosScrapeStore.

        Args:
            cities (dict): Dictionary of cities and cinema numbers to scrape movie data for.
        """
        super().__init__(cities, 'helios')

    def create_scraper(self):
        """
        Create and return the HeliosScraper object.
        """
        return HeliosScraper()

    def get_dates(self):
        """
        Get a dictionary of dates and the number of days from today for which to scrape movie data.
        """
        today = datetime.today()
        return {add_days(today, i).strftime('%Y-%m-%d'): i for i in range(self.AMOUNT_OF_DAYS)}

    def create_movie(self, movie_info):
        """
        Create and return a Movie object.

        Args:
            movie_info (dict): Information about the movie.

        Returns:
            Movie: The created or retrieved Movie object.
        """
        movie, _ = Movie.objects.get_or_create(
            title=movie_info['title'],
            defaults={
                'image_url': movie_info['image_url'],
                'movie_url': movie_info['movie_url'],
            }
        )
        return movie

    def scrape_and_store_data(self):
        """
        Scrape movie data from the Helios website for the specified cities, dates, and cinema numbers,
        and store it in the database.
        """
        for date, day_numb in self.get_dates().items():
            for cinema_num_in_city, city_name in self.cities.items():
                movie_info_list = self.scraper.get_movie_info(city_name, day_numb, cinema_num_in_city)

                for movie_info in movie_info_list:
                    for show_info in movie_info['show_info']:
                        try:
                            show_time = datetime.strptime(show_info['hour'], '%H:%M').time()
                        except ValueError:
                            continue
                        booking_link = show_info['booking_link']
                        cinema = self.create_cinema(city_name, cinema_num_in_city)
                        movie = self.create_movie(movie_info)
                        self.create_show(booking_link, cinema, movie, date, show_time)


@shared_task
def delete_past_shows():
    """
    Celery task for deleting past shows from the database.
    """
    today = datetime.today().date()
    Show.objects.filter(date__lt=today).delete()


@shared_task
def scrape_and_store_multikino(cities):
    """
    Celery task for scraping and storing movie data from Multikino website.

    Args:
        cities (list): List of cities to scrape movie data for.
    """
    delete_past_shows.delay()
    scraper = MultikinoScrapeStore(cities)
    scraper.scrape_and_store_data()


@shared_task
def scrape_and_store_helios(cities):
    """
    Celery task for scraping and storing movie data from Helios website.

    Args:
        cities (dict): Dictionary of cities and cinema numbers to scrape movie data for.
    """
    delete_past_shows.delay()
    scraper = HeliosScrapeStore(cities)
    scraper.scrape_and_store_data()
