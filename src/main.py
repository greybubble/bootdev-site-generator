from textnode import TextNode, TextType
from leafnode import LeafNode

def main():
    some_text = LeafNode("a", "This is some anchor text", {"href":"https://www.google.com",})
    print(some_text)
    print(some_text.to_html())


if __name__ == "__main__":
    main()
