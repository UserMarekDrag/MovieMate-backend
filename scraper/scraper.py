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
WAIT_TIME = 30

# Constants Multikino
URL_FORMAT_MULTIKINO = 'https://multikino.pl/repertuar/{}/teraz-gramy?data={}'

# Constants Helios
URL_FORMAT_HELIOS = 'https://www.helios.pl/{},{}/Repertuar/index/dzien/{}/kino/{}'


@contextmanager
def get_chrome_driver():
    """
    This context manager creates a headless Chrome WebDriver instance,
    manages its lifecycle, and cleans up after it is done.
    """
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome without UI
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # Disable sandbox for containers
    options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage

    driver = webdriver.Chrome(service=service, options=options)
    try:
        yield driver
    finally:
        driver.quit()


def get_movie_info_from_multikino(city, showing_date):
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
        url = URL_FORMAT_MULTIKINO.format(city, showing_date)
        with get_chrome_driver() as driver:
            driver.get(url)

            wait = WebDriverWait(driver, WAIT_TIME)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'filmlist__item')))

            film_items = driver.find_elements(By.CLASS_NAME, 'filmlist__item')

            for item in film_items:
                driver.execute_script("arguments[0].scrollIntoView();", item)

                # now you have to parse the item's HTML with BeautifulSoup
                item_html = item.get_attribute('outerHTML')
                soup_item = BeautifulSoup(item_html, 'html.parser')

                # Continue the process here using 'soup_item' instead of 'item'
                title = soup_item.find('div', {'class': 'filmlist__info-txt'}).find('span',
                                                                                    {'data-v-9364a27e': True}).text

                category = soup_item.find('a', {
                    'class': 'film-details__item',
                    'rv-class-film-details__item--selected': 'genre.highlighted'
                }).text.strip() if soup_item.find('a', {
                    'class': 'film-details__item',
                    'rv-class-film-details__item--selected': 'genre.highlighted'
                }) else ''

                description = soup_item.\
                    find('p', {'class': 'filmlist__synopsis--twoLines'}).text if soup_item.\
                    find('p', {'class': 'filmlist__synopsis--twoLines'}) else 'No description'

                # Get the image URL
                img_url = soup_item.find('img').get('src')

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
                    'show_info': show_info
                })

    except (WebDriverException, AttributeError) as e:
        print(f"Error occurred: {str(e)}")

    return movie_info_list_multikino


def get_movie_info_helios(city, day, cinema_numb):
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
        url = URL_FORMAT_HELIOS.format(cinema_numb, city, day, cinema_numb)
        with get_chrome_driver() as driver:
            driver.get(url)

            wait = WebDriverWait(driver, WAIT_TIME)
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'seances-list')))

            film_items = driver.find_elements(By.XPATH, "//ul/*[contains(@class, 'seance gallery-column')]")

            for item in film_items:
                driver.execute_script("arguments[0].scrollIntoView();", item)

                # now you have to parse the item's HTML with BeautifulSoup
                item_html = item.get_attribute('outerHTML')
                soup_item = BeautifulSoup(item_html, 'html.parser')

                # Continue the process here using 'soup_item' instead of 'item'
                title = soup_item.find('h2', {'class': 'movie-title'}).find('a', {'class': 'movie-link'}).text.strip()

                show_info = [{
                    'hour': time.find('a', {'class': 'hour-link fancybox-reservation'}).text.strip(),
                    'booking_link': 'https://helios.pl' + time.find('a')['href']
                } for time in soup_item.find_all('li', {'class': 'hour toolTipContainer'})
                    if time.find('a', {'class': 'hour-link fancybox-reservation'}) is not None]

                if show_info:
                    # Append the extracted info to movie_info_list
                    movie_info_list_helios.append({
                        'title': title,
                        'show_info': show_info
                    })

    except (WebDriverException, AttributeError) as e:
        print(f"Error occurred: {str(e)}")

    return movie_info_list_helios
