import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_invalid_markdown(self):
        matches = extract_markdown_images(
            "This is ![] not valid markdown for an image."
        )
        self.assertListEqual([], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_image_and_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class testExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_invalid_markdown(self):
        matches = extract_markdown_links(
            "This is [] not valid markdown for links."
        )
        self.assertListEqual([], matches)

    def test_image_and_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

if __name__ == "main":
    unittest.main()