import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_eq_2(self):
        node = HTMLNode(
            "a", "Google", [""], {"href": "https://www.google.com", "target": "_blank"}
        )
        node2 = HTMLNode(
            "a", "Google", [""], {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertNotEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode(
            "a", "Google", [""], {"href": "https://www.google.com", "target": "_blank"}
        )
        node2 = HTMLNode("p", "Lorem ipsum dolor sit amet", ["p"])
        self.assertNotEqual(node, node2)

    def test_props_1(self):
        node = HTMLNode("p", "Lorem ipsum dolor sit amet", ["p"])
        self.assertEqual(node.props_to_html(), "")

    def test_props_2(self):
        node = HTMLNode(
            "a", "Google", [""], {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href = "https://www.google.com" target = "_blank"'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Link", {"href": "link.com"})
        self.assertEqual(node.to_html(), f'<a href = "link.com">Link</a>')


if __name__ == "__main__":
    unittest.main()
