from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
import re
from blocktype import BlockType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.LINK:
            return LeafNode(TextType.LINK.value, text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(TextType.IMAGE.value, "", {"src": text_node.url, "alt": text_node.text})
        case TextType.BOLD | TextType.ITALIC | TextType.TEXT | TextType.CODE:
            return LeafNode(text_node.text_type.value, text_node.text)
        
    raise ValueError(f"Error: Invalid text type {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return []
    
    new_nodes = []

    for node in old_nodes:
        node_text = node.text.split(delimiter)

        if len(node_text)%2 == 0:
            raise Exception("Error: opening and closing delimiters don't match")
        
        for i in range(len(node_text)):
            if(i%2 == 0):
                new_nodes.append(TextNode(node_text[i], node.text_type))
            else:
                new_nodes.append(TextNode(node_text[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"(?<=!\[)([^\]\[]+)(?:\]\()([\w:/.-]+)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!\[)(?<=\[)([^\]\[]+)(?:\]\()([\w:/.-]+)", text)
    return matches

def split_nodes_image(old_nodes):
    if not old_nodes:
        return []
    
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        split_node = []
        current_text = node.text
        for i in range(0, len(images)):
            cut = current_text.split("![", 1)
            split_node.append(TextNode(cut[0],TextType.TEXT))
            split_node.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            cut = cut[1].split(")", 1)
            current_text = cut[1]
        split_node.append(TextNode(current_text,TextType.TEXT))
        new_nodes.extend(split_node)
    
    return new_nodes


def split_nodes_link(old_nodes):
    if not old_nodes:
        return []
    
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        split_node = []
        current_text = node.text
        for i in range(0, len(links)):
            cut = current_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if cut[0]:
                split_node.append(TextNode(cut[0],TextType.TEXT))
            split_node.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            # print("\n\nTesting split nodes link")
            # print(links)
            # print(cut)
            current_text = cut[1]
        if current_text:
            split_node.append(TextNode(current_text,TextType.TEXT))
        new_nodes.extend(split_node)
    
    return new_nodes

def text_to_textnodes(text):
    
    new_nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "`",TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes    

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n") 
    stripped_blocks = []
    for block in blocks:
        stripped = block.strip("\n ")
        if stripped:
            stripped_blocks.append(stripped)
    return stripped_blocks

def block_to_block_type(block):

    if re.match(r'#{1,6}\s', block):
        return BlockType.HEADING
    
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    if block[0] == ">":
        valid_quote = True
        lines = block.split('\n')
        for line in lines:
            if line[0] != '>':
                valid_quote = False
        
        if valid_quote:
            return BlockType.QUOTE
        
    if block[0:2] == "- ":
        valid_list = True
        lines = block.split('\n')
        for line in lines:
            if line[0:2] != '- ':
                valid_list = False
        if valid_list:
            return BlockType.UNORDERED_LIST
    
    if block[0:3] == "1. ":
        valid_list = True
        lines = block.split('\n')
        for i in range(1,len(lines)):
            start = lines[i].split(" ", 1)[0]
            if start != (str(i+1)+'.'):
                valid_list = False
        if valid_list:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def ul_block_to_html_node(block):
    l_children = []
    bullets = block.split("\n")

    for bullet in bullets:
        # print("\n\n Testing ul block to html node")
        # print(bullet[2:])
        text_nodes = text_to_textnodes(bullet[2:])
        h_nodes = []
        for node in text_nodes:
            h_nodes.append(text_node_to_html_node(node))
        bullet_node = ParentNode("li", h_nodes)
        l_children.append(bullet_node)

    return ParentNode("ul", l_children)

def ol_block_to_html_node(block):
    l_children = []
    bullets = block.split("\n")

    for bullet in bullets:
        text_nodes = text_to_textnodes(bullet.split(" ", 1)[1])
        h_nodes = []
        for node in text_nodes:
            h_nodes.append(text_node_to_html_node(node))
        bullet_node = ParentNode("li", h_nodes)
        l_children.append(bullet_node)

    return ParentNode("ol", l_children)

def quote_block_to_html_node(block):
    lines = block.split("\n")
    quote = []
    for line in lines:
        quote.append(line[2:])
    quote = ' '.join(quote)

    quote_tnodes = text_to_textnodes(quote)
    quote_hnodes = []
    for node in quote_tnodes:
        quote_hnodes.append(text_node_to_html_node(node))

    return ParentNode("blockquote", quote_hnodes)

def p_block_to_html_node(block):
    p_tnodes = text_to_textnodes(block.replace('\n', ' '))
    p_hnodes = []
    for node in p_tnodes:
        p_hnodes.append(text_node_to_html_node(node))
    
    return ParentNode("p", p_hnodes)

def code_block_to_html_node(block):
    text = block.strip('`').lstrip('\n')
    node = TextNode(text, TextType.CODE)
    hnode = text_node_to_html_node(node)

    return ParentNode("pre", [hnode])

def heading_block_to_html_node(block):
    heading = block.split(' ', 1)
    size = len(heading[0])
    tag = 'h' + str(size)
    h_tnodes = text_to_textnodes(heading[1])
    h_hnodes = []
    for node in h_tnodes:
        h_hnodes.append(text_node_to_html_node(node))
    
    return ParentNode(tag, h_hnodes)

def block_to_html_node(block):
    btype = block_to_block_type(block)

    match btype:
        case BlockType.CODE:
            return code_block_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ul_block_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ol_block_to_html_node(block)
        case BlockType.PARAGRAPH:
            return p_block_to_html_node(block)
        case BlockType.QUOTE:
            return quote_block_to_html_node(block)
        case BlockType.HEADING:
            return heading_block_to_html_node(block)
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        html_nodes.append(block_to_html_node(block))

    return ParentNode("div", html_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and block[0:2] == "# ":
            return block[2:]
    
    raise Exception("Error: No h1 heading included in the provided markdown text")






