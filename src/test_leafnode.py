import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "This is some anchor text", {"href":"https://www.google.com",})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">This is some anchor text</a>')

    def test_leaf_no_value(self):
        node = LeafNode("a", None, {"href":"https://www.google.com",})
        with self.assertRaises(ValueError):
            node.to_html()


    def test_leaf_no_tag(self):
        node = LeafNode("", "This is some anchor text", {"href":"https://www.google.com",})
        self.assertEqual(node.to_html(), node.value)