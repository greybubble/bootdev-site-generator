import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
from utilities import text_node_to_html_node

class TestUtilities(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_invalid_text_type(self):
        node = TextNode("This shouldn't work", "Grand")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
