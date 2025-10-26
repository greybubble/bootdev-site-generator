import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("Here is some text", TextType.ITALIC)
        node2 = TextNode("Here is some text", TextType.ITALIC)
        self.assertEqual(node1, node2)

    def test_text_not_eq(self):
        node1 = TextNode("Here is some text", TextType.ITALIC)
        node2 = TextNode("Here is some text.", TextType.ITALIC)
        self.assertEqual(node1, node2)

    def test_text_node_not_eq(self):
        node1 = TextNode("Here is some text", TextType.ITALIC, "http://www.someaddress.com")
        node2 = TextNode("Here is some text", TextType.BOLD, "http://www.someaddress.com")
        self.assertEqual(node1, node2)

    def test_url_not_eq(self):
        node1 = TextNode("Here is some text", TextType.ITALIC, "http://www.someaddress.com")
        node2 = TextNode("Here is some text", TextType.ITALIC, "http://www.someotheraddress.com")
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
