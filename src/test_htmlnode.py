import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    
    def test_eq_2(self):
        node = HTMLNode("a" , "Google" , [""] , {"href": "https://www.google.com","target": "_blank"})
        node2 = HTMLNode("a" , "Google" , [""] , {"href": "https://www.google.com","target": "_blank"})
        self.assertNotEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("a" , "Google" , [""] , {"href": "https://www.google.com","target": "_blank"})
        node2 = HTMLNode("p", "Lorem ipsum dolor sit amet", ["p"])
        self.assertNotEqual(node, node2)
    
    def test_props_1(self):
        node = HTMLNode("p", "Lorem ipsum dolor sit amet", ["p"])
        self.assertEqual(node.props_to_html(), "")

    def test_props_2(self):
        node = HTMLNode("a" , "Google" , [""] , {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href = "https://www.google.com" target = "_blank"')


if __name__ == "__main__":
    unittest.main()

