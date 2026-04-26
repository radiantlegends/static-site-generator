import unittest
from src.block_parser import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )
    
    def test_single_block(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is a single paragraph."]
        )

    def test_multiple_blank_lines(self):
        md = """
This test includes excessive amounts of blank spaces.



See? That's a lot of space.




- There's more above this list!
- Why so many?!
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This test includes excessive amounts of blank spaces.",
                "See? That's a lot of space.",
                "- There's more above this list!\n- Why so many?!",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_heading(self):
        md = "# This is a heading"
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        print(block_type)
        self.assertEqual(block_type, BlockType.HEADING)