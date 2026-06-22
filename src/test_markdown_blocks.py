import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


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

    def test_headings_and_text(self):
        md = """
        # Primary Heading

        This is a paragraph beneath the primary heading.

        ## Secondary Heading

        This paragraph has **bold** and *italic* text.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Primary Heading",
                "This is a paragraph beneath the primary heading.",
                "## Secondary Heading",
                "This paragraph has **bold** and *italic* text.",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        self.assertEqual(
            block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        code_block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("``` incomplete code"), BlockType.PARAGRAPH
        )

    def test_quote_blocks(self):
        self.assertEqual(block_to_block_type("> Single quote line"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("> Line 1\n>Line 2\n> Line 3"), BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("> Line 1\n Missing bracket"), BlockType.PARAGRAPH
        )

    def test_unordered_lists(self):
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(block_to_block_type("-Item 1 no space"), BlockType.PARAGRAPH)
        self.assertEqual(
            block_to_block_type("- Item 1\nNormal line"), BlockType.PARAGRAPH
        )

    def test_ordered_lists(self):
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n3. Third"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. First\n3. Out of order"), BlockType.PARAGRAPH
        )
        self.assertEqual(block_to_block_type("2. Missing start"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.No space"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph line."), BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()
