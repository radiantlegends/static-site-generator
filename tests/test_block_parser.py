import unittest
from src.block_parser import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
from src.text_node import TextNode, TextType, text_node_to_html_node

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
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_code(self):
        md = """
        ```
        This is a code block.
        ```
        """
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_quote(self):
        md = "> This is a quote."
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_unordered_list(self):
        md = """
        - This is an unordered list.
        - There's even two items!
        """
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_ordered_list(self):
        md = """
        1. This is an ordered list.
        2. With two items!
        """
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_paragraph(self):
        md = "This is a regular sentence."
        blocks = markdown_to_blocks(md)
        block_type = block_to_block_type(blocks[0])
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    

class test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = "# H1 Header"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1 Header</h1></div>"
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )