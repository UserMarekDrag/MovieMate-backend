from contextlib import contextmanager
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


# Constants
CHROMEDRIVER_PATH = 'drivers/chromedriver.exe'
URL_FORMAT = 'https://multikino.pl/repertuar/{}/teraz-gramy?data={}'
WAIT_TIME = 10


@contextmanager
def get_chrome_driver():
    """
    This context manager creates a headless Chrome WebDriver instance,
    manages its lifecycle, and cleans up after it is done.
    """
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # run Chrome in headless mode
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_movie_info(city, showing_date):
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
    try:
        # Navigate to the page
        url = URL_FORMAT.format(city, showing_date)
        with get_chrome_driver() as driver:
            driver.get(url)

            # Wait for the page to load
            wait = WebDriverWait(driver, WAIT_TIME)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'filmlist__item')))

            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find the film list
            film_list = soup.find('div', {'class': 'filmlist container container-small expand-small'})

            # Find the film items and get the information
            film_items = film_list.find_all('div', {'class': 'filmlist__item'})
            movie_info_list = [
                {
                    'title': item.find('div', {'class': 'filmlist__info-txt'}).find('span',
                                                                                    {'data-v-9364a27e': True}).text,
                    'description': item.find('p', {'class': 'filmlist__synopsis--twoLines'}).text
                    if item.find('p', {'class': 'filmlist__synopsis--twoLines'}) else 'No description',

                    'show_info': [
                                {
                                    'hour': time.find('time', {'class': 'default'}).text.strip(),
                                    'booking_link': 'https://multikino.pl' + time.find('a')['href']
                                }
                                for time in item.find_all('li', {'class': 'times__detail'})
                                if time.find('time', {'class': 'default'}) is not None
                             ]
                }
                for item in film_items
            ]

            return movie_info_list

    except (WebDriverException, AttributeError) as e:
        print(f"Error occurred: {str(e)}")
        return []
