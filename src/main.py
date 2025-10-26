from textnode import TextNode, TextType

def main():
    some_text = TextNode("This is some anchor text", TextType.BOLD)
    print(some_text)


if __name__ == "__main__":
    main()
