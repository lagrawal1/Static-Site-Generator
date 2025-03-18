import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq_TextType(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_URL(self):
        node = TextNode("This is a text node", TextType.BOLD, "idk.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "iknow.com")
        self.assertNotEqual(node, node2)

    def test_noteq_Content(self):
        node = TextNode("This is not a text node. Or is it", TextType.BOLD, "iknow.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "iknow.com")
        self.assertNotEqual(node, node2)
    
    def test_noteq_NoURL(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "iknow.com")
        self.assertNotEqual(node, node2)

class TestTextNodetoHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()

