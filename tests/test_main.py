import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import generate_site


class TestMain(unittest.TestCase):
    @patch("src.main.get_todays_featured_article")
    @patch("src.main.rewrite_content")
    @patch("builtins.open", new_callable=mock_open, read_data="{{title}} {{content}}")
    @patch("src.main.json.dump")
    def test_generate_site_full_flow(
        self, mock_json, mock_file, mock_rewrite, mock_get_article
    ):
        # Setup mock article
        mock_get_article.return_value = {
            "title": "Test Article",
            "extract": "Test extract",
            "thumbnail": "http://thumb",
            "url": "http://url",
        }
        mock_rewrite.return_value = "Rewritten insight"

        # We need to mock Path.exists so template is considered "found"
        with patch("src.main.Path.exists", return_value=True):
            generate_site()

        # Verify it called rewrite
        mock_rewrite.assert_called_once_with("Test extract", "Test Article")
        # Template was opened and writing was opened (index.html, meta.json)
        self.assertTrue(mock_file.call_count >= 3)
        mock_json.assert_called_once()

    @patch("src.main.get_todays_featured_article")
    def test_generate_site_no_content(self, mock_get_article):
        # Return an article without extract
        mock_get_article.return_value = {"title": "Empty Article"}

        # Test it returns early without error
        generate_site()


if __name__ == "__main__":
    unittest.main()
