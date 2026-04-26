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
    if(block.startswith("#")):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH

'''
Headings start with 1-6 # characters, followed by a space and then the heading text.
Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
Every line in a quote block must start with a "greater-than" character: > followed by the quote text. A space after > is allowed but not required.
Every line in an unordered list block must start with a - character, followed by a space.
Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
If none of the above conditions are met, the block is a normal paragraph.
'''