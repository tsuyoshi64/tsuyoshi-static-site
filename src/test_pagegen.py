import unittest

from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_standard_extraction(self):
        """Tests a standard h1 header on the first line."""
        self.assertEqual(extract_title("# Hello World"), "Hello World")

    def test_whitespace_padding(self):
        """Tests if leading and trailing whitespaces are properly stripped."""
        self.assertEqual(extract_title("#    Spaced Title   "), "Spaced Title")

    def test_iterative_search(self):
        """Tests if the function finds the header when it is not on the first line."""
        markdown = "Some intro text.\n\n# Main Title\n\nMore text."
        self.assertEqual(extract_title(markdown), "Main Title")

    def test_exception_triggering_no_header(self):
        """Tests if the exact base Exception is raised when no h1 exists."""
        markdown = "Just some text\nWithout any header"
        with self.assertRaisesRegex(Exception, "No header found."):
            extract_title(markdown)

    def test_strict_matching_ignores_subheaders(self):
        """Tests if the function ignores h2 and h3 tags and only targets h1."""
        markdown = "## Subheader\n### Another Sub\n# Real Title"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_strict_matching_ignores_inline_hash(self):
        """Tests if an inline hash symbol is correctly ignored."""
        markdown = "This sentence contains a # symbol.\n# Actual Header"
        self.assertEqual(extract_title(markdown), "Actual Header")

    def test_strict_matching_ignores_no_space_hash(self):
        """Tests if a hash without a trailing space is correctly ignored."""
        markdown = "#InvalidHeaderNoSpace\n# Valid Header"
        self.assertEqual(extract_title(markdown), "Valid Header")


if __name__ == "__main__":
    unittest.main()
