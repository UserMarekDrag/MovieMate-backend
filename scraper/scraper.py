import logging
from abc import ABC, abstractmethod
from contextlib import contextmanager
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

# Constants
CHROMEDRIVER_PATH = 'chromedriver'
WAIT_TIME_MULTIKINO = 300
WAIT_TIME_HELIOS = 60
MULTIKINO_URL_FORMAT = 'https://multikino.pl/repertuar/{}/teraz-gramy?data={}'
HELIOS_URL_FORMAT = 'https://www.helios.pl/{},{}/Repertuar/index/dzien/{}/kino/{}'

# Setup logging
logging.basicConfig(filename='/tmp/movie_scraper.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


class WebDriverManager:
    """
    Class for initializing and cleaning up the Chrome driver.
    """
    @contextmanager
    def get_chrome_driver(self):
        """
        Context manager for initializing and cleaning up the Chrome driver.
        """
        service = Service(CHROMEDRIVER_PATH)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=service, options=options)
        try:
            yield driver
        finally:
            driver.quit()


class BaseMovieScraper(ABC, WebDriverManager):
    """
    Abstract base class for movie scrapers.
    """
    URL_FORMAT = None

    @abstractmethod
    def get_movie_info(self, city, showing_date, cinema_numb=None):
        """
        Abstract method for getting movie information.
        """
        raise NotImplementedError


class MultikinoScraper(BaseMovieScraper):
    """
    Movie scraper for Multikino website.
    """
    URL_FORMAT = MULTIKINO_URL_FORMAT

    def get_movie_info(self, city, showing_date, cinema_numb=None):
        """
        This function uses Selenium and BeautifulSoup to scrape the Multikino website
        and get information about movies that are currently playing in the given city
        on the specified showing date.

        Args:
            city (str): The name of the city where the cinema is located.
            showing_date (str): The date in format DD-MM-YYYY for which movie information is to be retrieved.

        Returns:
            A list of dictionaries, where each dictionary represents information about a single movie.
            Each dictionary has the following keys:
            - title (str): The title of the movie.
            - description (str): The description of the movie.
            - hour (str): The time when the movie is playing.
            - booking_link (str): The link for booking the movie.
        """
        movie_info_list_multikino = []
        try:
            url = self.URL_FORMAT.format(city, showing_date)
            with self.get_chrome_driver() as driver:
                driver.get(url)
                wait = WebDriverWait(driver, WAIT_TIME_MULTIKINO)
                wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'filmlist__item')))
                film_items = driver.find_elements(By.CLASS_NAME, 'filmlist__item')

                for item in film_items:
                    driver.execute_script("arguments[0].scrollIntoView();", item)

                    # Parse the item's HTML with BeautifulSoup
                    item_html = item.get_attribute('outerHTML')
                    soup_item = BeautifulSoup(item_html, 'html.parser')

                    # Continue the process here using 'soup_item' instead of 'item'
                    title = soup_item.find('div', {'class': 'filmlist__info-txt'}).find('span',
                                                                                        {'data-v-9364a27e': True}).text

                    # Get the URL address to movie details
                    movie_url = 'https://multikino.pl' + soup_item \
                        .find('div', {'class': 'filmlist__info-txt'}) \
                        .find('a')['href']

                    category = soup_item.find('a', {
                        'class': 'film-details__item',
                        'rv-class-film-details__item--selected': 'genre.highlighted'
                    }).text.strip() if soup_item.find('a', {
                        'class': 'film-details__item',
                        'rv-class-film-details__item--selected': 'genre.highlighted'
                    }) else ''

                    description = soup_item. \
                        find('p', {'class': 'filmlist__synopsis--twoLines'}).text if soup_item. \
                        find('p', {'class': 'filmlist__synopsis--twoLines'}) else 'No description'

                    # Get the image URL
                    img_url = soup_item.find('img', {'class': 'filmlist__poster'}).get('src')

                    show_info = [{
                        'hour': time.find('time', {'class': 'default'}).text.strip().replace('*', ''),
                        'booking_link': 'https://multikino.pl' + time.find('a')['href']
                    } for time in soup_item.find_all('li', {'class': 'times__detail'})
                        if time.find('time', {'class': 'default'}) is not None]

                    # Append the extracted info to movie_info_list
                    movie_info_list_multikino.append({
                        'title': title,
                        'category': category,
                        'description': description,
                        'image_url': img_url,
                        'show_info': show_info,
                        'movie_url': movie_url
                    })

        except (WebDriverException, AttributeError) as error:

            logger.error("Error occurred: %s", str(error))

        return movie_info_list_multikino


class HeliosScraper(BaseMovieScraper):
    """
    Movie scraper for Helios website.
    """
    URL_FORMAT = HELIOS_URL_FORMAT

    def get_movie_info(self, city, day, cinema_numb):
        """
        This function uses Selenium and BeautifulSoup to scrape the Helio website
        and get information about movies that are currently playing in the given city
        on the specified showing date.

        Args:
            city (str): The name of the city where the cinema is located.
            day (int): The date where 0 == today, 1 == tomorrow, ....
            cinema_numb (int): The number of the cinema, number is unique.

        Returns:
            A list of dictionaries, where each dictionary represents information about a single movie.
            Each dictionary has the following keys:
            - title (str): The title of the movie.
            - hour (str): The time when the movie is playing.
            - booking_link (str): The link for booking the movie.
        """
        movie_info_list_helios = []
        try:
            url = self.URL_FORMAT.format(cinema_numb, city, day, cinema_numb)
            with self.get_chrome_driver() as driver:
                driver.get(url)
                wait = WebDriverWait(driver, WAIT_TIME_HELIOS)
                wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'seances-list')))
                film_items = driver.find_elements(By.XPATH, "//ul/*[contains(@class, 'seance gallery-column')]")

                for item in film_items:
                    driver.execute_script("arguments[0].scrollIntoView();", item)

                    # Parse the item's HTML with BeautifulSoup
                    item_html = item.get_attribute('outerHTML')
                    soup_item = BeautifulSoup(item_html, 'html.parser')

                    # Continue the process here using 'soup_item' instead of 'item'
                    title = soup_item.find('h2', {'class': 'movie-title'}).find('a',
                                                                                {'class': 'movie-link'}).text.strip()

                    # Get the URL address to movie details
                    movie_url = 'https://helios.pl' + soup_item \
                        .find('h2', {'class': 'movie-title'}) \
                        .find('a')['href']

                    # Get the image URL
                    img_url = soup_item.find('img').get('src')

                    show_info = [{
                        'hour': time.find('a', {'class': 'hour-link fancybox-reservation'}).text.strip(),
                        'booking_link': 'https://helios.pl' + time.find('a')['href']
                    } for time in soup_item.find_all('li', {'class': 'hour toolTipContainer'})
                        if time.find('a', {'class': 'hour-link fancybox-reservation'}) is not None]

                    if show_info:
                        # Append the extracted info to movie_info_list
                        movie_info_list_helios.append({
                            'title': title,
                            'image_url': img_url,
                            'show_info': show_info,
                            'movie_url': movie_url
                        })

        except (WebDriverException, AttributeError) as error:
            logger.error("Error occurred: %s", str(error))

        return movie_info_list_helios
