import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper import get_todays_featured_article

class TestScraper(unittest.TestCase):
    @patch('src.scraper.requests.get')
    def test_get_todays_featured_article_success(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tfa": {
                "titles": {"normalized": "Test Article"},
                "extract": "This is a test article.",
                "thumbnail": {"source": "http://image.url"},
                "content_urls": {"desktop": {"page": "http://article.url"}}
            }
        }
        mock_get.return_value = mock_response

        result = get_todays_featured_article()

        self.assertEqual(result['title'], "Test Article")
        self.assertEqual(result['extract'], "This is a test article.")
        self.assertEqual(result['thumbnail'], "http://image.url")
        self.assertEqual(result['url'], "http://article.url")

    @patch('src.scraper.requests.get')
    def test_get_todays_featured_article_failure(self, mock_get):
        # Mock failure response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_todays_featured_article()

        self.assertEqual(result['title'], "Error fetching article")

if __name__ == '__main__':
    unittest.main()
