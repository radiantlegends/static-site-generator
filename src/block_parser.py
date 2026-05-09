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
                code_text = match.group(1).rstrip("\n")
            else:
                code_text = block
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, code_text)])])

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

md_paragraph = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

md_heading = """
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header
"""

md_code = """
```
This is a code block. **Bold** and _italic_ show as plain text.
```
"""

node = markdown_to_html_node(md_code)
html = node.to_html()
print(html)