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
    matches = re.findall(r"(?<=!\[)([\w\s\.]+)(?:\]\()([\w:/.]+)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!\[)(?<=\[)([\w\s\.]+)(?:\]\()([\w:/.]+)", text)
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
            cut = current_text.split("[", 1)
            while cut[0][-1] == '!':
                temp = cut[0]
                cut = cut[1].split("[", 1)
                cut[0] = temp + '[' + cut[0]
                print(cut)
            split_node.append(TextNode(cut[0],TextType.TEXT))
            split_node.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            cut = cut[1].split(")", 1)
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



