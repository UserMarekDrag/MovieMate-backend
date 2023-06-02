import unittest
from unittest.mock import patch, MagicMock
from selenium.common import WebDriverException
from scraper.scraper import MultikinoScraper, HeliosScraper


class TestLogging(unittest.TestCase):
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
        mock_logging_error.assert_called_with('Error occurred: Message: Test exception\n')


class TestHeliosScraperLogging(unittest.TestCase):
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
        mock_logging_error.assert_called_with('Error occurred: Message: Test exception\n')
