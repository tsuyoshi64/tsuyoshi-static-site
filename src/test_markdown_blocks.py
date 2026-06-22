import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_standard_blocks(self):
        """Test standard blocks separated by exact double newlines."""
        markdown = "Block 1\n\nBlock 2\n\nBlock 3"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace_stripping(self):
        """Test that leading and trailing whitespace is stripped from each block."""
        markdown = "  Block 1  \n\n\tBlock 2\n\nBlock 3 \n"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_excessive_newlines(self):
        """Test that excessive newlines don't create empty blocks."""
        markdown = "Block 1\n\n\n\nBlock 2\n\n\nBlock 3\n\n\n\n\n"
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_internal_newlines(self):
        """Test that single newlines inside a block are preserved."""
        markdown = "This is line 1\nThis is line 2\n\nThis is a new block"
        expected = ["This is line 1\nThis is line 2", "This is a new block"]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        """Test that an empty string returns an empty list."""
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_whitespace_only(self):
        """Test that a string of only spaces and newlines returns an empty list."""
        markdown = "   \n\n   \n\n  \n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_block(self):
        """Test that a string with no double newlines returns a single block."""
        markdown = "Just one continuous block of text."
        expected = ["Just one continuous block of text."]
        self.assertEqual(markdown_to_blocks(markdown), expected)


if __name__ == "__main__":
    unittest.main()
