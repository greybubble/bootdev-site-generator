from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
from utilities import text_node_to_html_node

def main():
    some_text = LeafNode("a", "This is some anchor text", {"href":"https://www.google.com",})
    print(some_text)
    print(some_text.to_html())

    node1 = TextNode("Here is some italic text", TextType.ITALIC, "http://www.someaddress.com")
    node2 = TextNode("Here is some bolk text", TextType.BOLD, "http://www.someaddress.com")
    node3 = TextNode("Anchor text for a link", TextType.LINK, "http://www.someaddress.com")
    node4 = TextNode("image text for an image", TextType.IMAGE, "/some/place/on/my/computer.png")
    node5 = TextNode("Some code text here", TextType.CODE)
    node6 = TextNode("Some plain ol' text without a tag", TextType.TEXT)

    print(text_node_to_html_node(node1).to_html())
    print(text_node_to_html_node(node2).to_html())
    print(text_node_to_html_node(node3).to_html())
    print(text_node_to_html_node(node4).to_html())
    print(text_node_to_html_node(node5).to_html())
    print(text_node_to_html_node(node6).to_html())




if __name__ == "__main__":
    main()
