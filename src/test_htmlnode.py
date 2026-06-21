import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_populated(self):
        node = HTMLNode(
            tag="a", props={"href": "https://google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_props_to_html_empty_and_none(self):
        node_none = HTMLNode(tag="p", props=None)
        node_empty = HTMLNode(tag="p", props={})

        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_repr_output(self):
        child_node = HTMLNode(tag="span", value="Hello")
        parent_node = HTMLNode(tag="div", children=[child_node])

        expect_repr = "HTMLNode(div, None, [HTMLNode(span, Hello, None, None)], None)"
        self.assertEqual(repr(parent_node), expect_repr)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node: LeafNode = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_props(self):
        node: LeafNode = LeafNode("a", "Click me!", {"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        node: LeafNode = LeafNode(None, "Text")
        self.assertEqual(node.to_html(), "Text")

    def test_leaf_to_html_missn_values(self):
        node: LeafNode = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_node_repr(self):
        node: LeafNode = LeafNode("h1", "Title", {"id": "main"})
        expected_repr = "LeafNode(h1, Title, {'id': 'main'})"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
