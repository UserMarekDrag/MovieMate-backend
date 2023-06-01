from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from .models import Cinema, Movie, Show
from .scraper import MultikinoScraper, HeliosScraper
from celery import shared_task


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
        self.cities = cities
        self.cinema_name = cinema_name

    @abstractmethod
    def scrape_and_store_data(self):
        """
        Abstract method for scraping and storing movie data.
        """
        pass


class MultikinoScrapeStore(BaseScrapeStore):
    """
    Scrape and store movie data from the Multikino website.
    """
    def __init__(self, cities):
        super().__init__(cities, 'multikino')
        self.scraper = MultikinoScraper()

    def scrape_and_store_data(self):
        """
        Scrape and store movie data from the Multikino website for multiple cities and dates.
        """
        today = datetime.today()
        dates = [add_days(today, i).strftime('%Y-%m-%d') for i in range(self.AMOUNT_OF_DAYS)]

        for date in dates:
            for city_name in self.cities:
                movie_info_list = self.scraper.get_movie_info(city_name, date)

                for movie_info in movie_info_list:
                    for show_info in movie_info['show_info']:
                        show_time = datetime.strptime(show_info['hour'], '%H:%M').time()
                        booking_link = show_info['booking_link']
                        cinema, _ = Cinema.objects.get_or_create(
                            name=self.cinema_name,
                            city=city_name
                        )

                        movie, _ = Movie.objects.get_or_create(
                            title=movie_info['title'],
                            defaults={
                                'category': movie_info['category'],
                                'description': movie_info['description'],
                                'image_url': movie_info['image_url'],
                            }
                        )

                        Show.objects.get_or_create(
                            booking_link=booking_link,
                            defaults={
                                'cinema': cinema,
                                'movie': movie,
                                'date': date,
                                'time': show_time,
                            },
                        )


class HeliosScrapeStore(BaseScrapeStore):
    """
    Scrape and store movie data from the Helios website.
    """
    def __init__(self, cities):
        super().__init__(cities, 'helios')
        self.scraper = HeliosScraper()

    def scrape_and_store_data(self):
        """
        Scrape and store movie data from the Helios website for multiple cities and dates.
        """
        today = datetime.today()
        dates = {add_days(today, i).strftime('%Y-%m-%d'): i for i in range(self.AMOUNT_OF_DAYS)}
        for date in dates:
            data_number = dates[date]

            for city_name in self.cities:
                cinema_number_in_city = self.cities[city_name]
                movie_info_list = self.scraper.get_movie_info(city_name, data_number, cinema_number_in_city)

                for movie_info in movie_info_list:
                    for show_info in movie_info['show_info']:
                        show_time = datetime.strptime(show_info['hour'], '%H:%M').time()
                        booking_link = show_info['booking_link']
                        cinema, _ = Cinema.objects.get_or_create(
                            name=self.cinema_name,
                            city=city_name
                        )

                        movie, _ = Movie.objects.get_or_create(
                            title=movie_info['title'],
                        )

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
def scrape_and_store_multikino(cities):
    """
    Celery task for scraping and storing movie data from Multikino website.
    """
    scraper = MultikinoScrapeStore(cities)
    scraper.scrape_and_store_data()


@shared_task
def scrape_and_store_helios(cities):
    """
    Celery task for scraping and storing movie data from Helios website.
    """
    scraper = HeliosScrapeStore(cities)
    scraper.scrape_and_store_data()
