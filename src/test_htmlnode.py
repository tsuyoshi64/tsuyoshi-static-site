import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()

# f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
