import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_node_bold(self):
        node = TextNode("This is text with a **bold** word.", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.TEXT)
        ])
    
    def test_split_node_italic(self):
        node = TextNode("This is text with an _italic_ word.", TextType.TEXT)
        node2 = TextNode("This is text with another _italicized_ word.", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node, node2], "_", TextType.ITALIC),
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
            TextNode("This is text with another ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT)
        ])
    
    def test_split_node_error_syntax(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is **invalid Markdown syntax.", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Invalid Markdown syntax - matching delimiter not found.", str(context.exception))

if __name__ == "main":
    unittest.main()