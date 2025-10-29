import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    node1 = HTMLNode('a', "to google!", None, {"href": "https://www.google.com", "target":"_blank",})
    node2 = HTMLNode('abbr', "WHO", None, {"title":"World Health Organization",})
    node3 = HTMLNode('b', "Some bold text")
    def test_two_props_to_html(self):
        result = self.node1.props_to_html()
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(result, expected)

    def test_one_props_to_html(self):
        result = self.node2.props_to_html()
        expected = ' title="World Health Organization"'
        self.assertEqual(result, expected)

    def test_none_props_to_html(self):
        result = self.node3.props_to_html()
        expected = ""
        self.assertEqual(result, expected)

    