from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, Mock
from scraper.tasks import add_days, BaseScrapeStore
from scraper.tasks import MultikinoScrapeStore, HeliosScrapeStore, scrape_and_store_multikino, scrape_and_store_helios
from scraper.scraper import MultikinoScraper, HeliosScraper


class TestAddDays(TestCase):
    """
    Test class for the add_days function.
    """

    def test_add_days(self):
        """
        Test case to check the add_days function.
        """
        today = datetime(2022, 10, 1)
        result = add_days(today, 4)
        self.assertEqual(result, datetime(2022, 10, 5))


class TestBaseMovieScraper(TestCase):
    """
    Test class for the BaseScrapeStore class.
    """

    def test_get_movie_info_not_implemented(self):
        """
        Test case to check that get_movie_info raises NotImplementedError.
        """
        class FakeMovieScraper(BaseScrapeStore):
            """This is a fake Movie Scraper used for testing."""
            def create_scraper(self):
                pass

            def get_dates(self):
                pass

            def scrape_and_store_data(self):
                pass

        with self.assertRaises(TypeError):
            FakeMovieScraper(["city"], "date").create_scraper()
            FakeMovieScraper(["city"], "date").get_dates()
            FakeMovieScraper(["city"], "date").scrape_and_store_data()


class TestMultikinoScrapeStore(TestCase):
    """
    Test class for the MultikinoScrapeStore class.
    """

    @patch('scraper.tasks.MultikinoScraper')
    def setUp(self, MockScraper):
        self.mock_scraper = MockScraper()
        self.multikino = MultikinoScrapeStore(["Kraków"])

    def test_create_scraper(self):
        """
        Test case to check the create_scraper method.
        """
        self.assertIsInstance(self.multikino.create_scraper(), MultikinoScraper)

    def test_get_dates(self):
        """
        Test case to check the get_dates method.
        """
        dates = self.multikino.get_dates()
        self.assertEqual(len(dates), self.multikino.AMOUNT_OF_DAYS)
        self.assertIsInstance(dates[0], str)

    def test_create_cinema(self):
        """
        Test case to check the create_cinema method.
        """
        with patch('scraper.tasks.Cinema.objects.get_or_create', return_value=(Mock(), True)) as mock_get_or_create:
            self.multikino.create_cinema('Kraków')
        mock_get_or_create.assert_called_with(
            name='multikino',
            city='Kraków',
            number=None
        )


class TestHeliosScrapeStore(TestCase):
    """
    Test class for the HeliosScrapeStore class.
    """

    @patch('scraper.tasks.HeliosScraper')
    def setUp(self, MockScraper):
        self.mock_scraper = MockScraper()
        self.helios = HeliosScrapeStore({"Kraków": 1})

    def test_create_scraper(self):
        """
        Test case to check the create_scraper method.
        """
        self.assertIsInstance(self.helios.create_scraper(), HeliosScraper)

    def test_get_dates(self):
        """
        Test case to check the get_dates method.
        """
        dates = self.helios.get_dates()
        self.assertEqual(len(dates), self.helios.AMOUNT_OF_DAYS)

        for key, value in dates.items():
            self.assertIsInstance(key, str)
            datetime.strptime(key, '%Y-%m-%d')
            self.assertIsInstance(value, int)

    def test_create_cinema(self):
        """
        Test case to check the create_cinema method.
        """
        with patch('scraper.tasks.Cinema.objects.get_or_create', return_value=(Mock(), True)) as mock_get_or_create:
            self.helios.create_cinema('Kraków', 1)
        mock_get_or_create.assert_called_with(
            name='helios',
            city='Kraków',
            number=1
        )


class TestCeleryTasks(TestCase):
    """
    Test class for the Celery tasks.
    """

    @patch('scraper.tasks.MultikinoScrapeStore.scrape_and_store_data')
    def test_scrape_and_store_multikino(self, mock_scrape_and_store_data):
        """
        Test case to check the scrape_and_store_multikino task.
        """
        scrape_and_store_multikino(["Kraków"])
        mock_scrape_and_store_data.assert_called_once()

    @patch('scraper.tasks.HeliosScrapeStore.scrape_and_store_data')
    def test_scrape_and_store_helios(self, mock_scrape_and_store_data):
        """
        Test case to check the scrape_and_store_helios task.
        """
        scrape_and_store_helios({"Kraków": 1})
        mock_scrape_and_store_data.assert_called_once()
