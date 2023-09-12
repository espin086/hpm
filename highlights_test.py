"""
This is a test file for the highlights.py file. It tests the following functions:

"""


import unittest
from unittest.mock import patch

from highlights import (
    get_summary,
    render_summary_button,
    render_text_area,
    render_title,
)


class TestHighlights(unittest.TestCase):
    """Test the highlights.py file."""

    @patch("highlights.st.title")
    @patch("highlights.st.write")
    def test_render_title(self, mock_write, mock_title):
        """Test that the title and horizontal line are rendered."""
        render_title()
        mock_title.assert_called_with("Weekly Report Generator")
        mock_write.assert_called_with("---")

    @patch("highlights.st.text_area")
    def test_render_text_area(self, mock_text_area):
        """Test that the text area is rendered."""
        mock_text_area.return_value = "Test text"
        result = render_text_area("Test Section", "Help Text")
        mock_text_area.assert_called_with("", help="Help Text", key="Test Section")
        self.assertEqual(result, "Test text")

    @patch("highlights.st.button")
    def test_render_summary_button(self, mock_button):
        """Test that the summary button is rendered."""
        mock_button.return_value = True
        result = render_summary_button()
        mock_button.assert_called_with("Summarize", key="btn_summarize")
        self.assertTrue(result)

    @patch("highlights.generate_completion")
    def test_get_summary(self, mock_generate_completion):
        """Test that the summary is generated."""
        mock_generate_completion.return_value = "Summary text"
        result = get_summary("model", "role", "prompt")
        mock_generate_completion.assert_called_with("model", "role", "prompt")
        self.assertEqual(result, "Summary text")


if __name__ == "__main__":
    unittest.main()
