import unittest
from src.main import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_first_level_header(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Hello"
        )

    def test_missing_header(self):
        md = "Hello"
        with self.assertRaises(Exception):
            title = extract_title(md)
    
    def test_second_level_header(self):
        md = "## Hello"
        with self.assertRaises(Exception):
            title = extract_title(md)

    def test_missing_space(self):
        md = "#Hello"
        with self.assertRaises(Exception):
            title = extract_title(md)