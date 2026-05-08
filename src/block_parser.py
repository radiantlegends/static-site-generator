import re
from enum import Enum
from html_node import HTMLNode, LeafNode, ParentNode
from text_node import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    if(re.match(r"^#{1,6}\s.+", block)):
        return BlockType.HEADING
    elif(re.match(r"\`{3}\n(?:.|\n)*?\`{3}", block)):
        return BlockType.CODE
    elif(re.match(r"^(?:>.+\n?)+", block)):
        return BlockType.QUOTE
    elif(re.match(r"^(?:-.+\n?)+", block)):
        return BlockType.UNORDERED_LIST
    elif(re.match(r"^(?:\d\.\s+.+)(?:\n\d+\.\s+.+)*", block)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return LeafNode("p", block)
        case BlockType.HEADING:
            return LeafNode("h1", block[2:])


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print(f"Blocks: {blocks}")
    html_nodes = []
    for block in blocks:
        print("------------------------------")
        print(f"Block: {block}")
        block_type = block_to_block_type(block)
        print(f"Block Type: {block_type}")
        node = block_to_html_node(block, block_type)
        print(node)
        html_nodes.append(node)
    print(f"HTML Nodes: {html_nodes}")
    return ParentNode("div", html_nodes)

markdown_to_html_node("# H1 Header")