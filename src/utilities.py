from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.LINK:
            return LeafNode(TextType.LINK.value, text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(TextType.IMAGE.value, "", {"src": text_node.url, "alt": text_node.text})
        case TextType.BOLD | TextType.ITALIC | TextType.TEXT | TextType.CODE:
            return LeafNode(text_node.text_type.value, text_node.text)
        
    raise ValueError(f"Error: Invalid text type {text_node.text_type}")
