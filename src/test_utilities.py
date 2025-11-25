import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
from utilities import *

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

    def test_split_nodes_bold_once(self):
        node1 = TextNode("This node is interesting in that it has a **bold** word in it", TextType.TEXT)
        expected_node_list = [TextNode("This node is interesting in that it has a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word in it", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter([node1], "**", TextType.BOLD), expected_node_list)

    def test_extract_markdown_images(self):
        mdtext = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        imagetext = extract_markdown_images(mdtext)
        print("testing markdown extraction of images")
        print(imagetext)

    def test_extract_markdown_links(self):
        mdtext = "This is text with a [rick roll link](https://i.imgur.com/aKaOqIh.gif) and ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        imagetext = extract_markdown_links(mdtext)
        print("testing markdown extraction of images")
        print(imagetext)

    def test_split_node_image(self):
        node1 = TextNode("This is text with a [link1](https://i.imgur.com/aKaOqIh.gif) and ![image1](https://i.imgur.com/fJRm4Vk.jpeg) and [another link](https://anotherlink.com) as well!", TextType.TEXT)
        node2 = TextNode("This is text with a ![image2](https://i.imgur.com/aKaOqIh.gif) and [link2](https://i.imgur.com/fJRm4Vk.jpeg) and ![another image](https://i.imgur.com/someimage.jpeg) as well!", TextType.TEXT)
        node3 = TextNode("This is text with a ![image3](https://i.imgur.com/aKaOqIh.gif) and ![image4](https://i.imgur.com/fJRm4Vk.jpeg) also!", TextType.TEXT)
        node4 = TextNode("This is text with a [link3](https://i.imgur.com/aKaOqIh.gif) and [link4](https://i.imgur.com/fJRm4Vk.jpeg) also!", TextType.TEXT)
        node_list = [node1, node2, node3, node4]
        new_node_list = split_nodes_image(node_list)
        expected_result = [
        TextNode("This is text with a [link1](https://i.imgur.com/aKaOqIh.gif) and ", TextType.TEXT, None),
        TextNode("image1", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and [another link](https://anotherlink.com) as well!", TextType.TEXT, None),
        TextNode("This is text with a ", TextType.TEXT, None),
        TextNode("image2", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and [link2](https://i.imgur.com/fJRm4Vk.jpeg) and ", TextType.TEXT, None),
        TextNode("another image", TextType.IMAGE, "https://i.imgur.com/someimage.jpeg"),
        TextNode(" as well!", TextType.TEXT, None),
        TextNode("This is text with a ", TextType.TEXT, None),
        TextNode("image3", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.TEXT, None),
        TextNode("image4", TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
        TextNode(" also!", TextType.TEXT, None),
        TextNode("This is text with a [link3](https://i.imgur.com/aKaOqIh.gif) and [link4](https://i.imgur.com/fJRm4Vk.jpeg) also!", TextType.TEXT, None)
        ]
        self.assertEqual(new_node_list, expected_result)

        # print()
        # print("-----------split nodes image------------")
        # for node in new_node_list:
        #     print(node)

    def test_split_node_link(self):
        node1 = TextNode("This is text with a [link1](https://i.imgur.com/aKaOqIh.gif) and ![image1](https://i.imgur.com/fJRm4Vk.jpeg) and [another link](https://anotherlink.com) as well!", TextType.TEXT)
        node2 = TextNode("This is text with a ![image2](https://i.imgur.com/aKaOqIh.gif) and [link2](https://i.imgur.com/fJRm4Vk.jpeg) and ![another image](https://i.imgur.com/someimage.jpeg) as well!", TextType.TEXT)
        node3 = TextNode("This is text with a ![image3](https://i.imgur.com/aKaOqIh.gif) and ![image4](https://i.imgur.com/fJRm4Vk.jpeg) also!", TextType.TEXT)
        node4 = TextNode("This is text with a [link3](https://i.imgur.com/aKaOqIh.gif) and [link4](https://i.imgur.com/fJRm4Vk.jpeg) also!", TextType.TEXT)
        node_list = [node1, node2, node3, node4]
        new_node_list = split_nodes_link(node_list)
        expected_result = [
        TextNode("This is text with a ", TextType.TEXT, None),
        TextNode("link1", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ![image1](https://i.imgur.com/fJRm4Vk.jpeg) and " , TextType.TEXT, None),
        TextNode("another link", TextType.LINK, "https://anotherlink.com"),
        TextNode( " as well!", TextType.TEXT, None),
        TextNode("This is text with a ![image2](https://i.imgur.com/aKaOqIh.gif) and " , TextType.TEXT, None),
        TextNode("link2", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and ![another image](https://i.imgur.com/someimage.jpeg) as well!", TextType.TEXT, None),
        TextNode("This is text with a ![image3](https://i.imgur.com/aKaOqIh.gif) and ![image4](https://i.imgur.com/fJRm4Vk.jpeg) also!", TextType.TEXT, None),
        TextNode("This is text with a " , TextType.TEXT, None),
        TextNode("link3", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.TEXT, None),
        TextNode("link4", TextType.LINK, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" also!", TextType.TEXT, None),
        ]
        self.assertEqual(new_node_list, expected_result)
        # print()
        # print("-----------split nodes link------------")
        # for node in new_node_list:
        #     print(node)