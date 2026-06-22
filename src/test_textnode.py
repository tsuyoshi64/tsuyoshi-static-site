import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from utils.helper import split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()
