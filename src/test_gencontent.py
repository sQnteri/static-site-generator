import unittest
from src.gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# My Title
        This is some content."""
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_no_header(self):
        markdown = """This is some content without a header."""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_extract_title_whitespace(self):
        markdown = """
        # My Title with Whitespace    

        This is some content.
        """
        self.assertEqual(extract_title(markdown), "My Title with Whitespace")
