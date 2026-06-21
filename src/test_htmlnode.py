import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node: LeafNode = LeafNode("span", "child")
        parent_node: ParentNode = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node: LeafNode = LeafNode("b", "grandchild")
        child_node: ParentNode = ParentNode("span", [grandchild_node])
        parent_node: ParentNode = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node: ParentNode = ParentNode(
            "p",
            [
                LeafNode("b", "Bold Text"),
                LeafNode(None, "Normal Text"),
                LeafNode("i", "Italic Text"),
                LeafNode(None, "Normal Text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold Text</b>Normal Text<i>Italic Text</i>Normal Text</p>",
        )

    def test_to_html_miserably_deeply_nested(self):
        node: ParentNode = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("a", "Item 1", {"href": "/1"})]),
                        ParentNode("li", [LeafNode("span", "Item 2")]),
                    ],
                    {"class": "list-wrapper"},
                )
            ],
            {"id": "main-container"},
        )
        expected = (
            '<div id="main-container">'
            '<ul class="list-wrapper">'
            '<li><a href="/1">Item 1</a></li>'
            "<li><span>Item 2</span></li>"
            "</ul>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected)

        def test_to_html_empty_children_list(self):
            node: ParentNode = ParentNode("div", [])
            self.assertEqual(node.to_html(), "<div></div>")

        def test_to_html_missing_tag_raises_error(self):
            node: ParentNode = ParentNode(None, [LeafNode("span", "text")])
            with self.assertRaises(ValueError) as context:
                node.to_html()
            self.assertEqual(
                str(context.exception), "All parent nodes should have a tag."
            )

        def test_to_html_missing_children_raises_error(self):
            node: ParentNode = ParentNode("div", None)
            with self.assertRaises(ValueError) as context:
                node.to_html()
            self.assertEqual(
                str(context.exception),
                "All parent should have their children (I bet you understand that).",
            )


if __name__ == "__main__":
    unittest.main()
