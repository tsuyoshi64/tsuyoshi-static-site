import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from utils.helper import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This node is different", TextType.ITALIC)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node4, node3)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_normal(self):
        node: TextNode = TextNode("Normal text", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Normal text")

    def test_bold(self):
        node: TextNode = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node: TextNode = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node: TextNode = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node: TextNode = TextNode("Click me!", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node: TextNode = TextNode(
            "Alt text description", TextType.IMAGE, "https://image.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://image.com", "alt": "Alt text description"}
        )

    def test_invalid_type(self):
        node: TextNode = TextNode("Bypassed Type", "Invalid enum value")  # type: ignore
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node: TextNode = TextNode("This is a `code block` word.", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word.", TextType.NORMAL),
            ],
        )

    def test_bold(self):
        node: TextNode = TextNode("This is a **bold block** word.", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.NORMAL),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word.", TextType.NORMAL),
            ],
        )

    def test_italic(self):
        node: TextNode = TextNode("This is a *italic block* word.", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.NORMAL),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word.", TextType.NORMAL),
            ],
        )

    def test_multiple_delimiters_same_type(self):
        node: TextNode = TextNode("Use `a` and `b` in your code.", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Use ", TextType.NORMAL),
                TextNode("a", TextType.CODE),
                TextNode(" and ", TextType.NORMAL),
                TextNode("b", TextType.CODE),
                TextNode(" in your code.", TextType.NORMAL),
            ],
        )

    def test_starts_and_end_with_delimiter(self):
        node: TextNode = TextNode("**Bold is Bold**", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Bold is Bold", TextType.BOLD),
            ],
        )

    def test_multiple_nodes(self):
        node1: TextNode = TextNode("Text with `code`", TextType.NORMAL)
        node2: TextNode = TextNode("Bold node", TextType.BOLD)
        node3: TextNode = TextNode("Another text with `code`", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter(
            [node1, node2, node3], "`", TextType.CODE
        )
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text with ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                node2,
                TextNode("Another text with ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_no_delimiter(self):
        node: TextNode = TextNode("Portugal", TextType.NORMAL)
        new_nodes: list[TextNode] = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_unclosed_delimiter(self):
        node: TextNode = TextNode("I am **Umamusume", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "Here is ![one](url1.png) and another ![two](url2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("one", "url1.png"), ("two", "url2.jpg")], matches)

    def test_extract_images_no_matches(self):
        text = "This text has standard [links](https://link.com) but zero images."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_links(self):
        text = "Click [here](url1) or check this [doc](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("here", "url1"), ("doc", "url2")], matches)

    def test_links_ignores_images(self):
        text = "This has an ![image](img_url) and a plain [link](link_url)"
        matches = extract_markdown_links(text)
        # It should ignore the image and only capture the link
        self.assertListEqual([("link", "link_url")], matches)


class TestSplitNodes(unittest.TestCase):
    def test_split_link_basic(self):
        """Test a normal sentence containing a single markdown link"""
        node = TextNode("Go to [boot dev](https://www.boot.dev) now!", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Go to ", TextType.NORMAL),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" now!", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_at_start(self):
        """Test text starting immediately with a markdown link"""
        node = TextNode("[boot dev](https://www.boot.dev) is cool", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is cool", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_link_at_end(self):
        """Test text ending exactly on a markdown link"""
        node = TextNode("Visit [boot dev](https://www.boot.dev)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visit ", TextType.NORMAL),
            TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_links(self):
        """Test multiple distinct markdown links in a sequence"""
        node = TextNode("Links [a](url_a) and [b](url_b) here", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Links ", TextType.NORMAL),
            TextNode("a", TextType.LINK, "url_a"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("b", TextType.LINK, "url_b"),
            TextNode(" here", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_consecutive_identical_links(self):
        """Test consecutive duplicate links to verify sequential split consumption works"""
        node = TextNode("[link](url)[link](url)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_no_links(self):
        """Test text containing no links remains completely untouched"""
        node = TextNode("Just plain text with nothing special.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_image_basic(self):
        """Test a normal sentence containing a single markdown image"""
        node = TextNode("Check out ![logo](https://boot.dev)!", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Check out ", TextType.NORMAL),
            TextNode("logo", TextType.IMAGE, "https://boot.dev"),
            TextNode("!", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_image_at_start(self):
        """Test text starting immediately with a markdown image"""
        node = TextNode("![logo](https://boot.dev) text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("logo", TextType.IMAGE, "https://boot.dev"),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_multiple_images(self):
        """Test parsing multiple distinct images across a block of text"""
        node = TextNode("![one](url1) then ![two](url2)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" then ", TextType.NORMAL),
            TextNode("two", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_no_images(self):
        """Test text containing no images remains completely untouched"""
        node = TextNode("Just plain text without graphics.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    # ==========================================
    # SYSTEM BOUNDARY & STRUCTURAL TESTS
    # ==========================================

    def test_ignores_non_normal_nodes(self):
        """Verify formatted nodes (like BOLD) are skipped and not split further"""
        bold_node = TextNode("Don't change [link](url)", TextType.BOLD)
        image_node = TextNode("Don't touch ![alt](url)", TextType.IMAGE)

        link_split = split_nodes_link([bold_node])
        image_split = split_nodes_image([image_node])

        self.assertEqual(link_split, [bold_node])
        self.assertEqual(image_split, [image_node])

    def test_empty_list(self):
        """Passing an empty node collection returns an empty list safely"""
        self.assertEqual(split_nodes_link([]), [])
        self.assertEqual(split_nodes_image([]), [])


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
