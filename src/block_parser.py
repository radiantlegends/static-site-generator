import re
from enum import Enum

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