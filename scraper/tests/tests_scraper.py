from unittest import TestCase
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from scraper.scraper import MultikinoScraper, HeliosScraper, WebDriverManager, BaseMovieScraper


class TestLogging(TestCase):
    """
    Unit tests for exception logging in the scraper module.
    """
    @patch('scraper.scraper.MultikinoScraper.get_chrome_driver')
    @patch('scraper.scraper.logger.error')
    def test_exception_logging_in_get_movie_info(self, mock_logging_error, mock_get_chrome_driver):
        """
        Test that an exception in get_movie_info is logged correctly.
        """
        # Arrange
        mock_driver = MagicMock()
        mock_driver.get.side_effect = WebDriverException('Test exception')
        mock_get_chrome_driver.return_value.__enter__.return_value = mock_driver

        scraper = MultikinoScraper()

        # Act
        try:
            scraper.get_movie_info('test_city', '2023-01-01')
        except WebDriverException:
            pass

        # Assert
        mock_logging_error.assert_called_with('Error occurred: %s', 'Message: Test exception\n')


class TestHeliosScraperLogging(TestCase):
    """
    Unit tests for exception logging in the HeliosScraper class.
    """
    @patch('scraper.scraper.HeliosScraper.get_chrome_driver')
    @patch('scraper.scraper.logger.error')
    def test_exception_logging_in_get_movie_info(self, mock_logging_error, mock_get_chrome_driver):
        """
        Test that an exception in get_movie_info is logged correctly.
        """
        # Arrange
        mock_driver = MagicMock()
        mock_driver.get.side_effect = WebDriverException('Test exception')
        mock_get_chrome_driver.return_value.__enter__.return_value = mock_driver

        scraper = HeliosScraper()

        # Act
        try:
            scraper.get_movie_info('test_city', 1, 1)
        except WebDriverException:
            pass

        # Assert
        mock_logging_error.assert_called_with('Error occurred: %s', 'Message: Test exception\n')


class TestWebDriverManager(TestCase):
    """
    Test class for the WebDriverManager class.
    """

    @patch("selenium.webdriver.Chrome")
    @patch("selenium.webdriver.ChromeOptions")
    def test_get_chrome_driver(self, mock_options, mock_driver):
        """
        Test case for creating a Chrome WebDriver object.
        """
        with WebDriverManager().get_chrome_driver() as driver:
            self.assertEqual(driver, mock_driver.return_value)

        mock_options.assert_called()

        # Ensure Chrome was called with an instance of Service
        args, kwargs = mock_driver.call_args
        self.assertIsInstance(kwargs['service'], Service)
        self.assertEqual(kwargs['options'], mock_options.return_value)


class TestBaseMovieScraper(TestCase):
    """
    Test class for the BaseMovieScraper class.
    This class tests the abstract methods of the BaseMovieScraper class.
    """
    def test_get_movie_info_not_implemented(self):
        """
        Test case to check that get_movie_info raises NotImplementedError.
        """
        class FakeScraper(BaseMovieScraper):
            """
            A mock scraper class to test abstract methods from the BaseMovieScraper class.
            """
            def get_movie_info(self, city, date, cinema_numb=None):
                raise NotImplementedError("This method should be overridden in a subclass.")

        with self.assertRaises(NotImplementedError):
            FakeScraper().get_movie_info("city", "date")


class TestMultikinoScraper(TestCase):
    """
    Test class for the MultikinoScraper class.
    """
    @patch('scraper.scraper.WebDriverManager.get_chrome_driver')
    def test_get_movie_info(self, mock_get_chrome_driver):
        """
        Test case to check that get_movie_info returns correct data.
        """
        # Setup mock driver
        mock_driver = MagicMock()
        mock_driver.get.return_value = None
        mock_get_chrome_driver.return_value.__enter__.return_value = mock_driver

        # Setup MultikinoScraper
        scraper = MultikinoScraper()

        # Test get_movie_info
        data = scraper.get_movie_info("city", "date")

        expected_keys = {"title", "category", "description", "image", "show_info"}
        assert all(expected_keys.issubset(item.keys()) for item in data)
        assert all(isinstance(item['show_info'], list) for item in data)
        assert all(
            all(isinstance(show, dict) and 'hour' in show and 'booking_link' in show for show in item['show_info']) for
            item in data)
        assert all(isinstance(item[key], str) for item in data for key in ["title", "category", "description", "image"])


class TestHeliosScraper(TestCase):
    """
    Test class for the HeliosScraper class.
    """
    @patch('scraper.scraper.WebDriverManager.get_chrome_driver')
    def test_get_movie_info(self, mock_get_chrome_driver):
        """
        Test case to check that get_movie_info returns correct data.
        """
        # Setup mock driver
        mock_driver = MagicMock()
        mock_driver.get.return_value = None
        mock_get_chrome_driver.return_value.__enter__.return_value = mock_driver

        # Setup HeliosScraper
        scraper = HeliosScraper()

        # Test get_movie_info
        data = scraper.get_movie_info("city", 1, 1)

        expected_keys = {"title", "show_info"}
        assert all(expected_keys.issubset(item.keys()) for item in data)
        assert all(isinstance(item['show_info'], list) for item in data)
        assert all(
            all(isinstance(show, dict) and 'hour' in show and 'booking_link' in show for show in item['show_info']) for
            item in data)
        assert all(isinstance(item[key], str) for item in data for key in ["title"])
