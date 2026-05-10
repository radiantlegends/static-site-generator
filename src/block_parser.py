import re
from enum import Enum
from html_node import HTMLNode, LeafNode, ParentNode
from text_node import TextNode, TextType, text_node_to_html_node
from split_nodes import text_to_textnodes, split_nodes_delimiter

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
    if(re.match(r"^#{1,6}\s+.*$", block)):
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

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            paragraph_text = " ".join(line.strip() for line in block.splitlines())
            children = text_to_children(paragraph_text)
            return ParentNode("p", children)
        case BlockType.HEADING:
            heading_match = re.match(r"^(#{1,6})\s+(.*)$", block)
            if(heading_match):
                level = len(heading_match.group(1))
                heading_text = heading_match.group(2).strip()
                return ParentNode(f"h{level}", text_to_children(heading_text))
        case BlockType.CODE:
            match = re.match(r"\`{3}(?:\n)?(.*?)\`{3}", block, re.DOTALL)
            if(match):
                code_text = match.group(1)
            else:
                code_text = block
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_text)])])
        case BlockType.QUOTE:
            quote_lines = [re.sub(r"^>\s?", "", line).strip() for line in block.splitlines()]
            quote_text = " ".join(line for line in quote_lines)
            children = text_to_children(quote_text)
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            items = [re.sub(r"^-\s+", "", line).strip() for line in block.splitlines()]
            list_items = []
            for item in items:
                children = text_to_children(item)
                list_items.append(ParentNode("li", children))
            return ParentNode("ul", list_items)
        case BlockType.ORDERED_LIST:
            items = [re.sub(r"^\d+\.\s+", "", line).strip() for line in block.splitlines()]
            list_items = []
            for item in items:
                children = text_to_children(item)
                list_items.append(ParentNode("li", children))
            return ParentNode("ol", list_items)
        case _:
            raise Exception("Invalid Block Type: Unable to create HTML node.")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        html_nodes.append(node)
    return ParentNode("div", html_nodes)