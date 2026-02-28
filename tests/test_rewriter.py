import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rewriter import rewrite_content


class TestRewriter(unittest.TestCase):
    @patch("src.rewriter._call_gemini_with_fallback")
    def test_rewrite_content_success(self, mock_gemini):
        mock_gemini.return_value = "Rewritten awesome insight"

        result = rewrite_content("Boring test content", "Boring Title")
        self.assertEqual(result, "Rewritten awesome insight")
        mock_gemini.assert_called_once()

    @patch("src.rewriter._call_gemini_with_fallback")
    def test_rewrite_content_fallback_to_original(self, mock_gemini):
        # If API fails, it should return original content
        mock_gemini.return_value = None

        result = rewrite_content("Boring test content", "Boring Title")
        self.assertEqual(result, "Boring test content")


if __name__ == "__main__":
    unittest.main()
